"use client";

import React, { useState } from "react";
import { Vehicle } from "@/lib/types";
import { formatCurrency, formatKM } from "@/lib/utils";
import {
  X,
  Copy,
  Check,
  Sparkles,
  Shield,
  Flame,
  Film,
  Layers,
  Fuel,
  Settings,
  Tag,
  Gauge,
  FileCheck2,
  ListChecks,
  AlertCircle,
  Armchair,
  Smartphone,
  Sparkle,
  Briefcase
} from "lucide-react";

interface CreativeStudioModalProps {
  vehicle: Vehicle | null;
  isOpen: boolean;
  onClose: () => void;
  onVehicleUpdated: (updated: Vehicle) => void;
  showToast: (msg: string) => void;
}

export function CreativeStudioModal({
  vehicle,
  isOpen,
  onClose,
  showToast,
}: CreativeStudioModalProps) {
  const [selectedPhotoIndex, setSelectedPhotoIndex] = useState(0);
  const [activeTab, setActiveTab] = useState<"marketing" | "tech" | "expertise" | "features">("marketing");
  const [copyVariant, setCopyVariant] = useState<"balanced" | "professional" | "engaging" | "story">("balanced");
  const [isCopied, setIsCopied] = useState(false);

  if (!isOpen || !vehicle) return null;

  const images = vehicle.image_urls && vehicle.image_urls.length > 0
    ? vehicle.image_urls
    : (vehicle.images && vehicle.images.length > 0
        ? vehicle.images.map(img => img.image_url)
        : [vehicle.primary_image_url || "/placeholder.svg"]);

  const currentImageUrl = images[selectedPhotoIndex] || images[0];
  const brief = vehicle.brief;

  const handleCopyText = (text: string) => {
    navigator.clipboard.writeText(text);
    setIsCopied(true);
    showToast("📋 Metin başarıyla panoya kopyalandı!");
    setTimeout(() => setIsCopied(false), 2000);
  };

  const getCurrentCopyText = (): string => {
    if (!brief) return "AI reklam metni henüz oluşturulmadı.";

    if (copyVariant === "balanced") {
      return brief.balanced_copy || "Dengeli reklam metni bulunamadı.";
    }
    if (copyVariant === "professional") {
      return brief.professional_copy || "Kurumsal reklam metni bulunamadı.";
    }
    if (copyVariant === "engaging") {
      return brief.engaging_copy || "İlgi çekici reklam metni bulunamadı.";
    }
    if (copyVariant === "story") {
      if (brief.story_frames && brief.story_frames.length > 0) {
        return brief.story_frames.map((f) => `🎬 Sahne ${f.scene}:\n${f.text}`).join("\n\n────────────────\n\n");
      }
    }
    return "Reklam metni hazır değil.";
  };

  // Helper to extract ad features whether object or array
  const renderAdFeatures = () => {
    const rawFeatures = vehicle.ad_features || vehicle.features;

    if (!rawFeatures) {
      return (
        <div className="p-3 text-xs text-[#716D65] bg-[#F7F5F0] rounded-lg border border-[#E6E2D8]">
          Donanım bilgisi belirtilmemiş.
        </div>
      );
    }

    // If it's a categorized dictionary: { konfor: [...], guvenlik: [...], multimedya: [...] }
    if (typeof rawFeatures === "object" && !Array.isArray(rawFeatures)) {
      const categoryTitles: Record<string, { label: string; icon: any }> = {
        konfor: { label: "Konfor & Kolaylık", icon: Armchair },
        guvenlik: { label: "Güvenlik & Sürüş Asistanları", icon: Shield },
        multimedya: { label: "Multimedya & Eğlence", icon: Smartphone },
        ic_donanim: { label: "İç Donanım & Tasarım", icon: Sparkles },
        dis_donanim: { label: "Dış Donanım & Işıklandırma", icon: Sparkle },
      };

      const entries = Object.entries(rawFeatures).filter(([_, items]) => Array.isArray(items) && items.length > 0);

      if (entries.length === 0) {
        return (
          <div className="p-3 text-xs text-[#716D65] bg-[#F7F5F0] rounded-lg border border-[#E6E2D8]">
            Detaylı donanım listesi bulunamadı.
          </div>
        );
      }

      return (
        <div className="space-y-4">
          {entries.map(([catKey, items]) => {
            const catMeta = categoryTitles[catKey] || { label: catKey.toUpperCase(), icon: ListChecks };
            const Icon = catMeta.icon;
            return (
              <div key={catKey} className="rounded-xl border border-[#E6E2D8] bg-[#F7F5F0] p-3.5">
                <div className="flex items-center gap-2 font-bold text-xs text-[#18181B] mb-2.5 pb-1.5 border-b border-[#E6E2D8]">
                  <Icon className="h-3.5 w-3.5 text-[#9C8262]" />
                  <span>{catMeta.label} ({items.length})</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {items.map((feat: string, idx: number) => (
                    <div key={idx} className="flex items-center gap-2 rounded-lg bg-white p-2 text-[11px] font-medium text-[#18181B] border border-[#E6E2D8]/60 shadow-2xs">
                      <span className="h-1.5 w-1.5 rounded-full bg-[#15803D] shrink-0" />
                      <span className="truncate">{feat}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      );
    }

    // If it's a flat array of strings
    if (Array.isArray(rawFeatures)) {
      return (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
          {rawFeatures.map((feat, idx) => (
            <div key={idx} className="flex items-center gap-1.5 rounded-lg border border-[#E6E2D8] bg-[#F7F5F0] p-2 text-[11px] font-medium text-[#18181B]">
              <span className="h-1.5 w-1.5 rounded-full bg-[#9C8262]" />
              <span className="truncate">{String(feat)}</span>
            </div>
          ))}
        </div>
      );
    }

    return null;
  };

  // Helper to extract damage / expertise info
  const renderDamageExpertise = () => {
    const damage = vehicle.damage_expertise || {};
    const boyali = Array.isArray(damage.boyali_parcalar) ? damage.boyali_parcalar : [];
    const degisen = Array.isArray(damage.degisen_parcalar) ? damage.degisen_parcalar : [];
    const tramer = typeof damage.tramer_kaydi_tl === "number" ? damage.tramer_kaydi_tl : 0;

    const isFlawless = boyali.length === 0 && degisen.length === 0 && tramer === 0;

    return (
      <div className="space-y-3.5">
        <div className="rounded-xl border border-[#D1E7DD] bg-[#F0FDF4] p-4 text-[#0F5132]">
          <div className="flex items-center gap-2 font-bold text-sm">
            <FileCheck2 className="h-4 w-4 text-[#15803D]" />
            <span>Arkas Spoticar 100+ Nokta Kontrolü ve Garanti</span>
          </div>
          <p className="mt-2 text-xs leading-relaxed text-[#146C43]">
            {vehicle.expertise_note || "Arkas Spoticar 100+ Nokta Kontrolünden geçmiştir. Kilometre ve mekanik garantisi altındadır."}
          </p>
        </div>

        {isFlawless ? (
          <div className="flex items-center gap-2.5 rounded-xl border border-[#B8E2C8] bg-[#E8F8F0] p-4 text-xs font-bold text-[#0F5132]">
            <Check className="h-5 w-5 text-[#15803D]" />
            <span>Bu araç tamamen HATASIZ, BOYASIZ ve DEĞİŞENSİZDİR. (Tramer Kaydı: 0 TL)</span>
          </div>
        ) : (
          <div className="rounded-xl border border-[#E6E2D8] bg-[#F7F5F0] p-4 space-y-2.5">
            <h4 className="font-bold text-xs text-[#18181B] pb-1 border-b border-[#E6E2D8]">Hasar ve Ekspertiz Raporu:</h4>
            
            <div className="flex justify-between text-xs py-1 border-b border-[#E6E2D8]/60">
              <span className="text-[#716D65]">Boyalı Parçalar:</span>
              <span className="font-semibold text-[#18181B] text-right">
                {boyali.length > 0 ? boyali.join(", ") : "Yok (Boyasız)"}
              </span>
            </div>

            <div className="flex justify-between text-xs py-1 border-b border-[#E6E2D8]/60">
              <span className="text-[#716D65]">Değişen Parçalar:</span>
              <span className="font-semibold text-[#18181B] text-right">
                {degisen.length > 0 ? degisen.join(", ") : "Yok (Değişensiz)"}
              </span>
            </div>

            <div className="flex justify-between text-xs py-1">
              <span className="text-[#716D65]">Tramer Hasar Kaydı:</span>
              <span className="font-bold text-[#18181B]">
                {tramer > 0 ? `${tramer.toLocaleString("tr-TR")} TL` : "0 TL (Kayıt Yok)"}
              </span>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-3 sm:p-6 backdrop-blur-md animate-in fade-in duration-200">
      
      {/* Modal Container */}
      <div className="relative flex max-h-[92vh] w-full max-w-6xl flex-col overflow-hidden rounded-2xl border border-[#E6E2D8] bg-white shadow-2xl lg:flex-row">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-20 flex h-9 w-9 items-center justify-center rounded-full bg-[#F0EDE6] text-[#52525B] transition hover:bg-[#18181B] hover:text-white"
        >
          <X className="h-4 w-4" />
        </button>

        {/* LEFT COLUMN: Genuine Vehicle Photo Gallery */}
        <div className="flex flex-1 flex-col border-b border-[#E6E2D8] bg-[#F7F5F0] p-5 sm:p-7 lg:w-[48%] lg:border-b-0 lg:border-r">
          
          <div className="mb-3 flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-[#716D65] flex items-center gap-1.5">
              <Layers className="h-3.5 w-3.5 text-[#9C8262]" />
              <span>Orijinal Araç Galerisi ({images.length})</span>
            </span>
            <span className="text-[11px] text-[#8E8A82] font-medium">
              Fotoğraf {selectedPhotoIndex + 1} / {images.length}
            </span>
          </div>

          {/* Large Main Photo Display */}
          <div className="relative flex flex-1 items-center justify-center overflow-hidden rounded-xl bg-[#EBE7DE] border border-[#E6E2D8] min-h-[280px] lg:min-h-[420px]">
            {vehicle.primary_image_url ? (
              <>
                <img
                  src={currentImageUrl}
                  alt={`${vehicle.brand} ${vehicle.model}`}
                  referrerPolicy="no-referrer"
                  className="max-h-[440px] w-full h-full object-cover rounded-lg shadow-md transition-all"
                />

                <div className="absolute bottom-3 left-3 flex items-center gap-2 rounded-lg bg-white/90 px-3 py-1.5 text-[11px] font-semibold text-[#18181B] backdrop-blur-md border border-[#E6E2D8] shadow-xs">
                  <span className="h-2 w-2 rounded-full bg-[#15803D]" />
                  <span>Arkas Spoticar Sertifikalı Fotoğraf</span>
                </div>
              </>
            ) : (
              <div className="flex h-full w-full flex-col items-center justify-center bg-[#EAE6DD] p-8 text-center">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[#DCD6C9] text-[#716D65] mb-3">
                  <Layers className="h-8 w-8 text-[#8E8A82]" />
                </div>
                <h4 className="text-sm font-extrabold text-[#18181B]">
                  Bu aracın görseli bulunmamaktadır
                </h4>
                <p className="mt-1.5 max-w-xs text-xs text-[#716D65] leading-relaxed">
                  Arkas Spoticar 100+ Nokta Kontrolünden geçmiş olup detaylı teknik ve ekspertiz bilgileri sağ tarafta yer almaktadır.
                </p>
              </div>
            )}
          </div>

          {/* Thumbnail Strip (ul.classifiedDetailThumbList / image_0, image_1...) */}
          {images.length > 1 && (
            <div className="mt-3.5 flex gap-2 overflow-x-auto pb-1">
              {images.map((img, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedPhotoIndex(idx)}
                  className={`relative h-14 w-20 shrink-0 overflow-hidden rounded-lg border-2 transition-all ${
                    idx === selectedPhotoIndex
                      ? "border-[#18181B] shadow-sm scale-105"
                      : "border-transparent opacity-70 hover:opacity-100"
                  }`}
                >
                  <img
                    src={img}
                    alt={`image_${idx}`}
                    referrerPolicy="no-referrer"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=300&q=80";
                    }}
                    className="h-full w-full object-cover"
                  />
                </button>
              ))}
            </div>
          )}

        </div>

        {/* RIGHT COLUMN: AI Copywriting & Detailed Vehicle Specs */}
        <div className="flex flex-1 flex-col overflow-y-auto p-5 sm:p-7 lg:w-[52%] max-h-[85vh] bg-white">
          
          {/* Header Info */}
          <div className="border-b border-[#F0EDE6] pb-4">
            <div className="flex items-center gap-2">
              <span className="rounded bg-[#F0EDE6] px-2 py-0.5 text-xs font-extrabold uppercase tracking-wider text-[#18181B]">
                {vehicle.brand}
              </span>
              <span className="text-xs font-semibold text-[#716D65]">
                {vehicle.year} Model • {formatKM(vehicle.km)}
              </span>
              {vehicle.package && (
                <span className="rounded bg-[#F0EDE6] px-2 py-0.5 text-xs font-bold text-[#9C8262]">
                  {vehicle.package}
                </span>
              )}
            </div>

            <h2 className="mt-2 text-xl sm:text-2xl font-black text-[#18181B]">
              {vehicle.model} {vehicle.sub_model || ""}
            </h2>

            <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-[#716D65]">
              <span className="flex items-center gap-1">
                <Fuel className="h-3.5 w-3.5 text-[#8E8A82]" /> {vehicle.fuel_type || "Benzin"}
              </span>
              <span className="flex items-center gap-1">
                <Settings className="h-3.5 w-3.5 text-[#8E8A82]" /> {vehicle.transmission || "Otomatik"}
              </span>
              {vehicle.color && (
                <span className="flex items-center gap-1">
                  <Tag className="h-3.5 w-3.5 text-[#8E8A82]" /> {vehicle.color}
                </span>
              )}
              <span className="text-sm font-extrabold text-[#18181B] sm:ml-auto">
                {formatCurrency(vehicle.price)}
              </span>
            </div>

            {/* AI Strategy Brief */}
            {vehicle.brief && (
              <div className="mt-3.5 rounded-lg border border-[#E8DFC8] bg-[#FDFBF7] p-3 text-xs text-[#78613A]">
                <div className="flex items-center gap-1.5 font-bold">
                  <Sparkles className="h-3.5 w-3.5 text-[#9C8262]" />
                  <span>Hedef Persona & Duygusal Kanca:</span>
                </div>
                <p className="mt-1 text-[11px] text-[#78613A]/90 leading-relaxed font-normal">
                  "{vehicle.brief.emotional_points?.[0] || vehicle.brief.target_persona}" ({vehicle.brief.target_persona})
                </p>
              </div>
            )}
          </div>

          {/* Navigation Tabs (AI Metinler / Teknik / Ekspertiz / Donanım) */}
          <div className="mt-4 flex items-center gap-1 border-b border-[#F0EDE6] pb-2">
            <button
              onClick={() => setActiveTab("marketing")}
              className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
                activeTab === "marketing"
                  ? "bg-[#18181B] text-white shadow-xs"
                  : "text-[#716D65] hover:text-[#18181B]"
              }`}
            >
              <Sparkles className="h-3.5 w-3.5 text-[#C2A676]" />
              <span>AI Reklam Metinleri</span>
            </button>

            <button
              onClick={() => setActiveTab("tech")}
              className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
                activeTab === "tech"
                  ? "bg-[#18181B] text-white shadow-xs"
                  : "text-[#716D65] hover:text-[#18181B]"
              }`}
            >
              <Gauge className="h-3.5 w-3.5" />
              <span>Teknik Özellikler</span>
            </button>

            <button
              onClick={() => setActiveTab("expertise")}
              className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
                activeTab === "expertise"
                  ? "bg-[#18181B] text-white shadow-xs"
                  : "text-[#716D65] hover:text-[#18181B]"
              }`}
            >
              <FileCheck2 className="h-3.5 w-3.5 text-[#15803D]" />
              <span>Ekspertiz Durumu</span>
            </button>

            <button
              onClick={() => setActiveTab("features")}
              className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
                activeTab === "features"
                  ? "bg-[#18181B] text-white shadow-xs"
                  : "text-[#716D65] hover:text-[#18181B]"
              }`}
            >
              <ListChecks className="h-3.5 w-3.5 text-[#9C8262]" />
              <span>Donanımlar</span>
            </button>
          </div>

          {/* TAB 1: AI Marketing Copy */}
          {activeTab === "marketing" && (
            <div className="mt-4">
              <div className="flex flex-wrap items-center gap-2 mb-3">
                <button
                  onClick={() => setCopyVariant("balanced")}
                  className={`flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-semibold transition-all ${
                    copyVariant === "balanced"
                      ? "bg-[#F0EDE6] text-[#18181B] font-bold border border-[#D5CFC2]"
                      : "text-[#716D65] hover:text-[#18181B]"
                  }`}
                >
                  <Shield className="h-3.5 w-3.5 text-[#18181B]" />
                  <span>Dengeli & Şeffaf</span>
                </button>

                <button
                  onClick={() => setCopyVariant("professional")}
                  className={`flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-semibold transition-all ${
                    copyVariant === "professional"
                      ? "bg-[#F0EDE6] text-[#18181B] font-bold border border-[#D5CFC2]"
                      : "text-[#716D65] hover:text-[#18181B]"
                  }`}
                >
                  <Briefcase className="h-3.5 w-3.5 text-[#18181B]" />
                  <span>Kurumsal & Profesyonel</span>
                </button>

                <button
                  onClick={() => setCopyVariant("engaging")}
                  className={`flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-semibold transition-all ${
                    copyVariant === "engaging"
                      ? "bg-[#F0EDE6] text-[#18181B] font-bold border border-[#D5CFC2]"
                      : "text-[#716D65] hover:text-[#18181B]"
                  }`}
                >
                  <Flame className="h-3.5 w-3.5 text-[#C2A676]" />
                  <span>İlgi Çekici & Enerjik</span>
                </button>

                <button
                  onClick={() => setCopyVariant("story")}
                  className={`flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-semibold transition-all ${
                    copyVariant === "story"
                      ? "bg-[#F0EDE6] text-[#18181B] font-bold border border-[#D5CFC2]"
                      : "text-[#716D65] hover:text-[#18181B]"
                  }`}
                >
                  <Film className="h-3.5 w-3.5" />
                  <span>Story Akışı</span>
                </button>
              </div>

              <div className="relative rounded-xl border border-[#E6E2D8] bg-[#F7F5F0] p-4 text-xs leading-relaxed text-[#18181B]">
                <div className="whitespace-pre-wrap font-sans text-xs sm:text-sm text-[#18181B] selection:bg-[#18181B] selection:text-white">
                  {getCurrentCopyText()}
                </div>
              </div>

              <div className="mt-4 flex justify-end">
                <button
                  onClick={() => handleCopyText(getCurrentCopyText())}
                  className="flex items-center gap-2 rounded-xl bg-[#18181B] px-4 py-2.5 text-xs font-semibold text-white shadow-xs transition hover:bg-[#27272A] active:scale-95"
                >
                  {isCopied ? (
                    <>
                      <Check className="h-4 w-4 text-[#4ADE80]" />
                      <span>Kopyalandı!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="h-4 w-4" />
                      <span>Metni Kopyala</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {/* TAB 2: Technical Specifications */}
          {activeTab === "tech" && (
            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {Object.entries(vehicle.technical_specs || {}).map(([key, val]) => (
                <div key={key} className="flex flex-col rounded-lg border border-[#E6E2D8] bg-[#F7F5F0] p-3 text-xs">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-[#716D65]">
                    {key.replace(/_/g, " ")}
                  </span>
                  <span className="mt-1 font-bold text-[#18181B]">{String(val)}</span>
                </div>
              ))}
            </div>
          )}

          {/* TAB 3: Damage & Expertise Report */}
          {activeTab === "expertise" && (
            <div className="mt-4">
              {renderDamageExpertise()}
            </div>
          )}

          {/* TAB 4: Categorized Features */}
          {activeTab === "features" && (
            <div className="mt-4">
              {renderAdFeatures()}
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
