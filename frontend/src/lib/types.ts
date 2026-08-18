export interface StoryFrame {
  scene: number;
  text: string;
}

export interface MarketingCopy {
  id: number;
  vehicle_id: number;
  variant: "safe" | "bold" | string;
  headline: string;
  hook: string;
  body: string;
  cta: string;
  hashtags: string[];
  story_frames?: StoryFrame[];
  created_at: string;
}

export interface CreativeBrief {
  id: number;
  vehicle_id: number;
  brand_archetype: string;
  target_persona: string;
  emotional_points: string[];
  tone_of_voice: string;
  key_hooks: string[];
  created_at: string;
}

export interface Vehicle {
  id: number;
  external_id?: string;
  source?: string;
  url?: string;
  brand: string;
  model: string;
  package?: string;
  sub_model?: string;
  year: number;
  km: number;
  price: number;
  currency: string;
  body_type?: string;
  fuel_type?: string;
  transmission?: string;
  color?: string;
  engine_power?: string;
  engine_capacity?: string;
  technical_specs?: Record<string, any>;
  ad_features?: string[];
  features?: string[];
  damage_expertise?: Record<string, any>;
  expertise_note?: string;
  image_urls?: string[];
  primary_image_url?: string;
  is_active: boolean;
  created_at: string;
  brief?: CreativeBrief | null;
  copies?: MarketingCopy[];
}

export interface StatsResponse {
  total_vehicles: number;
  active_vehicles: number;
  total_copies: number;
  total_leads: number;
  brands: Array<{ brand: string; count: number }>;
}

export interface PipelineResult {
  status: string;
  scrape_stats: {
    total: number;
    new: number;
    updated: number;
    skipped: number;
  };
  copies_generated: number;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

export interface FilterAction {
  brand?: string;
  body_type?: string;
  max_price?: number;
  search?: string;
}

export interface ChatResponse {
  reply: string;
  customer_id: number;
  customer_name?: string;
  filter_action?: FilterAction | null;
  matched_vehicles?: Vehicle[];
}

export interface CustomerLead {
  id: number;
  first_name?: string;
  last_name?: string;
  full_name?: string;
  phone?: string;
  interested_brand?: string;
  interested_model?: string;
  interested_body_type?: string;
  budget_max?: number;
  focused_vehicle_id?: number;
  conversation_summary?: string;
  created_at: string;
}
