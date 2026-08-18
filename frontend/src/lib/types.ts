export interface Poster {
  id: number;
  vehicle_id: number;
  poster_type: "instagram_post" | "detail_headlight" | "rear_profile" | "banner" | string;
  file_path: string;
  file_url: string;
  headline?: string;
  subheading?: string;
  created_at: string;
}

export interface StoryFrame {
  scene: number;
  text: string;
}

export interface MarketingCopy {
  id: number;
  vehicle_id: number;
  variant: "safe" | "bold" | string;
  headline: string;
  subheading?: string;
  body: string;
  cta: string;
  hashtags: string[];
  story_frames?: StoryFrame[];
  created_at: string;
}

export interface CreativeBrief {
  id: number;
  vehicle_id: number;
  target_persona: string;
  emotional_hook: string;
  color_theme?: string;
  created_at: string;
}

export interface Vehicle {
  id: number;
  source_url?: string;
  brand: string;
  model: string;
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
  features?: string[];
  image_urls?: string[];
  primary_image_url?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  brief?: CreativeBrief | null;
  copies?: MarketingCopy[];
  posters?: Poster[];
}

export interface StatsResponse {
  total_vehicles: number;
  active_vehicles: number;
  total_posters: number;
  total_copies: number;
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
  posters_rendered: number;
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
  conversation_summary?: string;
  created_at: string;
}
