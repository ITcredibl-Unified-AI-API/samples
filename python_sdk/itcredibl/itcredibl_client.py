"""
ITcredibl Enterprise Python Client
----------------------------------
Features:
  - Sync and async chat
  - SSE streaming
  - Retries with jitter and backoff
  - Timeouts
  - Provider pinning or auto-routing
"""
from __future__ import annotations

import os
import json
import logging
from typing import Any, AsyncGenerator, Dict, List, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type

DEFAULT_BASE_URL = os.getenv("ITCREDIBL_API_URL", "https://api.itcredibl.com/functions/v1/itcredibl-api")
DEFAULT_TIMEOUT = float(os.getenv("ITCREDIBL_TIMEOUT", "60"))
DEFAULT_MAX_RETRIES = int(os.getenv("ITCREDIBL_MAX_RETRIES", "3"))

class ITcrediblError(Exception):
    pass

class ITcrediblAuthError(ITcrediblError):
    pass

class ITcrediblRateLimitError(ITcrediblError):
    pass

class ITcrediblServerError(ITcrediblError):
    pass

def _classify(status: int) -> ITcrediblError:
    if status in (401, 403):
        return ITcrediblAuthError("Authentication failed or not authorized")
    if status == 429:
        return ITcrediblRateLimitError("Rate limit exceeded")
    if 500 <= status < 600:
        return ITcrediblServerError(f"Server error: {status}")
    return ITcrediblError(f"HTTP {status}")

def _build_headers(api_key: str, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    h = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "itcredibl-python-enterprise/1.0",
    }
    if extra:
        h.update(extra)
    return h

class ITcrediblClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("ITCREDIBL_API_KEY")
        if not self.api_key:
            raise ITcrediblAuthError("Missing API key. Set ITCREDIBL_API_KEY or pass api_key.")
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.log = logger or logging.getLogger("itcredibl")
        if not self.log.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self.log.addHandler(handler)
            self.log.setLevel(logging.INFO)

        self._client = httpx.Client(timeout=self.timeout)
        self._aclient = httpx.AsyncClient(timeout=self.timeout)

    def close(self) -> None:
        try:
            self._client.close()
        finally:
            try:
                import anyio  # type: ignore
                anyio.run(self._aclient.aclose)
            except Exception:
                pass

    @retry(
        reraise=True,
        stop=stop_after_attempt(DEFAULT_MAX_RETRIES),
        wait=wait_exponential_jitter(initial=0.5, max=4.0),
        retry=retry_if_exception_type((ITcrediblServerError, ITcrediblRateLimitError, httpx.TransportError)),
    )
    def chat(
        self,
        *,
        messages: List[Dict[str, str]],
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }
        if provider:
            payload["provider"] = provider
        if model:
            payload["model"] = model
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if extra:
            payload.update(extra)

        r = self._client.post(
            self.base_url,
            headers=_build_headers(self.api_key),
            json=payload,
        )
        if r.status_code != 200:
            raise _classify(r.status_code)
        try:
            return r.json()
        except Exception as e:
            raise ITcrediblError(f"Invalid JSON response: {e}")

    @retry(
        reraise=True,
        stop=stop_after_attempt(DEFAULT_MAX_RETRIES),
        wait=wait_exponential_jitter(initial=0.5, max=4.0),
        retry=retry_if_exception_type((ITcrediblServerError, ITcrediblRateLimitError, httpx.TransportError)),
    )
    async def chat_async(
        self,
        *,
        messages: List[Dict[str, str]],
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }
        if provider:
            payload["provider"] = provider
        if model:
            payload["model"] = model
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if extra:
            payload.update(extra)

        r = await self._aclient.post(
            self.base_url,
            headers=_build_headers(self.api_key),
            json=payload,
        )
        if r.status_code != 200:
            raise _classify(r.status_code)
        try:
            return r.json()
        except Exception as e:
            raise ITcrediblError(f"Invalid JSON response: {e}")

    async def chat_stream(
        self,
        *,
        messages: List[Dict[str, str]],
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        extra: Optional[Dict[str, Any]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        payload: Dict[str, Any] = {
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        if provider:
            payload["provider"] = provider
        if model:
            payload["model"] = model
        if extra:
            payload.update(extra)

        async with self._aclient.stream(
            "POST",
            self.base_url,
            headers=_build_headers(self.api_key),
            json=payload,
        ) as response:
            if response.status_code != 200:
                await response.aread()
                raise _classify(response.status_code)
            async for line in response.aiter_lines():
                if not line:
                    continue
                if line.startswith("data:"):
                    data = line[5:].strip()
                    if data.lower() == "[done]":
                        break
                    try:
                        yield json.loads(data)
                    except Exception:
                        yield {"raw": data}