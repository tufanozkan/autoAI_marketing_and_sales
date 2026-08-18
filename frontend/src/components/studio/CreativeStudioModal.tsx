"use client";

import React, { useState } from "react";
import { Vehicle, Poster, MarketingCopy } from "@/lib/types";
import { formatCurrency, formatKM, getAngleInfo } from "@/lib/utils";
import {
  X,
  Download,
  Copy,
  Check,
  Sparkles,
  Shield,
  Flame,
  Film,
  RefreshCw,
  Layers,
  Fuel,
  Settings,
  Tag,
} from "lucide-react";
import { regenerateSingleVehicleCreative } from "@/lib/api";

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
  onVehicleUpdated,
  showToast,
}: CreativeStudioModalProps) {
  const [selectedAngleIndex, setSelectedAngleIndex] = useState(0);
  const [copyTab, setCopyTab] = useState<"safe" | "bold" | "story">("safe");
  const [isCopied, setIsCopied] = useState(false);
  const [isRegenerating, setIsRegenerating] = useState(false);

  if (!isOpen || !vehicle) return null;

  const posters = vehicle.posters || [];
  const copies = vehicle.copies || [];
  const currentPoster: Poster | undefined = posters[selectedAngleIndex] || posters[0];
  const imageUrl = currentPoster?.file_url || vehicle.primary_image_url || "/static/placeholder.png";

  const safeCopy = copies.find((c) => c.variant === "safe");
  const boldCopy = copies.find((c) => c.variant === "bold");

  const handleCopyText = (text: string) => {
    navigator.clipboard.writeText(text);
    setIsCopied(true);
    showToast("📋 Reklam metni panoya kopyalandı!");
    setTimeout(() => setIsCopied(false), 2000);
  };

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = imageUrl;
    link.download = `${vehicle.brand}_${vehicle.model}_${currentPoster?.poster_type || "afis"}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast("📥 Afiş başarıyla indirildi.");
  };

  const handleRegenerate = async () => {
    setIsRegenerating(true);
    showToast("⚡ AI yeni metinler ve afişler üretiyor...");
    try {
      const res = await regenerateSingleVehicleCreative(vehicle.id);
      if (res.status === "success") {
        showToast("✨ Yeni kreatifler ve çoklu açı afişleri başarıyla üretildi!");
        const updatedVehicle: Vehicle = {
          ...vehicle,
          posters: res.posters || vehicle.posters,
        };
        onVehicleUpdated(updatedVehicle);
      }
    } catch (err) {
      showToast("❌ Yeniden üretim sırasında bir hata oluştu.");
    } finally {
      setIsRegenerating(false);
    }
  };

  const getCurrentCopyText = (): string => {
    if (copyTab === "safe" && safeCopy) {
      return `${safeCopy.headline}\n\n${safeCopy.body}\n\n${safeCopy.cta}\n\n${(safeCopy.hashtags || []).join(" ")}`;
    }
    if (copyTab === "bold" && boldCopy) {
      return `${boldCopy.headline}\n\n${boldCopy.body}\n\n${boldCopy.cta}\n\n${(boldCopy.hashtags || []).join(" ")}`;
    }
    if (copyTab === "story") {
      const copy = safeCopy || boldCopy;
      if (copy?.story_frames && copy.story_frames.length > 0) {
        return copy.story_frames.map((f) => `🎬 Sahne ${f.scene}:\n${f.text}`).join("\n\n────────────────\n\n");
      }
    }
    return "Reklam metni henüz hazırlanmadı.";
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-3 sm:p-6 backdrop-blur-md animate-in fade-in duration-200">
      
      {/* Modal Card */}
      <div className="relative flex max-h-[92vh] w-full max-w-6xl flex-col overflow-hidden rounded-2xl border border-[#E6E2D8] bg-white shadow-2xl lg:flex-row">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-20 flex h-9 w-9 items-center justify-center rounded-full bg-[#F0EDE6] text-[#52525B] transition hover:bg-[#18181B] hover:text-white"
        >
          <X className="h-4 w-4" />
        </button>

        {/* LEFT COLUMN: Visual Multi-Angle Studio */}
        <div className="flex flex-1 flex-col border-b border-[#E6E2D8] bg-[#F7F5F0] p-5 sm:p-7 lg:w-[48%] lg:border-b-0 lg:border-r">
          
          {/* Angle Selector Tabs */}
          <div className="mb-4">
            <div className="mb-2 flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-[#716D65]">
                Afiş Açıları ({posters.length})
              </span>
              <span className="text-[11px] text-[#8E8A82] font-medium">
                {currentPoster?.poster_type === "banner" ? "1200x630 Banner" : "1080x1350 4:5 Post"}
              </span>
            </div>

            <div className="flex flex-wrap gap-1.5">
              {posters.map((poster, idx) => {
                const info = getAngleInfo(poster.poster_type);
                const isActive = idx === selectedAngleIndex;
                return (
                  <button
                    key={poster.id || idx}
                    onClick={() => setSelectedAngleIndex(idx)}
                    className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
                      isActive
                        ? "bg-[#18181B] text-white shadow-xs"
                        : "border border-[#E6E2D8] bg-white text-[#52525B] hover:border-[#D5CFC2] hover:bg-[#F0EDE6]"
                    }`}
                  >
                    <Layers className="h-3 w-3" />
                    <span>{info.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* High-Resolution Poster Image Display */}
          <div className="relative flex flex-1 items-center justify-center overflow-hidden rounded-xl bg-[#EBE7DE] border border-[#E6E2D8] p-2 min-h-[300px] lg:min-h-[440px]">
            <img
              src={imageUrl}
              alt={`${vehicle.brand} ${vehicle.model}`}
              className="max-h-[500px] w-auto rounded-lg object-contain shadow-lg transition-all"
            />

            {/* Poster Info Pill */}
            <div className="absolute bottom-4 left-4 flex items-center gap-2 rounded-lg bg-white/90 px-3 py-1.5 text-[11px] font-semibold text-[#18181B] backdrop-blur-md border border-[#E6E2D8] shadow-xs">
              <span className="h-2 w-2 rounded-full bg-[#15803D] animate-pulse" />
              <span>Yüksek Çözünürlük Render</span>
            </div>
          </div>

          {/* Direct Download Action */}
          <div className="mt-4 flex items-center gap-2.5">
            <button
              onClick={handleDownload}
              className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-[#18181B] py-3 text-xs font-bold text-white shadow-sm transition hover:bg-[#27272A] active:scale-98"
            >
              <Download className="h-4 w-4" />
              <span>Seçili Afişi İndir (HD PNG)</span>
            </button>
          </div>

        </div>

        {/* RIGHT COLUMN: AI Copywriting & Marketing Studio */}
        <div className="flex flex-1 flex-col overflow-y-auto p-5 sm:p-7 lg:w-[52%] max-h-[85vh] bg-white">
          
          {/* Vehicle Metadata Header */}
          <div className="border-b border-[#F0EDE6] pb-4">
            <div className="flex items-center gap-2">
              <span className="rounded bg-[#F0EDE6] px-2 py-0.5 text-xs font-extrabold uppercase tracking-wider text-[#18181B]">
                {vehicle.brand}
              </span>
              <span className="text-xs font-semibold text-[#716D65]">
                {vehicle.year} Model • {formatKM(vehicle.km)}
              </span>
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

            {/* AI Emotional Strategy Brief Pill */}
            {vehicle.brief && (
              <div className="mt-3.5 rounded-lg border border-[#E8DFC8] bg-[#FDFBF7] p-3 text-xs text-[#78613A]">
                <div className="flex items-center gap-1.5 font-bold">
                  <Sparkles className="h-3.5 w-3.5 text-[#9C8262]" />
                  <span>Hedef Persona & Duygusal Kanca:</span>
                </div>
                <p className="mt-1 text-[11px] text-[#78613A]/90 leading-relaxed font-normal">
                  "{vehicle.brief.emotional_hook}" ({vehicle.brief.target_persona})
                </p>
              </div>
            )}
          </div>

          {/* AI Copy Tone Tabs */}
          <div className="mt-5">
            <div className="flex items-center gap-2 border-b border-[#F0EDE6] pb-2.5">
              <button
                onClick={() => setCopyTab("safe")}
                className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
                  copyTab === "safe"
                    ? "bg-[#18181B] text-white shadow-xs"
                    : "text-[#716D65] hover:text-[#18181B]"
                }`}
              >
                <Shield className="h-3.5 w-3.5" />
                <span>Kurumsal & Güvenli</span>
              </button>

              <button
                onClick={() => setCopyTab("bold")}
                className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
                  copyTab === "bold"
                    ? "bg-[#18181B] text-white shadow-xs"
                    : "text-[#716D65] hover:text-[#18181B]"
                }`}
              >
                <Flame className="h-3.5 w-3.5 text-[#C2A676]" />
                <span>Duygusal & Tutkulu</span>
              </button>

              <button
                onClick={() => setCopyTab("story")}
                className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
                  copyTab === "story"
                    ? "bg-[#18181B] text-white shadow-xs"
                    : "text-[#716D65] hover:text-[#18181B]"
                }`}
              >
                <Film className="h-3.5 w-3.5" />
                <span>Instagram Story</span>
              </button>
            </div>

            {/* Copy Content Display Box */}
            <div className="mt-3.5 relative rounded-xl border border-[#E6E2D8] bg-[#F7F5F0] p-4 text-xs leading-relaxed text-[#18181B]">
              <div className="whitespace-pre-wrap font-sans text-xs sm:text-sm text-[#18181B] selection:bg-[#18181B] selection:text-white">
                {getCurrentCopyText()}
              </div>
            </div>
          </div>

          {/* Action Footer: Copy Text & AI Regenerate */}
          <div className="mt-auto pt-6 flex items-center justify-between gap-3 border-t border-[#F0EDE6]">
            <button
              onClick={() => handleCopyText(getCurrentCopyText())}
              className="flex items-center gap-2 rounded-xl border border-[#E6E2D8] bg-[#F7F5F0] px-4 py-2.5 text-xs font-semibold text-[#18181B] transition hover:bg-[#EBE7DE] active:scale-95"
            >
              {isCopied ? (
                <>
                  <Check className="h-4 w-4 text-[#15803D]" />
                  <span className="text-[#15803D]">Kopyalandı!</span>
                </>
              ) : (
                <>
                  <Copy className="h-4 w-4 text-[#716D65]" />
                  <span>Metni Kopyala</span>
                </>
              )}
            </button>

            <button
              onClick={handleRegenerate}
              disabled={isRegenerating}
              className="flex items-center gap-2 rounded-xl border border-[#E6E2D8] bg-[#F7F5F0] px-4 py-2.5 text-xs font-semibold text-[#18181B] transition hover:bg-[#18181B] hover:text-white active:scale-95 disabled:opacity-50"
            >
              <RefreshCw className={`h-4 w-4 ${isRegenerating ? "animate-spin text-[#9C8262]" : ""}`} />
              <span>{isRegenerating ? "Üretiliyor..." : "AI Yeniden Üret"}</span>
            </button>
          </div>

        </div>

      </div>
    </div>
  );
}
