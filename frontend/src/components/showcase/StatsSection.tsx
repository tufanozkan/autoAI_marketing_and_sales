"use client";

import React from "react";
import { Car, ShieldCheck, Award, Image as ImageIcon } from "lucide-react";
import { StatsResponse } from "@/lib/types";

interface StatsSectionProps {
  stats: StatsResponse | null;
  loading: boolean;
}

export function StatsSection({ stats, loading }: StatsSectionProps) {
  const items = [
    {
      label: "Showroom Araç Stoğu",
      value: stats?.total_vehicles ? `${stats.total_vehicles} Araç` : "5 Araç",
      icon: Car,
      color: "text-[#18181B]",
      bg: "bg-[#F0EDE6]",
      subText: "Hemen Teslim Sertifikalı Stok",
    },
    {
      label: "Ekspertiz Güvencesi",
      value: "100+ Nokta",
      icon: ShieldCheck,
      color: "text-[#15803D]",
      bg: "bg-[#F0FDF4]",
      subText: "%100 Şeffaf Ekspertiz Raporu",
    },
    {
      label: "Spoticar Garantisi",
      value: "12 Ay",
      icon: Award,
      color: "text-[#9C8262]",
      bg: "bg-[#F5F0E6]",
      subText: "Mekanik & Elektrik Koruma",
    },
    {
      label: "Showroom Fotoğrafları",
      value: stats?.total_images ? `${stats.total_images} Fotoğraf` : "25 Fotoğraf",
      icon: ImageIcon,
      color: "text-[#1E40AF]",
      bg: "bg-[#EFF6FF]",
      subText: "Çok Açılı Orijinal Çekimler",
    },
  ];

  return (
    <section className="grid grid-cols-2 gap-3.5 sm:grid-cols-2 lg:grid-cols-4">
      {items.map((item, index) => {
        const Icon = item.icon;
        return (
          <div
            key={index}
            className="group relative overflow-hidden rounded-2xl border border-[#E6E2D8] bg-white p-5 shadow-xs transition-all duration-300 hover:border-[#D5CFC2] hover:shadow-md"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs font-semibold text-[#716D65]">{item.label}</p>
                <div className="mt-2 flex items-baseline gap-2">
                  {loading ? (
                    <div className="h-8 w-20 rounded bg-[#F0EDE6] skeleton-shimmer" />
                  ) : (
                    <span className="text-2xl font-extrabold tracking-tight text-[#18181B]">
                      {item.value}
                    </span>
                  )}
                </div>
                <p className="mt-1 text-[11px] text-[#8E8A82]">{item.subText}</p>
              </div>

              <div className={`flex h-11 w-11 items-center justify-center rounded-xl ${item.bg} ${item.color}`}>
                <Icon className="h-5 w-5" />
              </div>
            </div>
          </div>
        );
      })}
    </section>
  );
}
