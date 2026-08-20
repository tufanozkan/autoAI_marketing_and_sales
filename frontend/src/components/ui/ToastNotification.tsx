"use client";

import React, { useEffect } from "react";
import { CheckCircle2, AlertCircle, Info, X } from "lucide-react";

interface ToastNotificationProps {
  message: string | null;
  type?: "success" | "error" | "info";
  duration?: number;
  onClose: () => void;
}

export function ToastNotification({
  message,
  type = "info",
  duration = 3500,
  onClose,
}: ToastNotificationProps) {
  useEffect(() => {
    if (!message) return;
    const timer = setTimeout(() => {
      onClose();
    }, duration);
    return () => clearTimeout(timer);
  }, [message, duration, onClose]);

  if (!message) return null;

  const isSuccess =
    type === "success" ||
    message.includes("başarıyla") ||
    message.includes("🎉") ||
    message.includes("✨") ||
    message.includes("📋") ||
    message.includes("🎯");
  const isError = type === "error" || message.includes("hata") || message.includes("❌");

  return (
    <div className="fixed top-6 left-1/2 -translate-x-1/2 z-[100] flex max-w-[calc(100vw-2rem)] items-center gap-3 rounded-2xl border border-[#E6E2D8] bg-white/95 px-4 py-3 text-xs font-semibold text-[#18181B] shadow-2xl backdrop-blur-xl animate-in fade-in slide-in-from-top-4 duration-300">
      {isSuccess && <CheckCircle2 className="h-4 w-4 text-[#15803D] shrink-0" />}
      {isError && <AlertCircle className="h-4 w-4 text-[#B91C1C] shrink-0" />}
      {!isSuccess && !isError && <Info className="h-4 w-4 text-[#C2A676] shrink-0" />}

      <span className="truncate sm:max-w-md">{message}</span>

      <button
        onClick={onClose}
        aria-label="Kapat"
        className="ml-1.5 rounded-lg p-1 text-[#8E8A82] transition hover:bg-[#F0EDE6] hover:text-[#18181B]"
      >
        <X className="h-3.5 w-3.5" />
      </button>
    </div>
  );
}
