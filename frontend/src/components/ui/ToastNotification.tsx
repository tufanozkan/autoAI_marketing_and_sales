"use client";

import React from "react";
import { CheckCircle, AlertCircle, Info, X } from "lucide-react";

interface ToastNotificationProps {
  message: string | null;
  type?: "success" | "error" | "info";
  onClose: () => void;
}

export function ToastNotification({
  message,
  type = "info",
  onClose,
}: ToastNotificationProps) {
  if (!message) return null;

  const isSuccess = type === "success" || message.includes("başarıyla") || message.includes("🎉") || message.includes("✨") || message.includes("📋");
  const isError = type === "error" || message.includes("hata") || message.includes("❌");

  return (
    <div className="fixed bottom-6 right-6 z-50 flex items-center gap-3 rounded-xl border border-[#E6E2D8] bg-white px-4 py-3 text-xs font-semibold text-[#18181B] shadow-xl backdrop-blur-xl animate-in slide-in-from-bottom-5 duration-200">
      {isSuccess && <CheckCircle className="h-4 w-4 text-[#15803D] shrink-0" />}
      {isError && <AlertCircle className="h-4 w-4 text-[#B91C1C] shrink-0" />}
      {!isSuccess && !isError && <Info className="h-4 w-4 text-[#475569] shrink-0" />}

      <span className="max-w-md">{message}</span>

      <button
        onClick={onClose}
        className="ml-2 text-[#8E8A82] hover:text-[#18181B]"
      >
        <X className="h-3.5 w-3.5" />
      </button>
    </div>
  );
}
