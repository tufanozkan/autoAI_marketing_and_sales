import { Vehicle, StatsResponse, PipelineResult, ChatResponse, CustomerLead } from "./types";

const API_BASE = ""; // Relative path leverages Next.js rewrites or same-origin

export async function fetchStats(): Promise<StatsResponse> {
  const res = await fetch(`${API_BASE}/api/stats`, { cache: "no-store" });
  if (!res.ok) throw new Error("İstatistikler alınamadı");
  return res.json();
}

export async function fetchBrands(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/api/brands`, { cache: "no-store" });
  if (!res.ok) throw new Error("Markalar alınamadı");
  return res.json();
}

export interface VehicleQueryParams {
  brand?: string;
  body_type?: string;
  search?: string;
  min_price?: number;
  max_price?: number;
}

export async function fetchVehicles(params: VehicleQueryParams = {}): Promise<Vehicle[]> {
  const query = new URLSearchParams();
  if (params.brand && params.brand !== "all") query.append("brand", params.brand);
  if (params.body_type && params.body_type !== "all") query.append("body_type", params.body_type);
  if (params.search) query.append("search", params.search);
  if (params.min_price !== undefined && params.min_price !== null) query.append("min_price", params.min_price.toString());
  if (params.max_price !== undefined && params.max_price !== null) query.append("max_price", params.max_price.toString());

  const res = await fetch(`${API_BASE}/api/vehicles?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Araçlar yüklenemedi");
  return res.json();
}

export async function fetchVehicleDetail(id: number): Promise<Vehicle> {
  const res = await fetch(`${API_BASE}/api/vehicles/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Araç detayları alınamadı");
  return res.json();
}

export async function runFullPipeline(): Promise<PipelineResult> {
  const res = await fetch(`${API_BASE}/api/pipeline/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error("Pipeline çalıştırılırken bir hata oluştu");
  return res.json();
}

export async function regenerateSingleVehicleCreative(id: number): Promise<{
  status: string;
  vehicle_id: number;
  copies_count: number;
  posters: any[];
}> {
  const res = await fetch(`${API_BASE}/api/pipeline/generate-single/${id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error("Araç kreatifleri yeniden üretilemedi");
  return res.json();
}

export async function sendChatMessage(
  message: string,
  customerId?: number | null,
  sessionId?: string | null
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      customer_id: customerId || null,
      session_id: sessionId || null,
    }),
  });
  if (!res.ok) throw new Error("Mesaj gönderilemedi");
  return res.json();
}

export async function fetchLeads(): Promise<CustomerLead[]> {
  const res = await fetch(`${API_BASE}/api/leads`, { cache: "no-store" });
  if (!res.ok) throw new Error("Müşteri talepleri alınamadı");
  return res.json();
}
