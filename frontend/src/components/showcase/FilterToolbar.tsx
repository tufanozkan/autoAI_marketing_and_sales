"use client";

import React from "react";
import { Search, X, SlidersHorizontal, LayoutGrid, List } from "lucide-react";

interface FilterToolbarProps {
  search: string;
  onSearchChange: (val: string) => void;
  brand: string;
  onBrandChange: (val: string) => void;
  bodyType: string;
  onBodyTypeChange: (val: string) => void;
  brandsList: string[];
  totalCount: number;
  viewMode: "grid" | "compact";
  onViewModeChange: (mode: "grid" | "compact") => void;
  searchInputRef: React.RefObject<HTMLInputElement | null>;
}

export function FilterToolbar({
  search,
  onSearchChange,
  brand,
  onBrandChange,
  bodyType,
  onBodyTypeChange,
  brandsList,
  totalCount,
  viewMode,
  onViewModeChange,
  searchInputRef,
}: FilterToolbarProps) {
  const bodyTypes = [
    { label: "Tüm Kasa Tipleri", value: "all" },
    { label: "SUV", value: "SUV" },
    { label: "Sedan", value: "Sedan" },
    { label: "Hatchback", value: "Hatchback" },
  ];

  return (
    <div className="flex flex-col gap-4 rounded-xl border border-[#E6E2D8] bg-white p-4 sm:p-5 shadow-xs">
      
      {/* Top Row: Search Input + Selects + Layout Toggle */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        
        {/* Search Bar */}
        <div className="relative flex-1">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-[#8E8A82]">
            <Search className="h-4 w-4" />
          </div>
          <input
            ref={searchInputRef}
            type="text"
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Marka, model, yakıt veya donanım ara..."
            className="w-full rounded-lg border border-[#E6E2D8] bg-[#F7F5F0] py-2.5 pl-10 pr-9 text-xs sm:text-sm text-[#18181B] placeholder-[#8E8A82] transition focus:border-[#18181B] focus:bg-white focus:outline-none"
          />
          {search && (
            <button
              onClick={() => onSearchChange("")}
              className="absolute inset-y-0 right-0 flex items-center pr-3 text-[#8E8A82] hover:text-[#18181B]"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>

        {/* Filters Group */}
        <div className="flex items-center gap-2.5 overflow-x-auto pb-1 sm:pb-0">
          
          {/* Body Type Dropdown */}
          <div className="relative min-w-[140px]">
            <select
              value={bodyType}
              onChange={(e) => onBodyTypeChange(e.target.value)}
              className="w-full appearance-none rounded-lg border border-[#E6E2D8] bg-[#F7F5F0] px-3.5 py-2.5 text-xs font-medium text-[#18181B] transition hover:border-[#D5CFC2] focus:border-[#18181B] focus:bg-white focus:outline-none cursor-pointer"
            >
              {bodyTypes.map((t) => (
                <option key={t.value} value={t.value} className="bg-white text-[#18181B]">
                  {t.label}
                </option>
              ))}
            </select>
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3 text-[#8E8A82]">
              <SlidersHorizontal className="h-3.5 w-3.5" />
            </div>
          </div>

          {/* View Mode Toggle */}
          <div className="flex items-center rounded-lg border border-[#E6E2D8] bg-[#F7F5F0] p-1">
            <button
              onClick={() => onViewModeChange("grid")}
              className={`rounded-md p-1.5 transition ${
                viewMode === "grid"
                  ? "bg-[#18181B] text-white shadow-xs"
                  : "text-[#716D65] hover:text-[#18181B]"
              }`}
              title="Afiş Izgara Görünümü"
            >
              <LayoutGrid className="h-4 w-4" />
            </button>
            <button
              onClick={() => onViewModeChange("compact")}
              className={`rounded-md p-1.5 transition ${
                viewMode === "compact"
                  ? "bg-[#18181B] text-white shadow-xs"
                  : "text-[#716D65] hover:text-[#18181B]"
              }`}
              title="Kompakt Liste Görünümü"
            >
              <List className="h-4 w-4" />
            </button>
          </div>

        </div>
      </div>

      {/* Bottom Row: Brand Pills Carousel */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none pt-2 border-t border-[#F0EDE6]">
        <button
          onClick={() => onBrandChange("all")}
          className={`shrink-0 rounded-full px-3.5 py-1.5 text-xs font-semibold transition-all ${
            brand === "all"
              ? "bg-[#18181B] text-white shadow-xs"
              : "border border-[#E6E2D8] bg-[#F7F5F0] text-[#716D65] hover:border-[#D5CFC2] hover:text-[#18181B]"
          }`}
        >
          Tümü ({totalCount})
        </button>

        {brandsList.map((b) => (
          <button
            key={b}
            onClick={() => onBrandChange(b)}
            className={`shrink-0 rounded-full px-3.5 py-1.5 text-xs font-semibold transition-all ${
              brand === b
                ? "bg-[#18181B] text-white shadow-xs"
                : "border border-[#E6E2D8] bg-[#F7F5F0] text-[#716D65] hover:border-[#D5CFC2] hover:text-[#18181B]"
            }`}
          >
            {b}
          </button>
        ))}
      </div>

    </div>
  );
}
