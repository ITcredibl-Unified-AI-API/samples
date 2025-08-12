import axios, { AxiosInstance } from "axios";

export type Provider = "openai" | "anthropic" | "google" | "groq" | "bedrock";

export interface Config {
  apiKey: string;
  baseURL?: string;
  timeoutMs?: number;
  defaultProvider?: Provider;
}

export interface Message {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface ChatRequest {
  model?: string;
  messages: Message[];
  provider?: Provider;
  temperature?: number;
  max_tokens?: number;
  stream?: boolean;
  [key: string]: any;
}

export interface ChoiceDelta {
  delta?: { content?: string };
  message?: { role: string; content: string };
}

export interface ChatResponse {
  id?: string;
  choices: ChoiceDelta[];
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
    cost?: number;
  };
  provider?: Provider;
  model?: string;
}

export class AIGatewaySDK {
  private http: AxiosInstance;
  private cfg: Required<Config>;

  constructor(cfg: Config) {
    this.cfg = {
      baseURL: cfg.baseURL ?? process.env.ITCREDIBL_API_URL ?? "https://api.itcredibl.com/functions/v1/itcredibl-api",
      timeoutMs: cfg.timeoutMs ?? 60000,
      defaultProvider: cfg.defaultProvider ?? "openai",
      apiKey: cfg.apiKey,
    };
    this.http = axios.create({
      baseURL: this.cfg.baseURL,
      timeout: this.cfg.timeoutMs,
      headers: {
        Authorization: `Bearer ${this.cfg.apiKey}`,
        "Content-Type": "application/json",
        "User-Agent": "itcredibl-ts-enterprise/1.0"
      },
    });
  }

  async chatCompletion(req: ChatRequest): Promise<ChatResponse> {
    const payload = {
      ...req,
      provider: req.provider ?? this.cfg.defaultProvider,
      stream: false,
    };
    const { data } = await this.http.post("", payload);
    return data;
  }

  async streamChatCompletion(
    req: ChatRequest,
    onDelta: (delta: ChoiceDelta) => void
  ): Promise<void> {
    const payload = { ...req, provider: req.provider ?? this.cfg.defaultProvider, stream: true };
    const res = await fetch(this.cfg.baseURL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.cfg.apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok || !res.body) {
      throw new Error(`Streaming failed with status ${res.status}`);
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value);
      for (const line of chunk.split("\\n")) {
        const trimmed = line.trim();
        if (!trimmed.startsWith("data:")) continue;
        const jsonStr = trimmed.slice(5).trim();
        if (jsonStr.toLowerCase() === "[done]") return;
        try {
          const obj = JSON.parse(jsonStr);
          onDelta(obj);
        } catch {
          // ignore
        }
      }
    }
  }
}

export default AIGatewaySDK;