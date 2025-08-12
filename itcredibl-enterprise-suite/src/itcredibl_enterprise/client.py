# from __future__ import annotations

# import os, json, time
# from typing import Any, AsyncIterator, Dict, List, Optional, Callable

# import httpx
# from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type

# DEFAULT_BASE_URL = (os.getenv("ITCREDIBL_API_URL") or "https://api.itcredibl.com").rstrip("/")
# DEFAULT_TIMEOUT = float(os.getenv("ITCREDIBL_TIMEOUT", "60"))
# DEFAULT_MAX_RETRIES = int(os.getenv("ITCREDIBL_MAX_RETRIES", "3"))
# DEFAULT_PROVIDER = os.getenv("ITCREDIBL_DEFAULT_PROVIDER", "openai")

# class ITCError(Exception): ...
# class ITCAuthError(ITCError): ...
# class ITCRateLimitError(ITCError): ...
# class ITCServerError(ITCError): ...

# def _classify(status: int) -> ITCError:
#     if status in (401, 403): return ITCAuthError("Auth failed or not authorized")
#     if status == 429: return ITCRateLimitError("Rate limit exceeded")
#     if 500 <= status < 600: return ITCServerError(f"Server error {status}")
#     return ITCError(f"HTTP {status}")

# def _headers(api_key: str, org: Optional[str]) -> Dict[str, str]:
#     h = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "User-Agent": "itcredibl-enterprise-demo/1.0"}
#     if org: h["X-Organization-Id"] = org
#     return h

# class ITcrediblClient:
#     """Enterprise‑friendly async client for the ITcredibl AI Gateway."""

#     def __init__(
#         self,
#         api_key: Optional[str] = None,
#         base_url: str = DEFAULT_BASE_URL,
#         org_id: Optional[str] = None,
#         default_provider: str = DEFAULT_PROVIDER,
#         timeout: float = DEFAULT_TIMEOUT,
#         max_retries: int = DEFAULT_MAX_RETRIES,
#         on_metrics: Optional[Callable[[Dict[str, Any]], None]] = None,
#     ) -> None:
#         self.api_key = api_key or os.getenv("ITCREDIBL_API_KEY")
#         if not self.api_key:
#             raise ITCAuthError("Missing ITCREDIBL_API_KEY")
#         self.base_url = base_url.rstrip("/")
#         self.org_id = org_id or os.getenv("ITCREDIBL_ORG_ID")
#         self.default_provider = default_provider
#         self.timeout = timeout
#         self.max_retries = max_retries
#         self.on_metrics = on_metrics

#         self._client = httpx.AsyncClient(
#             base_url=self.base_url,
#             headers=_headers(self.api_key, self.org_id),
#             timeout=self.timeout,
#         )

#     async def aclose(self) -> None:
#         await self._client.aclose()

#     @retry(reraise=True, stop=stop_after_attempt(DEFAULT_MAX_RETRIES), wait=wait_exponential_jitter(initial=0.5, max=4.0), retry=retry_if_exception_type((ITCServerError, ITCRateLimitError, httpx.TransportError)))
#     async def chat(self, messages: List[Dict[str, Any]], model: str, provider: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
#         payload = {"model": model, "messages": messages, "provider": provider or self.default_provider}
#         payload.update({k: v for k, v in kwargs.items() if v is not None})
#         t0 = time.perf_counter()
#         resp = await self._client.post("/v1/chat/completions", json=payload)
#         if resp.status_code != 200: raise _classify(resp.status_code)
#         data = resp.json(); self._emit_metrics("chat", t0, data, payload); return data

#     async def chat_stream(self, messages: List[Dict[str, Any]], model: str, provider: Optional[str] = None, **kwargs: Any) -> AsyncIterator[str]:
#         payload = {"model": model, "messages": messages, "provider": provider or self.default_provider, "stream": True}
#         payload.update({k: v for k, v in kwargs.items() if v is not None})
#         t0 = time.perf_counter()
#         async with self._client.stream("POST", "/v1/chat/completions", json=payload, headers={"Accept": "text/event-stream"}) as resp:
#             if resp.status_code != 200: raise _classify(resp.status_code)
#             async for line in resp.aiter_lines():
#                 if not line or not line.startswith("data:"): continue
#                 data = line[5:].strip()
#                 if data == "[DONE]": break
#                 try:
#                     obj = json.loads(data)
#                     delta = obj.get("choices", [{}])[0].get("delta", {})
#                     if "content" in delta and delta["content"]:
#                         yield delta["content"]
#                     else:
#                         msg = obj.get("choices", [{}])[0].get("message", {})
#                         if isinstance(msg, dict) and msg.get("content"): yield msg["content"]
#                 except Exception:
#                     if data: yield data
#         self._emit_metrics("chat_stream", t0, None, payload)

#     async def tool_call(self, messages: List[Dict[str, Any]], model: str, tools: List[Dict[str, Any]], provider: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
#         payload = {"model": model, "messages": messages, "tools": tools, "provider": provider or self.default_provider}
#         payload.update({k: v for k, v in kwargs.items() if v is not None})
#         t0 = time.perf_counter(); resp = await self._client.post("/v1/chat/completions", json=payload)
#         if resp.status_code != 200: raise _classify(resp.status_code)
#         data = resp.json(); self._emit_metrics("tool_call", t0, data, payload); return data

#     async def embeddings(self, inputs: List[str], model: str = "text-embedding-3-small") -> Dict[str, Any]:
#         payload = {"model": model, "input": inputs}
#         t0 = time.perf_counter(); resp = await self._client.post("/v1/embeddings", json=payload)
#         if resp.status_code != 200: raise _classify(resp.status_code)
#         data = resp.json(); self._emit_metrics("embeddings", t0, data, payload); return data

#     async def moderate(self, text: str) -> Dict[str, Any]:
#         payload = {"input": text}
#         t0 = time.perf_counter(); resp = await self._client.post("/v1/moderations", json=payload)
#         if resp.status_code != 200: raise _classify(resp.status_code)
#         data = resp.json(); self._emit_metrics("moderation", t0, data, payload); return data

#     async def usage(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
#         params: Dict[str, Any] = {}
#         if start_date: params["start_date"] = start_date
#         if end_date: params["end_date"] = end_date
#         t0 = time.perf_counter(); resp = await self._client.get("/v1/usage", params=params)
#         if resp.status_code != 200: raise _classify(resp.status_code)
#         data = resp.json(); self._emit_metrics("usage", t0, data, {"params": params}); return data

#     def _emit_metrics(self, op: str, t0: float, data: Optional[Dict[str, Any]], meta: Dict[str, Any]):
#         if not self.on_metrics: return
#         dur_ms = int((time.perf_counter() - t0) * 1000)
#         usage = (data or {}).get("usage", {})
#         payload = {
#             "operation": op,
#             "duration_ms": dur_ms,
#             "provider": (data or {}).get("provider") or meta.get("provider"),
#             "model": (data or {}).get("model") or meta.get("model"),
#             "tokens": {
#                 "prompt": usage.get("prompt_tokens"),
#                 "completion": usage.get("completion_tokens"),
#                 "total": usage.get("total_tokens"),
#             },
#             "cost": usage.get("cost"),
#         }
#         try: self.on_metrics(payload)
#         except Exception: pass


from __future__ import annotations

import os, json, time
from typing import Any, AsyncIterator, Dict, List, Optional, Callable

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type

DEFAULT_BASE_URL = (os.getenv("ITCREDIBL_API_URL") or "https://api.itcredibl.com").rstrip("/")
DEFAULT_TIMEOUT = float(os.getenv("ITCREDIBL_TIMEOUT", "60"))
DEFAULT_MAX_RETRIES = int(os.getenv("ITCREDIBL_MAX_RETRIES", "3"))
DEFAULT_PROVIDER = os.getenv("ITCREDIBL_DEFAULT_PROVIDER", "openai")

class ITCError(Exception): ...
class ITCAuthError(ITCError): ...
class ITCRateLimitError(ITCError): ...
class ITCServerError(ITCError): ...

def _classify(status: int) -> ITCError:
    if status in (401, 403): return ITCAuthError("Auth failed or not authorized")
    if status == 429: return ITCRateLimitError("Rate limit exceeded")
    if 500 <= status < 600: return ITCServerError(f"Server error {status}")
    return ITCError(f"HTTP {status}")

def _headers(api_key: str, org: Optional[str]) -> Dict[str, str]:
    h = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "User-Agent": "itcredibl-enterprise-demo/1.0"}
    if org: h["X-Organization-Id"] = org
    return h

class ITcrediblClient:
    """Enterprise-friendly async client for the ITcredibl AI Gateway."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        org_id: Optional[str] = None,
        default_provider: str = DEFAULT_PROVIDER,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        on_metrics: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("ITCREDIBL_API_KEY")
        if not self.api_key:
            raise ITCAuthError("Missing ITCREDIBL_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.org_id = org_id or os.getenv("ITCREDIBL_ORG_ID")
        self.default_provider = default_provider
        self.timeout = timeout
        self.max_retries = max_retries
        self.on_metrics = on_metrics

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=_headers(self.api_key, self.org_id),
            timeout=self.timeout,
        )

    # ---- routing helper: function base -> root (""), openai-style -> /v1/... ----
    def _is_function_base(self) -> bool:
        # heuristics for Supabase Functions or similar function-style endpoints
        return "/functions/" in self.base_url or self.base_url.endswith("/itcredibl-api")

    def _route(self, openai_v1_path: str) -> str:
        # On function base we POST to the root; on OpenAI-compatible base we use the given path
        return "" if self._is_function_base() else openai_v1_path

    async def aclose(self) -> None:
        await self._client.aclose()

    @retry(reraise=True, stop=stop_after_attempt(DEFAULT_MAX_RETRIES), wait=wait_exponential_jitter(initial=0.5, max=4.0), retry=retry_if_exception_type((ITCServerError, ITCRateLimitError, httpx.TransportError)))
    async def chat(self, messages: List[Dict[str, Any]], model: str, provider: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        payload = {"model": model, "messages": messages, "provider": provider or self.default_provider}
        payload.update({k: v for k, v in kwargs.items() if v is not None})
        t0 = time.perf_counter()
        resp = await self._client.post(self._route("/v1/chat/completions"), json=payload)
        if resp.status_code != 200: raise _classify(resp.status_code)
        data = resp.json(); self._emit_metrics("chat", t0, data, payload); return data

    async def chat_stream(self, messages: List[Dict[str, Any]], model: str, provider: Optional[str] = None, **kwargs: Any) -> AsyncIterator[str]:
        payload = {"model": model, "messages": messages, "provider": provider or self.default_provider, "stream": True}
        payload.update({k: v for k, v in kwargs.items() if v is not None})
        t0 = time.perf_counter()
        async with self._client.stream("POST", self._route("/v1/chat/completions"), json=payload, headers={"Accept": "text/event-stream"}) as resp:
            if resp.status_code != 200: raise _classify(resp.status_code)
            async for line in resp.aiter_lines():
                if not line or not line.startswith("data:"): continue
                data = line[5:].strip()
                if data.lower() in ("[done]", "[done]."): break
                try:
                    obj = json.loads(data)
                    delta = obj.get("choices", [{}])[0].get("delta", {})
                    if "content" in delta and delta["content"]:
                        yield delta["content"]
                    else:
                        msg = obj.get("choices", [{}])[0].get("message", {})
                        if isinstance(msg, dict) and msg.get("content"): yield msg["content"]
                except Exception:
                    if data: yield data
        self._emit_metrics("chat_stream", t0, None, payload)

    async def tool_call(self, messages: List[Dict[str, Any]], model: str, tools: List[Dict[str, Any]], provider: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        payload = {"model": model, "messages": messages, "tools": tools, "provider": provider or self.default_provider}
        payload.update({k: v for k, v in kwargs.items() if v is not None})
        t0 = time.perf_counter(); resp = await self._client.post(self._route("/v1/chat/completions"), json=payload)
        if resp.status_code != 200: raise _classify(resp.status_code)
        data = resp.json(); self._emit_metrics("tool_call", t0, data, payload); return data

    async def embeddings(self, inputs: List[str], model: str = "text-embedding-3-small") -> Dict[str, Any]:
        payload = {"model": model, "input": inputs}
        t0 = time.perf_counter(); resp = await self._client.post(self._route("/v1/embeddings"), json=payload)
        if resp.status_code != 200: raise _classify(resp.status_code)
        data = resp.json(); self._emit_metrics("embeddings", t0, data, payload); return data

    async def moderate(self, text: str) -> Dict[str, Any]:
        payload = {"input": text}
        t0 = time.perf_counter(); resp = await self._client.post(self._route("/v1/moderations"), json=payload)
        if resp.status_code != 200: raise _classify(resp.status_code)
        data = resp.json(); self._emit_metrics("moderation", t0, data, payload); return data

    async def usage(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if start_date: params["start_date"] = start_date
        if end_date: params["end_date"] = end_date
        t0 = time.perf_counter(); resp = await self._client.get(self._route("/v1/usage"), params=params)
        if resp.status_code != 200: raise _classify(resp.status_code)
        data = resp.json(); self._emit_metrics("usage", t0, data, {"params": params}); return data

    def _emit_metrics(self, op: str, t0: float, data: Optional[Dict[str, Any]], meta: Dict[str, Any]):
        if not self.on_metrics: return
        dur_ms = int((time.perf_counter() - t0) * 1000)
        usage = (data or {}).get("usage", {})
        payload = {
            "operation": op,
            "duration_ms": dur_ms,
            "provider": (data or {}).get("provider") or meta.get("provider"),
            "model": (data or {}).get("model") or meta.get("model"),
            "tokens": {
                "prompt": usage.get("prompt_tokens"),
                "completion": usage.get("completion_tokens"),
                "total": usage.get("total_tokens"),
            },
            "cost": usage.get("cost"),
        }
        try: self.on_metrics(payload)
        except Exception: pass

