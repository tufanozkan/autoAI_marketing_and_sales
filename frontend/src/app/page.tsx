"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { StatsSection } from "@/components/showcase/StatsSection";
import { FilterToolbar } from "@/components/showcase/FilterToolbar";
import { VehicleCard } from "@/components/showcase/VehicleCard";
import { CreativeStudioModal } from "@/components/studio/CreativeStudioModal";
import { ToastNotification } from "@/components/ui/ToastNotification";
import { ChatbotWidget } from "@/components/chat/ChatbotWidget";
import { fetchVehicles, fetchStats, fetchBrands } from "@/lib/api";
import {
  Vehicle,
  StatsResponse,
  FilterAction,
  ChatAction,
  VehicleFilters,
  createEmptyVehicleFilters,
} from "@/lib/types";
import { ShieldCheck, Award, Car, RotateCcw } from "lucide-react";

export default function Home() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [brandsList, setBrandsList] = useState<string[]>([]);
  const [filters, setFilters] = useState<VehicleFilters>(createEmptyVehicleFilters());
  const [viewMode, setViewMode] = useState<"grid" | "compact">("grid");

  const [loadingVehicles, setLoadingVehicles] = useState(true);
  const [loadingStats, setLoadingStats] = useState(true);

  // Modals & Popups
  const [selectedVehicle, setSelectedVehicle] = useState<Vehicle | null>(null);
  const [isStudioOpen, setIsStudioOpen] = useState(false);
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
  const loadVehiclesData = useCallback(async (currentFilters: VehicleFilters = filters) => {
    setLoadingVehicles(true);
    try {
      const data = await fetchVehicles({
        search: currentFilters.search.trim() || undefined,
        brand: currentFilters.brand !== "all" ? currentFilters.brand : undefined,
        model: currentFilters.model || undefined,
        body_type: currentFilters.body_type !== "all" ? currentFilters.body_type : undefined,
        min_price: currentFilters.min_price !== null ? currentFilters.min_price : undefined,
        max_price: currentFilters.max_price !== null ? currentFilters.max_price : undefined,
        min_km: currentFilters.min_km !== null ? currentFilters.min_km : undefined,
        max_km: currentFilters.max_km !== null ? currentFilters.max_km : undefined,
        fuel_type: currentFilters.fuel_type || undefined,
        transmission: currentFilters.transmission || undefined,
        feature:
          currentFilters.features.length > 0
            ? currentFilters.features[0] === "sunroof"
              ? "cam tavan"
              : currentFilters.features[0]
            : undefined,
        is_new: currentFilters.is_new !== null ? currentFilters.is_new : undefined,
      });
      setVehicles(data);
    } catch (err) {
      console.error("Vehicles load error:", err);
      showToast("❌ Araçlar yüklenirken bir hata oluştu.");
    } finally {
      setLoadingVehicles(false);
    }
  }, [filters, showToast]);

  // Handle Search & Filter Debounce
  useEffect(() => {
    const timer = setTimeout(() => {
      loadVehiclesData(filters);
    }, 250);
    return () => clearTimeout(timer);
  }, [filters, loadVehiclesData]);

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

  const handleClearFilters = useCallback(() => {
    const empty = createEmptyVehicleFilters();
    setFilters(empty);
    loadVehiclesData(empty);
  }, [loadVehiclesData]);

  // AI Chatbot Page Filter Action Handler
  const handleApplyFilterFromAI = useCallback((action: FilterAction | ChatAction) => {
    if (action.type === "RESET_VEHICLE_FILTERS" || ("reset" in action && action.reset)) {
      handleClearFilters();
      return;
    }

    setFilters((prev) => {
      const next: VehicleFilters = { ...prev };
      const a = action as FilterAction;
      if (a.brand !== undefined) next.brand = a.brand;
      if (a.model !== undefined) next.model = a.model || null;
      if (a.body_type !== undefined) next.body_type = a.body_type;
      if (a.min_price !== undefined) next.min_price = a.min_price;
      if (a.max_price !== undefined) next.max_price = a.max_price;
      if (a.min_km !== undefined) next.min_km = a.min_km;
      if (a.max_km !== undefined) next.max_km = a.max_km;
      if (a.fuel_type !== undefined) next.fuel_type = a.fuel_type || null;
      if (a.transmission !== undefined) next.transmission = a.transmission || null;
      if (a.features !== undefined) next.features = a.features;
      if (a.is_new !== undefined) next.is_new = a.is_new;
      if (a.search !== undefined) next.search = a.search;
      return next;
    });
  }, [handleClearFilters]);

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

  const hasActiveFilters =
    filters.search !== "" ||
    filters.brand !== "all" ||
    filters.body_type !== "all" ||
    filters.min_price !== null ||
    filters.max_price !== null ||
    filters.features.length > 0 ||
    filters.model !== null;

  return (
    <div className="flex min-h-screen flex-col bg-[#F7F5F0] text-[#18181B]">
      {/* Top Showroom Navbar */}
      <Navbar
        onRefresh={() => {
          loadInitialData();
          loadVehiclesData();
          showToast("🔄 Showroom araç listesi güncellendi.");
        }}
        onOpenSearchFocus={() => searchInputRef.current?.focus()}
      />

      {/* Main Showroom Container */}
      <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col px-4 py-8 sm:px-6 lg:px-8">
        
        {/* Editorial Showroom Hero Header */}
        <section className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-[#E6E2D8] pb-7">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-[#D5CFC2] bg-[#EAE6DD] px-3.5 py-1 text-xs font-bold text-[#716D65] mb-3">
              <ShieldCheck className="h-3.5 w-3.5 text-[#15803D]" />
              <span>Sertifikalı Ekspertiz Güvencesiyle 100+ Nokta Kontrollü Araçlar</span>
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-[#18181B] leading-tight">
              Sertifikalı 2. El Otomobil Showroomu
            </h1>
            <p className="mt-2.5 text-xs sm:text-sm text-[#716D65] leading-relaxed">
              Kapsamlı ekspertiz kontrolünden geçmiş, 12 ay garantili ve hemen teslime hazır ikinci el araçlarımızı çok açılı orijinal showroom fotoğraflarıyla inceleyin.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="rounded-2xl border border-[#E6E2D8] bg-white p-3.5 text-right shadow-xs">
              <div className="text-[11px] font-semibold text-[#8E8A82]">Showroom Durumu</div>
              <div className="flex items-center gap-2 mt-0.5 justify-end">
                <span className="h-2 w-2 rounded-full bg-[#15803D] animate-pulse" />
                <span className="text-xs font-bold text-[#18181B]">Canlı & Güncel Stok</span>
              </div>
            </div>
          </div>
        </section>

        {/* Showroom Trust Stats */}
        <div className="mb-8">
          <StatsSection stats={stats} loading={loadingStats} />
        </div>

        {/* Filters Toolbar */}
        <div className="mb-8">
          <FilterToolbar
            search={filters.search}
            onSearchChange={(val) =>
              setFilters((prev) => ({ ...prev, search: val }))
            }
            brand={filters.brand}
            onBrandChange={(val) =>
              setFilters((prev) => ({ ...prev, brand: val }))
            }
            bodyType={filters.body_type}
            onBodyTypeChange={(val) =>
              setFilters((prev) => ({ ...prev, body_type: val }))
            }
            brandsList={brandsList}
            totalCount={stats?.total_vehicles || vehicles.length}
            viewMode={viewMode}
            onViewModeChange={setViewMode}
            searchInputRef={searchInputRef}
          />
        </div>

        {/* Showcase Header & Active Filter Badges */}
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <Award className="h-4 w-4 text-[#9C8262]" />
            <h2 className="text-base sm:text-lg font-extrabold text-[#18181B]">
              Seçkin Showroom Araçları
            </h2>
            <span className="rounded-full bg-[#EAE6DD] px-2.5 py-0.5 text-xs font-bold text-[#716D65] border border-[#D5CFC2]">
              {vehicles.length} Araç Listeleniyor
            </span>
          </div>

          {hasActiveFilters && (
            <button
              onClick={handleClearFilters}
              className="flex items-center gap-1.5 text-xs text-[#9C8262] font-bold hover:underline"
            >
              <RotateCcw className="h-3 w-3" />
              <span>Filtreleri Temizle</span>
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
            <h3 className="mt-4 text-lg font-bold text-[#18181B]">Aradığınız Kriterlerde Araç Bulunamadı</h3>
            <p className="mt-1.5 max-w-md text-xs text-[#716D65] leading-relaxed">
              Filtreleri temizleyerek tüm portföyü görüntüleyebilir veya sağ alttaki AI Danışmanımıza aradığınız bütçe ve modeli sorabilirsiniz.
            </p>
            <button
              onClick={handleClearFilters}
              className="mt-5 flex items-center gap-2 rounded-xl bg-[#18181B] px-5 py-2.5 text-xs font-bold text-white shadow-xs transition hover:bg-[#27272A]"
            >
              <RotateCcw className="h-3.5 w-3.5 text-[#C2A676]" />
              <span>Tüm Araçları Göster</span>
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

      {/* Vehicle Showroom Detail & Inspection Modal */}
      <CreativeStudioModal
        vehicle={selectedVehicle}
        isOpen={isStudioOpen}
        onClose={() => setIsStudioOpen(false)}
        onVehicleUpdated={handleVehicleUpdated}
        showToast={showToast}
      />

      {/* AI Sales Advisor Floating Widget */}
      <ChatbotWidget
        onApplyFilter={handleApplyFilterFromAI}
        onResetFilters={handleClearFilters}
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
