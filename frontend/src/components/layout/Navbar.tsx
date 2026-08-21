"use client";

import React from "react";
import { Search, ShieldCheck, RefreshCw, Award, CheckCircle2 } from "lucide-react";

interface NavbarProps {
  onRefresh: () => void;
  onOpenSearchFocus: () => void;
}

export function Navbar({
  onRefresh,
  onOpenSearchFocus,
}: NavbarProps) {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[#E6E2D8] bg-[#F7F5F0]/95 backdrop-blur-xl transition-all shadow-xs">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        
        {/* Brand Logo & Showroom Title */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 items-center justify-center rounded-xl bg-[#18181B] px-4 shadow-sm">
              <span className="font-black tracking-widest text-[#F7F5F0] text-sm uppercase">AUTO AI</span>
            </div>
            <div className="hidden sm:block h-6 w-px bg-[#D5CFC2]" />
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="text-sm font-extrabold tracking-tight text-[#18181B]">SMART SHOWROOM</span>
                <span className="rounded-full bg-[#EAE6DD] px-2 py-0.5 text-[10px] font-bold text-[#716D65] border border-[#D5CFC2]">
                  DİJİTAL VİTRİN
                </span>
              </div>
              <span className="text-[11px] text-[#716D65] font-medium">
                Sertifikalı & Garantili Otomotiv Vitrini
              </span>
            </div>
          </div>
        </div>

        {/* Center Trust Badges (Visible on desktop) */}
        <div className="hidden lg:flex items-center gap-6 text-xs text-[#52525B] font-medium">
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="h-4 w-4 text-[#15803D]" />
            <span>100+ Nokta Ekspertiz</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Award className="h-4 w-4 text-[#9C8262]" />
            <span>12 Ay Kapsamlı Garanti</span>
          </div>
          <div className="flex items-center gap-1.5">
            <CheckCircle2 className="h-4 w-4 text-[#1E40AF]" />
            <span>Değerinde Takas</span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          {/* Quick Search Shortcut */}
          <button
            onClick={onOpenSearchFocus}
            className="hidden md:flex items-center gap-2.5 rounded-xl border border-[#E6E2D8] bg-white px-4 py-2.5 text-xs text-[#716D65] shadow-xs transition hover:border-[#D5CFC2] hover:text-[#18181B]"
          >
            <Search className="h-3.5 w-3.5 text-[#8E8A82]" />
            <span>Araç Ara...</span>
            <kbd className="rounded bg-[#F0EDE6] px-1.5 py-0.5 text-[10px] font-mono text-[#716D65] border border-[#E6E2D8]">⌘K</kbd>
          </button>

          {/* Refresh Showroom Data */}
          <button
            onClick={onRefresh}
            title="Vitrin Verilerini Yenile"
            className="flex h-10 w-10 items-center justify-center rounded-xl border border-[#E6E2D8] bg-white text-[#52525B] shadow-xs transition hover:bg-[#F0EDE6] hover:text-[#18181B] active:scale-95"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>

      </div>
    </header>
  );
}
