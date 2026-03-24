const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface LoginRequest {
  user_id: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface VoteRequest {
  user_id: string;
  proposal_id: string;
  vote_weights: number[];
  proof: string;
}

export interface Vote {
  id: number;
  user_id: string;
  proposal_id: string;
  vote_weights: number[];
  proof: string;
}

export interface KPI {
  id: number;
  region: string;
  epoch: number;
  participation_rate: number;
  accessibility_score: number;
  trust_index: number;
}

export interface Alert {
  id: number;
  epoch: number;
  msi: number;
  vei: number;
  collusion_flag: boolean;
  status: string;
}

export interface AnomalyLog {
  id: number;
  timestamp: string;
  type: string;
  description: string;
  user_id: string | null;
  severity: string;
  resolved: boolean;
}

export interface ProofRequest {
  user_id: string;
  proof_type: string;
  public_signals: string[];
  external_nullifier: string;
}

class ApiClient {
  private token: string | null = null;

  constructor() {
    if (typeof window !== "undefined") {
      this.token = localStorage.getItem("op_token");
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== "undefined") {
      localStorage.setItem("op_token", token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== "undefined") {
      localStorage.removeItem("op_token");
    }
  }

  isAuthenticated(): boolean {
    return this.token !== null;
  }

  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    const res = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers,
    });

    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: res.statusText }));
      throw new ApiError(res.status, error.detail || "Unknown error");
    }

    return res.json();
  }

  // --- Auth ---
  async login(data: LoginRequest): Promise<LoginResponse> {
    const resp = await this.request<LoginResponse>("/api/identity/login", {
      method: "POST",
      body: JSON.stringify(data),
    });
    this.setToken(resp.access_token);
    return resp;
  }

  logout() {
    this.clearToken();
  }

  // --- Governance ---
  async submitVote(data: VoteRequest): Promise<Vote> {
    return this.request<Vote>("/api/governance/vote", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getVotes(params?: Record<string, string>): Promise<Vote[]> {
    const query = params ? "?" + new URLSearchParams(params).toString() : "";
    return this.request<Vote[]>(`/api/governance/votes${query}`);
  }

  // --- Reporting ---
  async getKPIs(region?: string): Promise<KPI[]> {
    const query = region ? `?region=${encodeURIComponent(region)}` : "";
    return this.request<KPI[]>(`/api/reporting/kpis${query}`);
  }

  // --- Tokenomics ---
  async getAlerts(): Promise<Alert[]> {
    return this.request<Alert[]>("/api/tokenomics/alerts");
  }

  // --- Anomaly ---
  async getAnomalies(): Promise<AnomalyLog[]> {
    return this.request<AnomalyLog[]>("/api/anomaly/anomalies");
  }

  // --- Identity ---
  async submitProofRequest(data: ProofRequest) {
    return this.request("/api/identity/proof-request", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  // --- Health ---
  async healthCheck() {
    return this.request<{ name: string; version: string; status: string }>("/");
  }

  // --- Dev ---
  async seedDemoData() {
    return this.request<{ detail: string; seeded: boolean; counts?: Record<string, number> }>(
      "/api/dev/seed",
      { method: "POST" }
    );
  }
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export const api = new ApiClient();
