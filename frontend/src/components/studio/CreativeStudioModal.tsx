"use client";

import React, { useState } from "react";
import { Vehicle, MarketingCopy } from "@/lib/types";
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
  AlertCircle
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
  const [copyVariant, setCopyVariant] = useState<"safe" | "bold" | "story">("safe");
  const [isCopied, setIsCopied] = useState(false);

  if (!isOpen || !vehicle) return null;

  const images = vehicle.image_urls && vehicle.image_urls.length > 0
    ? vehicle.image_urls
    : [vehicle.primary_image_url || "/static/placeholder.png"];

  const currentImageUrl = images[selectedPhotoIndex] || images[0];
  const copies = vehicle.copies || [];

  const safeCopy = copies.find((c) => c.variant === "safe");
  const boldCopy = copies.find((c) => c.variant === "bold");

  const handleCopyText = (text: string) => {
    navigator.clipboard.writeText(text);
    setIsCopied(true);
    showToast("📋 Metin başarıyla panoya kopyalandı!");
    setTimeout(() => setIsCopied(false), 2000);
  };

  const getCurrentCopyText = (): string => {
    if (copyVariant === "safe" && safeCopy) {
      return `${safeCopy.headline}\n\n${safeCopy.body}\n\n${safeCopy.cta}\n\n${(safeCopy.hashtags || []).join(" ")}`;
    }
    if (copyVariant === "bold" && boldCopy) {
      return `${boldCopy.headline}\n\n${boldCopy.body}\n\n${boldCopy.cta}\n\n${(boldCopy.hashtags || []).join(" ")}`;
    }
    if (copyVariant === "story") {
      const copy = safeCopy || boldCopy;
      if (copy?.story_frames && copy.story_frames.length > 0) {
        return copy.story_frames.map((f) => `🎬 Sahne ${f.scene}:\n${f.text}`).join("\n\n────────────────\n\n");
      }
    }
    return "AI reklam metni henüz oluşturulmadı.";
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
            <img
              src={currentImageUrl}
              alt={`${vehicle.brand} ${vehicle.model}`}
              className="max-h-[440px] w-full h-full object-cover rounded-lg shadow-md transition-all"
            />

            <div className="absolute bottom-3 left-3 flex items-center gap-2 rounded-lg bg-white/90 px-3 py-1.5 text-[11px] font-semibold text-[#18181B] backdrop-blur-md border border-[#E6E2D8] shadow-xs">
              <span className="h-2 w-2 rounded-full bg-[#15803D]" />
              <span>Arkas 2. El Sertifikalı Fotoğraf</span>
            </div>
          </div>

          {/* Thumbnail Strip */}
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
                  <img src={img} alt="thumbnail" className="h-full w-full object-cover" />
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
              <ListChecks className="h-3.5 w-3.5" />
              <span>Donanımlar</span>
            </button>
          </div>

          {/* TAB 1: AI Marketing Copy */}
          {activeTab === "marketing" && (
            <div className="mt-4">
              <div className="flex items-center gap-2 mb-3">
                <button
                  onClick={() => setCopyVariant("safe")}
                  className={`flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-semibold transition-all ${
                    copyVariant === "safe"
                      ? "bg-[#F0EDE6] text-[#18181B] font-bold border border-[#D5CFC2]"
                      : "text-[#716D65] hover:text-[#18181B]"
                  }`}
                >
                  <Shield className="h-3.5 w-3.5 text-[#18181B]" />
                  <span>Dengeli & Profesyonel</span>
                </button>

                <button
                  onClick={() => setCopyVariant("bold")}
                  className={`flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-semibold transition-all ${
                    copyVariant === "bold"
                      ? "bg-[#F0EDE6] text-[#18181B] font-bold border border-[#D5CFC2]"
                      : "text-[#716D65] hover:text-[#18181B]"
                  }`}
                >
                  <Flame className="h-3.5 w-3.5 text-[#C2A676]" />
                  <span>İlgi Çekici & Cesur</span>
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
            <div className="mt-4 space-y-2.5 text-xs">
              <div className="grid grid-cols-2 gap-2.5">
                <div className="rounded-lg bg-[#F7F5F0] p-3 border border-[#E6E2D8]">
                  <span className="text-[#8E8A82] block text-[11px]">Motor & Güç</span>
                  <span className="font-bold text-[#18181B] mt-0.5 block">{vehicle.engine_power || "110 HP"} • {vehicle.engine_capacity || "999 cc"}</span>
                </div>
                <div className="rounded-lg bg-[#F7F5F0] p-3 border border-[#E6E2D8]">
                  <span className="text-[#8E8A82] block text-[11px]">Şanzıman & Çekiş</span>
                  <span className="font-bold text-[#18181B] mt-0.5 block">{vehicle.transmission || "Otomatik"} • Önden Çekiş</span>
                </div>
                <div className="rounded-lg bg-[#F7F5F0] p-3 border border-[#E6E2D8]">
                  <span className="text-[#8E8A82] block text-[11px]">Yakıt Türü</span>
                  <span className="font-bold text-[#18181B] mt-0.5 block">{vehicle.fuel_type || "Benzin"}</span>
                </div>
                <div className="rounded-lg bg-[#F7F5F0] p-3 border border-[#E6E2D8]">
                  <span className="text-[#8E8A82] block text-[11px]">Kasa Tipi & Renk</span>
                  <span className="font-bold text-[#18181B] mt-0.5 block">{vehicle.body_type || "SUV"} • {vehicle.color || "Beyaz"}</span>
                </div>
              </div>

              {vehicle.technical_specs && Object.keys(vehicle.technical_specs).length > 0 && (
                <div className="mt-3 rounded-lg border border-[#E6E2D8] bg-[#F7F5F0] p-3.5">
                  <h4 className="font-bold text-[#18181B] mb-2">Detaylı Teknik Tablo:</h4>
                  <div className="grid grid-cols-2 gap-2 text-[11px]">
                    {Object.entries(vehicle.technical_specs).map(([key, val]) => (
                      <div key={key} className="flex justify-between border-b border-[#E6E2D8] py-1">
                        <span className="text-[#716D65] capitalize">{key}:</span>
                        <span className="font-semibold text-[#18181B]">{String(val)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 3: Expertise & Damage Report */}
          {activeTab === "expertise" && (
            <div className="mt-4 space-y-3 text-xs">
              <div className="rounded-xl border border-[#D1E7DD] bg-[#F0FDF4] p-4 text-[#0F5132]">
                <div className="flex items-center gap-2 font-bold text-sm">
                  <FileCheck2 className="h-4 w-4 text-[#15803D]" />
                  <span>Arkas 2. El Güvence & Ekspertiz Durumu</span>
                </div>
                <p className="mt-2 text-xs leading-relaxed text-[#146C43]">
                  {vehicle.expertise_note || "Arkas 2. El 100+ Nokta Kontrolünden geçmiştir. Kilometre ve ekspertiz garantilidir."}
                </p>
              </div>

              {vehicle.damage_expertise && Object.keys(vehicle.damage_expertise).length > 0 ? (
                <div className="rounded-lg border border-[#E6E2D8] bg-[#F7F5F0] p-3.5">
                  <h4 className="font-bold text-[#18181B] mb-2">Hasar & Tramer Raporu:</h4>
                  <div className="space-y-1.5 text-[11px]">
                    {Object.entries(vehicle.damage_expertise).map(([part, status]) => (
                      <div key={part} className="flex justify-between border-b border-[#E6E2D8] py-1">
                        <span className="text-[#716D65]">{part}</span>
                        <span className="font-semibold text-[#18181B]">{String(status)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="flex items-center gap-2 text-xs text-[#716D65] p-3 bg-[#F7F5F0] rounded-lg border border-[#E6E2D8]">
                  <AlertCircle className="h-4 w-4 text-[#9C8262]" />
                  <span>Bu araç için değişen veya boyalı parça bilgisi bulunmamaktadır (Hatasız / Orijinal).</span>
                </div>
              )}
            </div>
          )}

          {/* TAB 4: Equipment & Features */}
          {activeTab === "features" && (
            <div className="mt-4 space-y-3 text-xs">
              <h4 className="font-bold text-[#18181B]">İlan Detaylarındaki Donanım Listesi:</h4>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {(vehicle.ad_features && vehicle.ad_features.length > 0 ? vehicle.ad_features : (vehicle.features || ["Yetkili Servis Bakımlı", "Ekspertiz Garantili", "Yedek Anahtar"]))
                  .map((feat, idx) => (
                    <div key={idx} className="flex items-center gap-1.5 rounded-lg border border-[#E6E2D8] bg-[#F7F5F0] p-2 text-[11px] font-medium text-[#18181B]">
                      <span className="h-1.5 w-1.5 rounded-full bg-[#9C8262]" />
                      <span className="truncate">{feat}</span>
                    </div>
                  ))}
              </div>
            </div>
          )}

        </div>

      </div>
    </div>
  );
}
