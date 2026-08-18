"use client";

import React, { useState } from "react";
import { Vehicle } from "@/lib/types";
import { formatCurrency, formatKM } from "@/lib/utils";
import { Sparkles, Fuel, Gauge, Layers, ShieldCheck, Zap } from "lucide-react";

interface VehicleCardProps {
  vehicle: Vehicle;
  onOpenStudio: (vehicle: Vehicle) => void;
  viewMode: "grid" | "compact";
}

export function VehicleCard({ vehicle, onOpenStudio, viewMode }: VehicleCardProps) {
  const images = vehicle.image_urls && vehicle.image_urls.length > 0
    ? vehicle.image_urls
    : [vehicle.primary_image_url || "/static/placeholder.png"];

  const [selectedPhotoIndex, setSelectedPhotoIndex] = useState(0);
  const currentImageUrl = images[selectedPhotoIndex] || images[0];

  if (viewMode === "compact") {
    return (
      <div
        onClick={() => onOpenStudio(vehicle)}
        className="group flex flex-col sm:flex-row items-center justify-between gap-4 rounded-xl border border-[#E6E2D8] bg-white p-4 shadow-xs transition-all hover:border-[#D5CFC2] hover:shadow-md cursor-pointer"
      >
        <div className="flex items-center gap-4 w-full sm:w-auto">
          <div className="relative h-20 w-28 shrink-0 overflow-hidden rounded-lg bg-[#F0EDE6]">
            <img
              src={currentImageUrl}
              alt={`${vehicle.brand} ${vehicle.model}`}
              className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
              loading="lazy"
            />
            {images.length > 1 && (
              <span className="absolute bottom-1 right-1 rounded bg-[#18181B]/80 px-1.5 py-0.5 text-[9px] font-bold text-white">
                {images.length} Foto
              </span>
            )}
          </div>

          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className="text-xs font-extrabold uppercase tracking-wider text-[#18181B]">
                {vehicle.brand}
              </span>
              <span className="text-xs text-[#716D65]">• {vehicle.year} Model</span>
              {vehicle.package && (
                <span className="rounded bg-[#F0EDE6] px-1.5 py-0.5 text-[10px] font-semibold text-[#18181B]">
                  {vehicle.package}
                </span>
              )}
            </div>
            <h4 className="text-sm font-bold text-[#18181B] group-hover:text-[#9C8262] transition-colors">
              {vehicle.model} {vehicle.sub_model || ""}
            </h4>
            <div className="mt-1 flex items-center gap-3 text-xs text-[#716D65]">
              <span>{formatKM(vehicle.km)}</span>
              <span>{vehicle.fuel_type || "Benzin"}</span>
              <span>{vehicle.transmission || "Otomatik"}</span>
              {vehicle.engine_power && <span>{vehicle.engine_power}</span>}
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between sm:justify-end gap-4 w-full sm:w-auto border-t sm:border-t-0 pt-3 sm:pt-0 border-[#F0EDE6]">
          <div className="text-right">
            <div className="text-base font-extrabold text-[#18181B]">
              {formatCurrency(vehicle.price)}
            </div>
            <div className="text-[10px] text-[#15803D] font-medium flex items-center justify-end gap-1">
              <ShieldCheck className="h-3 w-3" />
              <span>Arkas Güvenceli</span>
            </div>
          </div>

          <button
            onClick={() => onOpenStudio(vehicle)}
            className="flex items-center gap-1.5 rounded-lg bg-[#18181B] px-3.5 py-2 text-xs font-semibold text-white shadow-xs transition hover:bg-[#27272A]"
          >
            <Sparkles className="h-3.5 w-3.5 text-[#C2A676]" />
            <span>AI Kreatif & Detay</span>
          </button>
        </div>
      </div>
    );
  }

  // Standard Luxury Grid Card
  return (
    <div
      onClick={() => onOpenStudio(vehicle)}
      className="group relative flex flex-col overflow-hidden rounded-2xl border border-[#E6E2D8] bg-white shadow-xs luxury-card cursor-pointer"
    >
      {/* Visual Image Container (16:10 Aspect Ratio) */}
      <div className="relative aspect-[16/10] w-full overflow-hidden bg-[#F0EDE6]">
        {vehicle.primary_image_url ? (
          <>
            <img
              src={currentImageUrl}
              alt={`${vehicle.brand} ${vehicle.model}`}
              referrerPolicy="no-referrer"
              className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
              loading="lazy"
            />
            {/* Top Badges */}
            <div className="absolute top-3.5 left-3.5 right-3.5 flex items-center justify-between pointer-events-none">
              <div className="flex items-center gap-1.5 rounded-md bg-white/90 px-2.5 py-1 text-[11px] font-bold text-[#18181B] backdrop-blur-md border border-[#E6E2D8] shadow-xs">
                <Layers className="h-3 w-3 text-[#9C8262]" />
                <span>{images.length} Orijinal Görsel</span>
              </div>

              <div className="flex items-center gap-1 rounded-md bg-[#18181B]/90 px-2.5 py-1 text-[10px] font-extrabold tracking-wider text-white uppercase backdrop-blur-md">
                <span>ARKAS 2. EL</span>
              </div>
            </div>

            {/* Photo Switcher Dots / Tabs */}
            {images.length > 1 && (
              <div
                onClick={(e) => e.stopPropagation()}
                className="absolute bottom-2.5 left-3 right-3 flex items-center justify-center gap-1.5 rounded-lg bg-black/40 p-1 backdrop-blur-md transition-opacity opacity-0 group-hover:opacity-100"
              >
                {images.slice(0, 6).map((_, idx) => (
                  <button
                    key={idx}
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedPhotoIndex(idx);
                    }}
                    className={`h-2 rounded-full transition-all ${
                      idx === selectedPhotoIndex ? "w-6 bg-white" : "w-2 bg-white/50 hover:bg-white/80"
                    }`}
                  />
                ))}
              </div>
            )}
          </>
        ) : (
          <div className="flex h-full w-full flex-col items-center justify-center bg-[#EAE6DD] p-6 text-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[#DCD6C9] text-[#716D65] mb-2">
              <Layers className="h-6 w-6 text-[#8E8A82]" />
            </div>
            <span className="text-xs font-bold text-[#18181B]">
              Bu aracın görseli bulunmamaktadır
            </span>
            <span className="mt-1 text-[10px] text-[#716D65]">
              Arkas Spoticar 100+ Nokta Kontrollü
            </span>
          </div>
        )}
      </div>

      {/* Card Content Info */}
      <div className="flex flex-1 flex-col p-5">
        
        {/* Brand & Year Header */}
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-1.5">
            <span className="font-extrabold uppercase tracking-wider text-[#18181B]">
              {vehicle.brand}
            </span>
            {vehicle.package && (
              <span className="rounded bg-[#F0EDE6] px-1.5 py-0.5 text-[10px] font-bold text-[#716D65]">
                {vehicle.package}
              </span>
            )}
          </div>
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
              onClick={() => onOpenStudio(vehicle)}
              className="flex items-center gap-1.5 rounded-lg bg-[#18181B] px-3.5 py-2 text-xs font-bold text-white shadow-xs transition hover:bg-[#27272A] active:scale-95"
            >
              <Sparkles className="h-3.5 w-3.5 text-[#C2A676]" />
              <span>AI Metin & Detay</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
