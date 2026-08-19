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
  model?: string;
  body_type?: string;
  search?: string;
  min_price?: number | null;
  max_price?: number | null;
  min_km?: number | null;
  max_km?: number | null;
  fuel_type?: string;
  transmission?: string;
  feature?: string;
  is_new?: boolean;
}

export async function fetchVehicles(params: VehicleQueryParams = {}): Promise<Vehicle[]> {
  const query = new URLSearchParams();
  if (params.brand && params.brand !== "all") query.append("brand", params.brand);
  if (params.model) query.append("model", params.model);
  if (params.body_type && params.body_type !== "all") query.append("body_type", params.body_type);
  if (params.search) query.append("search", params.search);
  if (params.min_price !== undefined && params.min_price !== null) query.append("min_price", params.min_price.toString());
  if (params.max_price !== undefined && params.max_price !== null) query.append("max_price", params.max_price.toString());
  if (params.min_km !== undefined && params.min_km !== null) query.append("min_km", params.min_km.toString());
  if (params.max_km !== undefined && params.max_km !== null) query.append("max_km", params.max_km.toString());
  if (params.fuel_type) query.append("fuel_type", params.fuel_type);
  if (params.transmission) query.append("transmission", params.transmission);
  if (params.feature) query.append("feature", params.feature);
  if (params.is_new !== undefined) query.append("is_new", params.is_new.toString());

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

export async function resetChatSession(
  customerId?: number | null,
  sessionId?: string | null
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat/reset`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      customer_id: customerId || null,
      session_id: sessionId || null,
    }),
  });
  if (!res.ok) throw new Error("Sohbet sıfırlanamadı");
  return res.json();
}

export async function fetchLeads(): Promise<CustomerLead[]> {
  const res = await fetch(`${API_BASE}/api/leads`, { cache: "no-store" });
  if (!res.ok) throw new Error("Müşteri talepleri alınamadı");
  return res.json();
}
