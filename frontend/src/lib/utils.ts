import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(val?: number): string {
  if (val === undefined || val === null) return "0 TL";
  return new Intl.NumberFormat("tr-TR").format(val) + " TL";
}

export function formatKM(val?: number): string {
  if (val === undefined || val === null) return "0 KM";
  return new Intl.NumberFormat("tr-TR").format(val) + " KM";
}

export interface AngleMeta {
  key: string;
  label: string;
  shortLabel: string;
  iconName: string;
}

export function getAngleInfo(posterType: string): AngleMeta {
  switch (posterType) {
    case "instagram_post":
      return { key: "instagram_post", label: "Ana Görünüm (Ön Çapraz)", shortLabel: "Ana Açı", iconName: "Sparkles" };
    case "detail_headlight":
      return { key: "detail_headlight", label: "Ön Far & Izgara Detayı", shortLabel: "Ön Far", iconName: "Lightbulb" };
    case "rear_profile":
      return { key: "rear_profile", label: "Arka Çapraz Profil", shortLabel: "Arka Profil", iconName: "Car" };
    case "banner":
      return { key: "banner", label: "Geniş Web/Sosyal Banner (16:9)", shortLabel: "Banner", iconName: "Maximize2" };
    default:
      return { key: posterType, label: "Kreatif Afiş", shortLabel: "Afiş", iconName: "Image" };
  }
}
