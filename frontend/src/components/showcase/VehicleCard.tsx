"use client";

import React, { useState } from "react";
import { Vehicle, Poster } from "@/lib/types";
import { formatCurrency, formatKM, getAngleInfo } from "@/lib/utils";
import { Download, Eye, Sparkles, Fuel, Gauge, Layers } from "lucide-react";

interface VehicleCardProps {
  vehicle: Vehicle;
  onOpenStudio: (vehicle: Vehicle) => void;
  viewMode: "grid" | "compact";
}

export function VehicleCard({ vehicle, onOpenStudio, viewMode }: VehicleCardProps) {
  const posters = vehicle.posters || [];
  const [selectedAngleIndex, setSelectedAngleIndex] = useState(0);

  const currentPoster = posters[selectedAngleIndex] || posters[0];
  const imageUrl = currentPoster?.file_url || vehicle.primary_image_url || "/static/placeholder.png";

  const handleDownload = (e: React.MouseEvent) => {
    e.stopPropagation();
    const link = document.createElement("a");
    link.href = imageUrl;
    link.download = `${vehicle.brand}_${vehicle.model}_${currentPoster?.poster_type || "afis"}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (viewMode === "compact") {
    return (
      <div
        onClick={() => onOpenStudio(vehicle)}
        className="group flex flex-col sm:flex-row items-center justify-between gap-4 rounded-xl border border-[#E6E2D8] bg-white p-4 shadow-xs transition-all hover:border-[#D5CFC2] hover:shadow-md cursor-pointer"
      >
        <div className="flex items-center gap-4 w-full sm:w-auto">
          <div className="relative h-20 w-28 shrink-0 overflow-hidden rounded-lg bg-[#F0EDE6]">
            <img
              src={imageUrl}
              alt={`${vehicle.brand} ${vehicle.model}`}
              className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
              loading="lazy"
            />
            <span className="absolute bottom-1 right-1 rounded bg-[#18181B]/80 px-1.5 py-0.5 text-[9px] font-bold text-white">
              {posters.length} Açı
            </span>
          </div>

          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className="text-xs font-extrabold uppercase tracking-wider text-[#18181B]">
                {vehicle.brand}
              </span>
              <span className="text-xs text-[#716D65]">• {vehicle.year} Model</span>
            </div>
            <h4 className="text-sm font-bold text-[#18181B] group-hover:text-[#9C8262] transition-colors">
              {vehicle.model} {vehicle.sub_model || ""}
            </h4>
            <div className="mt-1 flex items-center gap-3 text-xs text-[#716D65]">
              <span>{formatKM(vehicle.km)}</span>
              <span>{vehicle.fuel_type || "Benzin"}</span>
              <span>{vehicle.transmission || "Otomatik"}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between sm:justify-end gap-4 w-full sm:w-auto border-t sm:border-t-0 pt-3 sm:pt-0 border-[#F0EDE6]">
          <div className="text-right">
            <div className="text-base font-extrabold text-[#18181B]">
              {formatCurrency(vehicle.price)}
            </div>
            <div className="text-[10px] text-[#15803D] font-medium">Arkas Güvencesiyle</div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleDownload}
              title="Aktif Afişi İndir"
              className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#E6E2D8] bg-[#F7F5F0] text-[#52525B] transition hover:bg-[#18181B] hover:text-white"
            >
              <Download className="h-4 w-4" />
            </button>
            <button
              onClick={() => onOpenStudio(vehicle)}
              className="flex items-center gap-1.5 rounded-lg bg-[#18181B] px-3.5 py-2 text-xs font-semibold text-white shadow-xs transition hover:bg-[#27272A]"
            >
              <Eye className="h-3.5 w-3.5" />
              <span>Stüdyo</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Standard Luxury Grid Poster Card
  return (
    <div
      onClick={() => onOpenStudio(vehicle)}
      className="group relative flex flex-col overflow-hidden rounded-2xl border border-[#E6E2D8] bg-white shadow-xs luxury-card cursor-pointer"
    >
      {/* Visual Image Container (4:5 Aspect Ratio) */}
      <div className="relative aspect-[4/5] w-full overflow-hidden bg-[#F0EDE6]">
        <img
          src={imageUrl}
          alt={`${vehicle.brand} ${vehicle.model}`}
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-[1.02]"
          loading="lazy"
        />

        {/* Top Badges */}
        <div className="absolute top-3.5 left-3.5 right-3.5 flex items-center justify-between pointer-events-none">
          <div className="flex items-center gap-1.5 rounded-md bg-white/90 px-2.5 py-1 text-[11px] font-bold text-[#18181B] backdrop-blur-md border border-[#E6E2D8] shadow-xs">
            <Layers className="h-3 w-3 text-[#9C8262]" />
            <span>{posters.length || 1} Farklı Açı</span>
          </div>

          <div className="flex items-center gap-1 rounded-md bg-[#18181B]/90 px-2.5 py-1 text-[10px] font-extrabold tracking-wider text-white uppercase backdrop-blur-md">
            <span>ARKAS AI</span>
          </div>
        </div>

        {/* Inline Multi-Angle Switcher Tabs on Card */}
        {posters.length > 1 && (
          <div
            onClick={(e) => e.stopPropagation()}
            className="absolute bottom-3 left-3 right-3 flex items-center justify-center gap-1 rounded-lg bg-white/95 p-1 backdrop-blur-lg border border-[#E6E2D8] shadow-sm transition-opacity opacity-90 group-hover:opacity-100"
          >
            {posters.map((p, idx) => {
              const info = getAngleInfo(p.poster_type);
              const isActive = idx === selectedAngleIndex;
              return (
                <button
                  key={p.id || idx}
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedAngleIndex(idx);
                  }}
                  title={info.label}
                  className={`flex-1 rounded py-1 text-[10px] font-semibold transition-all ${
                    isActive
                      ? "bg-[#18181B] text-white shadow-xs"
                      : "text-[#716D65] hover:text-[#18181B] hover:bg-[#F0EDE6]"
                  }`}
                >
                  {info.shortLabel}
                </button>
              );
            })}
          </div>
        )}
      </div>

      {/* Card Content Info */}
      <div className="flex flex-1 flex-col p-5">
        
        {/* Brand & Year Header */}
        <div className="flex items-center justify-between text-xs">
          <span className="font-extrabold uppercase tracking-wider text-[#18181B]">
            {vehicle.brand}
          </span>
          <span className="font-medium text-[#716D65]">{vehicle.year} Model</span>
        </div>

        {/* Title */}
        <h3 className="mt-1.5 text-base font-bold tracking-tight text-[#18181B] line-clamp-1 group-hover:text-[#9C8262] transition-colors">
          {vehicle.model} {vehicle.sub_model || ""}
        </h3>

        {/* Specs Pills */}
        <div className="mt-3 flex items-center gap-3 text-xs text-[#716D65]">
          <div className="flex items-center gap-1">
            <Gauge className="h-3.5 w-3.5 text-[#8E8A82]" />
            <span>{formatKM(vehicle.km)}</span>
          </div>
          <div className="flex items-center gap-1">
            <Fuel className="h-3.5 w-3.5 text-[#8E8A82]" />
            <span>{vehicle.fuel_type || "Benzin"}</span>
          </div>
          <div className="truncate">
            <span>{vehicle.transmission || "Otomatik"}</span>
          </div>
        </div>

        {/* Footer: Price & Actions */}
        <div className="mt-5 flex items-center justify-between border-t border-[#F0EDE6] pt-4">
          <div className="flex flex-col">
            <span className="text-[11px] text-[#8E8A82] font-medium">Satış Fiyatı</span>
            <span className="text-lg font-extrabold tracking-tight text-[#18181B]">
              {formatCurrency(vehicle.price)}
            </span>
          </div>

          <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
            <button
              onClick={handleDownload}
              title="Afişi İndir"
              className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#E6E2D8] bg-[#F7F5F0] text-[#52525B] transition hover:border-[#D5CFC2] hover:bg-[#18181B] hover:text-white active:scale-95"
            >
              <Download className="h-4 w-4" />
            </button>
            <button
              onClick={() => onOpenStudio(vehicle)}
              className="flex items-center gap-1.5 rounded-lg bg-[#18181B] px-3.5 py-2 text-xs font-bold text-white shadow-xs transition hover:bg-[#27272A] active:scale-95"
            >
              <Sparkles className="h-3.5 w-3.5 text-[#C2A676]" />
              <span>Stüdyo</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
