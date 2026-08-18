"use client";

import React from "react";
import { RefreshCw, CheckCircle2, Globe, Cpu, Palette, Database } from "lucide-react";

interface PipelineProgressModalProps {
  isOpen: boolean;
  step: "idle" | "running" | "completed" | "error";
  summary?: string;
  onClose: () => void;
}

export function PipelineProgressModal({
  isOpen,
  step,
  summary,
  onClose,
}: PipelineProgressModalProps) {
  if (!isOpen) return null;

  const stepsList = [
    {
      title: "1. Canlı Web Scraper",
      desc: "arkasotomotiv2.com sitesinden orijinal araç fotoğrafları & teknik veriler çekiliyor",
      icon: Globe,
    },
    {
      title: "2. AI Pazarlama Ajanı",
      desc: "Marka kimliği analizi, Safe/Bold reklam metinleri ve duygusal kancalar üretiliyor",
      icon: Cpu,
    },
    {
      title: "3. 5 Açılı Afiş Motoru",
      desc: "Ön, Far, Arka, Kokpit ve 16:9 Banner afişleri Pillow grafik motoruyla render ediliyor",
      icon: Palette,
    },
    {
      title: "4. PostgreSQL Kaydı",
      desc: "SHA-256 hash doğrulamasıyla mükerrerlik olmadan veritabanı güncelleniyor",
      icon: Database,
    },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-lg overflow-hidden rounded-2xl border border-[#E6E2D8] bg-white p-6 shadow-2xl">
        
        {/* Header */}
        <div className="flex items-center gap-3 border-b border-[#F0EDE6] pb-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#F0EDE6] text-[#18181B]">
            {step === "running" ? (
              <RefreshCw className="h-5 w-5 animate-spin text-[#9C8262]" />
            ) : (
              <CheckCircle2 className="h-5 w-5 text-[#15803D]" />
            )}
          </div>
          <div>
            <h3 className="text-base font-bold text-[#18181B]">
              {step === "running" ? "AI İşlem Hattı Çalışıyor" : "İşlem Tamamlandı!"}
            </h3>
            <p className="text-xs text-[#716D65]">
              {step === "running"
                ? "Canlı Arkas kataloğu taranıyor ve afişler üretiliyor..."
                : summary || "Tüm araçlar ve çoklu açı afişleri hazırlandı."}
            </p>
          </div>
        </div>

        {/* Steps List */}
        <div className="my-5 flex flex-col gap-2.5">
          {stepsList.map((s, idx) => {
            const Icon = s.icon;
            return (
              <div
                key={idx}
                className="flex items-start gap-3 rounded-xl border border-[#E6E2D8] bg-[#F7F5F0] p-3"
              >
                <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-white text-[#716D65] border border-[#E6E2D8]">
                  <Icon className="h-3.5 w-3.5" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-[#18181B]">{s.title}</span>
                    {step === "running" ? (
                      <span className="inline-flex h-2 w-2 rounded-full bg-[#9C8262] animate-ping" />
                    ) : (
                      <CheckCircle2 className="h-3.5 w-3.5 text-[#15803D]" />
                    )}
                  </div>
                  <p className="mt-0.5 text-[11px] text-[#716D65] leading-normal">{s.desc}</p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="flex justify-end pt-2">
          <button
            onClick={onClose}
            disabled={step === "running"}
            className="rounded-xl bg-[#18181B] px-5 py-2.5 text-xs font-bold text-white shadow-xs transition hover:bg-[#27272A] disabled:opacity-40"
          >
            {step === "running" ? "Lütfen Bekleyin..." : "Vitrine Dön"}
          </button>
        </div>

      </div>
    </div>
  );
}
