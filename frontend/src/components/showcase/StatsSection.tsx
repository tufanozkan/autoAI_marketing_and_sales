"use client";

import React from "react";
import { Car, Image as ImageIcon, FileText, Tag } from "lucide-react";
import { StatsResponse } from "@/lib/types";

interface StatsSectionProps {
  stats: StatsResponse | null;
  loading: boolean;
}

export function StatsSection({ stats, loading }: StatsSectionProps) {
  const items = [
    {
      label: "Canlı Yayındaki Araçlar",
      value: stats?.total_vehicles ?? 0,
      icon: Car,
      color: "text-[#18181B]",
      bg: "bg-[#F0EDE6]",
      subText: "PostgreSQL Canlı Veri",
    },
    {
      label: "Üretilen 5 Açılı Afişler",
      value: stats?.total_posters ?? 0,
      icon: ImageIcon,
      color: "text-[#9C8262]",
      bg: "bg-[#F5F0E6]",
      subText: "1080x1350 & 16:9 HD",
    },
    {
      label: "AI Reklam Metinleri",
      value: stats?.total_copies ?? 0,
      icon: FileText,
      color: "text-[#475569]",
      bg: "bg-[#F1F5F9]",
      subText: "Safe / Bold / Story",
    },
    {
      label: "Katalog Markaları",
      value: stats?.brands?.length ?? 0,
      icon: Tag,
      color: "text-[#15803D]",
      bg: "bg-[#F0FDF4]",
      subText: "Farklı Üretici",
    },
  ];

  return (
    <section className="grid grid-cols-2 gap-3.5 sm:grid-cols-2 lg:grid-cols-4">
      {items.map((item, index) => {
        const Icon = item.icon;
        return (
          <div
            key={index}
            className="group relative overflow-hidden rounded-xl border border-[#E6E2D8] bg-white p-5 shadow-xs transition-all duration-300 hover:border-[#D5CFC2] hover:shadow-md"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs font-semibold text-[#716D65]">{item.label}</p>
                <div className="mt-2 flex items-baseline gap-2">
                  {loading ? (
                    <div className="h-8 w-16 rounded bg-[#F0EDE6] skeleton-shimmer" />
                  ) : (
                    <span className="text-3xl font-extrabold tracking-tight text-[#18181B]">
                      {item.value}
                    </span>
                  )}
                </div>
                <p className="mt-1 text-[11px] text-[#8E8A82]">{item.subText}</p>
              </div>

              <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${item.bg} ${item.color}`}>
                <Icon className="h-4 w-4" />
              </div>
            </div>
          </div>
        );
      })}
    </section>
  );
}
