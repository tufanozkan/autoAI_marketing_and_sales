"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { StatsSection } from "@/components/showcase/StatsSection";
import { FilterToolbar } from "@/components/showcase/FilterToolbar";
import { VehicleCard } from "@/components/showcase/VehicleCard";
import { CreativeStudioModal } from "@/components/studio/CreativeStudioModal";
import { PipelineProgressModal } from "@/components/studio/PipelineProgressModal";
import { ToastNotification } from "@/components/ui/ToastNotification";
import { ChatbotWidget } from "@/components/chat/ChatbotWidget";
import {
  fetchVehicles,
  fetchStats,
  fetchBrands,
  runFullPipeline,
} from "@/lib/api";
import { Vehicle, StatsResponse, FilterAction } from "@/lib/types";
import { Sparkles, Layers, Zap, Car } from "lucide-react";

export default function Home() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [brandsList, setBrandsList] = useState<string[]>([]);
  const [search, setSearch] = useState("");
  const [brand, setBrand] = useState("all");
  const [bodyType, setBodyType] = useState("all");
  const [maxPrice, setMaxPrice] = useState<number | null>(null);
  const [viewMode, setViewMode] = useState<"grid" | "compact">("grid");

  const [loadingVehicles, setLoadingVehicles] = useState(true);
  const [loadingStats, setLoadingStats] = useState(true);

  // Modals & Popups
  const [selectedVehicle, setSelectedVehicle] = useState<Vehicle | null>(null);
  const [isStudioOpen, setIsStudioOpen] = useState(false);
  const [pipelineModalOpen, setPipelineModalOpen] = useState(false);
  const [pipelineStep, setPipelineStep] = useState<"idle" | "running" | "completed" | "error">("idle");
  const [pipelineSummary, setPipelineSummary] = useState("");
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const searchInputRef = useRef<HTMLInputElement | null>(null);

  const showToast = useCallback((msg: string) => {
    setToastMessage(msg);
  }, []);

  // Initial Data Load
  const loadInitialData = useCallback(async () => {
    setLoadingStats(true);
    try {
      const [statsData, brandsData] = await Promise.all([
        fetchStats(),
        fetchBrands(),
      ]);
      setStats(statsData);
      setBrandsList(brandsData);
    } catch (err) {
      console.error("Stats/Brands load error:", err);
    } finally {
      setLoadingStats(false);
    }
  }, []);

  // Load Vehicles based on filters
  const loadVehiclesData = useCallback(async () => {
    setLoadingVehicles(true);
    try {
      const data = await fetchVehicles({
        search: search.trim() || undefined,
        brand: brand !== "all" ? brand : undefined,
        bodyType: bodyType !== "all" ? bodyType : undefined,
        max_price: maxPrice !== null ? maxPrice : undefined,
      });
      setVehicles(data);
    } catch (err) {
      console.error("Vehicles load error:", err);
      showToast("❌ Araçlar yüklenirken bir hata oluştu.");
    } finally {
      setLoadingVehicles(false);
    }
  }, [search, brand, bodyType, maxPrice, showToast]);

  // Handle Search Debounce
  useEffect(() => {
    const timer = setTimeout(() => {
      loadVehiclesData();
    }, 250);
    return () => clearTimeout(timer);
  }, [search, brand, bodyType, maxPrice, loadVehiclesData]);

  useEffect(() => {
    loadInitialData();
  }, [loadInitialData]);

  // Keyboard shortcut ⌘K / Ctrl+K to search
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // AI Chatbot Page Filter Action Handler
  const handleApplyFilterFromAI = (action: FilterAction) => {
    if (action.brand && action.brand !== "all") {
      setBrand(action.brand);
    }
    if (action.body_type && action.body_type !== "all") {
      setBodyType(action.body_type);
    }
    if (action.max_price) {
      setMaxPrice(action.max_price);
    }
    if (action.search) {
      setSearch(action.search);
    }
  };

  // Run Full Pipeline
  const handleRunPipeline = async () => {
    setPipelineModalOpen(true);
    setPipelineStep("running");
    showToast("🚀 Canlı Arkas Scraper ve AI Danışman veritabanı güncelleniyor...");

    try {
      const res = await runFullPipeline();
      if (res.status === "success") {
        setPipelineStep("completed");
        setPipelineSummary(
          `Toplam ${res.scrape_stats.total} canlı ilan tarandı, reklam metinleri ve vitrin hazırlandı.`
        );
        showToast("🎉 İşlem başarıyla tamamlandı!");
        await loadInitialData();
        await loadVehiclesData();
      } else {
        setPipelineStep("error");
        setPipelineSummary("İşlem tamamlanamadı.");
      }
    } catch (err) {
      setPipelineStep("error");
      setPipelineSummary("Pipeline çalıştırılırken bir sunucu hatası oluştu.");
      showToast("❌ Pipeline çalıştırma hatası.");
    }
  };

  const handleOpenStudio = (v: Vehicle) => {
    setSelectedVehicle(v);
    setIsStudioOpen(true);
  };

  const handleVehicleUpdated = (updated: Vehicle) => {
    setSelectedVehicle(updated);
    setVehicles((prev) =>
      prev.map((item) => (item.id === updated.id ? updated : item))
    );
    loadInitialData();
  };

  return (
    <div className="flex min-h-screen flex-col bg-[#F7F5F0] text-[#18181B]">
      {/* Top Navbar */}
      <Navbar
        onRunPipeline={handleRunPipeline}
        onRefresh={() => {
          loadInitialData();
          loadVehiclesData();
          showToast("🔄 Veriler yenilendi.");
        }}
        isRunningPipeline={pipelineStep === "running"}
        onOpenSearchFocus={() => searchInputRef.current?.focus()}
      />

      {/* Main Container */}
      <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col px-4 py-8 sm:px-6 lg:px-8">
        
        {/* Editorial Hero Header */}
        <section className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-[#E6E2D8] pb-7">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-[#D5CFC2] bg-[#EAE6DD] px-3 py-1 text-xs font-semibold text-[#716D65] mb-3">
              <Sparkles className="h-3.5 w-3.5 text-[#9C8262]" />
              <span>Yapay Zeka Destekli Otomotiv Danışmanı & Kreatif Vitrini</span>
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-[#18181B] leading-tight">
              Arkas 2. El Pazarlama & İlan Vitrini
            </h1>
            <p className="mt-2 text-xs sm:text-sm text-[#716D65] leading-relaxed">
              Doğrudan Arkas kataloğundan çekilen orijinal araç fotoğrafları, 16:9 geniş bannerlar, sosyal medya metinleri ve sayfayı anlık yöneten akıllı AI danışmanı.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="rounded-xl border border-[#E6E2D8] bg-white p-3 text-right shadow-xs">
              <div className="text-[11px] font-semibold text-[#8E8A82]">Veritabanı Durumu</div>
              <div className="flex items-center gap-2 mt-0.5 justify-end">
                <span className="h-2 w-2 rounded-full bg-[#15803D] animate-pulse" />
                <span className="text-xs font-bold text-[#18181B]">PostgreSQL 17 Aktif</span>
              </div>
            </div>
          </div>
        </section>

        {/* Stats KPIs */}
        <div className="mb-8">
          <StatsSection stats={stats} loading={loadingStats} />
        </div>

        {/* Filters Toolbar */}
        <div className="mb-8">
          <FilterToolbar
            search={search}
            onSearchChange={setSearch}
            brand={brand}
            onBrandChange={setBrand}
            bodyType={bodyType}
            onBodyTypeChange={setBodyType}
            brandsList={brandsList}
            totalCount={stats?.total_vehicles || vehicles.length}
            viewMode={viewMode}
            onViewModeChange={setViewMode}
            searchInputRef={searchInputRef}
          />
        </div>

        {/* Showcase Header & Count */}
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Layers className="h-4 w-4 text-[#9C8262]" />
            <h2 className="text-base sm:text-lg font-bold text-[#18181B]">
              Yayındaki Araçlar & Kreatifler
            </h2>
            <span className="rounded-full bg-[#EAE6DD] px-2.5 py-0.5 text-xs font-semibold text-[#716D65] border border-[#D5CFC2]">
              {vehicles.length} Araç
            </span>
          </div>

          {maxPrice && (
            <button
              onClick={() => setMaxPrice(null)}
              className="text-xs text-[#9C8262] font-semibold hover:underline"
            >
              Fiyat Filtresini Temizle ({maxPrice.toLocaleString("tr-TR")} TL)
            </button>
          )}
        </div>

        {/* Vehicle Showcase Cards Grid / List */}
        {loadingVehicles ? (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3, 4, 5, 6].map((n) => (
              <div
                key={n}
                className="h-[460px] rounded-2xl border border-[#E6E2D8] bg-white skeleton-shimmer"
              />
            ))}
          </div>
        ) : vehicles.length === 0 ? (
          <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-[#D5CFC2] bg-white p-12 text-center shadow-xs">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-[#F0EDE6] text-[#8E8A82]">
              <Car className="h-8 w-8" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-[#18181B]">İlan Bulunamadı</h3>
            <p className="mt-1.5 max-w-md text-xs text-[#716D65]">
              {search || brand !== "all" || bodyType !== "all" || maxPrice !== null
                ? "Arama kriterlerinize uygun araç bulunamadı. Filtreleri temizleyerek tekrar deneyin veya AI Danışmana danışın."
                : "Canlı Arkas kataloğunu taramak için aşağıdaki butona basın."}
            </p>
            <button
              onClick={handleRunPipeline}
              className="mt-5 flex items-center gap-2 rounded-xl bg-[#18181B] px-5 py-2.5 text-xs font-bold text-white shadow-xs transition hover:bg-[#27272A]"
            >
              <Zap className="h-4 w-4 text-[#C2A676]" />
              <span>Scraper & AI Motorunu Başlat</span>
            </button>
          </div>
        ) : (
          <div
            className={
              viewMode === "grid"
                ? "grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
                : "flex flex-col gap-3.5"
            }
          >
            {vehicles.map((vehicle) => (
              <VehicleCard
                key={vehicle.id}
                vehicle={vehicle}
                onOpenStudio={handleOpenStudio}
                viewMode={viewMode}
              />
            ))}
          </div>
        )}
      </main>

      {/* Flagship Creative Studio Modal */}
      <CreativeStudioModal
        vehicle={selectedVehicle}
        isOpen={isStudioOpen}
        onClose={() => setIsStudioOpen(false)}
        onVehicleUpdated={handleVehicleUpdated}
        showToast={showToast}
      />

      {/* Real-time Pipeline Progress Modal */}
      <PipelineProgressModal
        isOpen={pipelineModalOpen}
        step={pipelineStep}
        summary={pipelineSummary}
        onClose={() => setPipelineModalOpen(false)}
      />

      {/* AI Danışman Chatbot Widget (Floating on Bottom Right) */}
      <ChatbotWidget
        onApplyFilter={handleApplyFilterFromAI}
        showToast={showToast}
        onOpenVehicleStudio={handleOpenStudio}
      />

      {/* Floating Toast Notification */}
      <ToastNotification
        message={toastMessage}
        onClose={() => setToastMessage(null)}
      />
    </div>
  );
}
