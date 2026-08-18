"use client";

import React from "react";
import { Sparkles, RefreshCw, Zap, Search, ShieldCheck, Compass } from "lucide-react";

interface NavbarProps {
  onRunPipeline: () => void;
  onRefresh: () => void;
  isRunningPipeline: boolean;
  onOpenSearchFocus: () => void;
}

export function Navbar({
  onRunPipeline,
  onRefresh,
  isRunningPipeline,
  onOpenSearchFocus,
}: NavbarProps) {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[#E6E2D8] bg-[#F7F5F0]/90 backdrop-blur-xl transition-all">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        
        {/* Brand Logo & Tagline */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 items-center justify-center rounded-lg bg-[#18181B] px-3.5 shadow-sm">
              <span className="font-extrabold tracking-wider text-[#F7F5F0] text-xs uppercase">ARKAS</span>
            </div>
            <div className="hidden sm:block h-5 w-px bg-[#D5CFC2]" />
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="text-sm font-bold tracking-tight text-[#18181B]">Pazarlama Stüdyosu</span>
                <span className="rounded-full bg-[#EAE6DD] px-2 py-0.5 text-[10px] font-semibold text-[#716D65] border border-[#D5CFC2]">
                  AI v2.0
                </span>
              </div>
              <span className="text-[11px] text-[#716D65] font-normal">
                Minimalist Kreatif & Afiş Vitrini
              </span>
            </div>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2.5">
          {/* Quick Search Shortcut */}
          <button
            onClick={onOpenSearchFocus}
            className="hidden md:flex items-center gap-2.5 rounded-lg border border-[#E6E2D8] bg-white px-3.5 py-2 text-xs text-[#716D65] shadow-xs transition hover:border-[#D5CFC2] hover:text-[#18181B]"
          >
            <Search className="h-3.5 w-3.5 text-[#8E8A82]" />
            <span>Hızlı İlan Ara...</span>
            <kbd className="rounded bg-[#F0EDE6] px-1.5 py-0.5 text-[10px] font-mono text-[#716D65] border border-[#E6E2D8]">⌘K</kbd>
          </button>

          {/* Refresh Data */}
          <button
            onClick={onRefresh}
            title="Verileri Yenile"
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#E6E2D8] bg-white text-[#52525B] shadow-xs transition hover:bg-[#F0EDE6] hover:text-[#18181B] active:scale-95"
          >
            <RefreshCw className="h-4 w-4" />
          </button>

          {/* Run Pipeline Button */}
          <button
            onClick={onRunPipeline}
            disabled={isRunningPipeline}
            className="relative flex items-center gap-2 rounded-lg bg-[#18181B] px-4 py-2.5 text-xs font-semibold text-white shadow-sm transition-all hover:bg-[#27272A] active:scale-95 disabled:opacity-50 disabled:pointer-events-none"
          >
            {isRunningPipeline ? (
              <>
                <RefreshCw className="h-3.5 w-3.5 animate-spin text-white" />
                <span>İşleniyor...</span>
              </>
            ) : (
              <>
                <Zap className="h-3.5 w-3.5 text-[#C2A676] fill-[#C2A676]" />
                <span className="hidden sm:inline">Scraper & AI Motorunu Başlat</span>
                <span className="sm:hidden">Başlat</span>
              </>
            )}
          </button>
        </div>

      </div>
    </header>
  );
}
