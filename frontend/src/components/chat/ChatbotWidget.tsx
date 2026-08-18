"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Sparkles,
  X,
  Send,
  RefreshCw,
  Car,
  User,
  Bot,
  SlidersHorizontal,
  ChevronRight,
  ShieldCheck,
  Phone,
} from "lucide-react";
import { ChatMessage, FilterAction, Vehicle } from "@/lib/types";
import { sendChatMessage } from "@/lib/api";
import { formatCurrency, formatKM } from "@/lib/utils";

interface ChatbotWidgetProps {
  onApplyFilter: (action: FilterAction) => void;
  showToast: (msg: string) => void;
  onOpenVehicleStudio?: (vehicle: Vehicle) => void;
}

export function ChatbotWidget({
  onApplyFilter,
  showToast,
  onOpenVehicleStudio,
}: ChatbotWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [customerId, setCustomerId] = useState<number | null>(null);
  const [customerName, setCustomerName] = useState<string>("");
  
  const [sessionId, setSessionId] = useState<string>(() => {
    if (typeof window !== "undefined") {
      const saved = sessionStorage.getItem("arkas_ai_session_id");
      if (saved) return saved;
      const newId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
      sessionStorage.setItem("arkas_ai_session_id", newId);
      return newId;
    }
    return `session_${Date.now()}`;
  });

  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  // Initial greeting
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: "welcome-1",
          role: "assistant",
          content:
            "Merhaba! Arkas 2. El AI Danışmanına hoş geldiniz. 🚗✨\n\nSize nasıl hitap etmemizi istersiniz? Ad ve soyadınızı paylaşabilir misiniz?\nAyrıca aradığınız kriterlerde yeni bir araç stoğumuza girdiğinde ilk sizin haberiniz olması için telefon numaranızı da yazabilirsiniz.",
        },
      ]);
    }
  }, [messages.length]);

  // Scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // Focus input on open
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [isOpen]);

  const handleSend = async (textToSend?: string) => {
    const text = (textToSend || inputValue).trim();
    if (!text || isLoading) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputValue("");
    setIsLoading(true);

    try {
      const res = await sendChatMessage(text, customerId, sessionId);
      if (res.customer_id) {
        setCustomerId(res.customer_id);
      }
      if (res.customer_name) {
        setCustomerName(res.customer_name);
      }

      const botMsg: ChatMessage = {
        id: `bot-${Date.now()}`,
        role: "assistant",
        content: res.reply,
        timestamp: new Date().toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, botMsg]);

      // If AI generated a page filter action, execute it on the main page
      if (res.filter_action) {
        onApplyFilter(res.filter_action);
        showToast("🎯 AI Danışman sayfadaki ilanları güncelledi!");
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: `bot-err-${Date.now()}`,
          role: "assistant",
          content: "Üzgünüm, mesajınızı yanıtlarken bir bağlantı hatası oluştu. Lütfen tekrar deneyin.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetChat = () => {
    const newId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    if (typeof window !== "undefined") {
      sessionStorage.setItem("arkas_ai_session_id", newId);
    }
    setSessionId(newId);
    setCustomerId(null);
    setCustomerName("");
    setMessages([
      {
        id: `welcome-${Date.now()}`,
        role: "assistant",
        content:
          "Sohbet sıfırlandı. Merhaba! Size nasıl hitap etmemizi istersiniz? Adınızı, soyadınızı ve ilgilendiğiniz araç kriterlerini iletebilirsiniz.",
      },
    ]);
    showToast("🔄 Sohbet sıfırlandı.");
  };

  const quickChips = [
    "1.5M TL altı SUV'lar",
    "Skoda Kamiq km ve vites",
    "Kamiq koltuk ısıtma var mı?",
    "Volvo XC40 özellikleri",
    "Ekspertiz ve garanti durumu",
  ];

  return (
    <>
      {/* Floating Trigger Button on Bottom Right */}
      {!isOpen && (
        <div className="fixed bottom-6 right-6 z-40 animate-in fade-in zoom-in-75 duration-200">
          <button
            onClick={() => setIsOpen(true)}
            className="group relative flex items-center gap-2.5 rounded-full border border-[#D5CFC2] bg-[#18181B] px-5 py-3 text-xs font-bold text-white shadow-xl transition-all hover:scale-105 hover:bg-[#27272A] hover:shadow-2xl"
          >
            {/* Soft Breathing Ambient Ring */}
            <span className="absolute -inset-1 rounded-full bg-[#C2A676]/30 blur-sm animate-pulse" />
            
            <div className="relative flex h-6 w-6 items-center justify-center rounded-full bg-white/10 text-[#C2A676]">
              <Sparkles className="h-3.5 w-3.5" />
            </div>

            <div className="relative flex flex-col text-left">
              <span className="text-[10px] text-[#C2A676] font-extrabold uppercase tracking-wider">
                Yapay Zeka Danışmanı
              </span>
              <span className="text-xs font-semibold text-[#F7F5F0]">
                {customerName ? `Merhaba, ${customerName}` : "Araç Bul & Soru Sor"}
              </span>
            </div>
          </button>
        </div>
      )}

      {/* Expandable Chatbot Pop-up Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-4 sm:right-6 z-50 flex h-[580px] w-[410px] max-w-[calc(100vw-2rem)] flex-col overflow-hidden rounded-2xl border border-[#E6E2D8] bg-white shadow-2xl animate-in slide-in-from-bottom-5 duration-200">
          
          {/* Header */}
          <div className="flex items-center justify-between border-b border-[#F0EDE6] bg-[#F7F5F0] px-4 py-3.5">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#18181B] text-[#C2A676] shadow-xs">
                <Sparkles className="h-4 w-4" />
              </div>
              <div className="flex flex-col">
                <div className="flex items-center gap-1.5">
                  <span className="text-xs font-extrabold text-[#18181B]">Arkas AI Danışman</span>
                  <span className="h-1.5 w-1.5 rounded-full bg-[#15803D] animate-pulse" />
                </div>
                <span className="text-[10px] text-[#716D65]">
                  {customerName ? `${customerName} için Aktif Oturum` : "Stok Veritabanı & Canlı Otomotiv Ağı"}
                </span>
              </div>
            </div>

            <div className="flex items-center gap-1">
              <button
                onClick={handleResetChat}
                title="Sohbeti Sıfırla"
                className="flex h-8 w-8 items-center justify-center rounded-lg text-[#716D65] hover:bg-[#EBE7DE] hover:text-[#18181B]"
              >
                <RefreshCw className="h-3.5 w-3.5" />
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="flex h-8 w-8 items-center justify-center rounded-lg text-[#716D65] hover:bg-[#EBE7DE] hover:text-[#18181B]"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Messages Area */}
          <div className="flex flex-1 flex-col gap-3.5 overflow-y-auto p-4 bg-white">
            {messages.map((msg) => {
              const isUser = msg.role === "user";
              return (
                <div
                  key={msg.id}
                  className={`flex flex-col ${isUser ? "items-end" : "items-start"}`}
                >
                  <div
                    className={`max-w-[88%] rounded-2xl p-3.5 text-xs leading-relaxed ${
                      isUser
                        ? "bg-[#18181B] text-white rounded-br-none"
                        : "bg-[#F7F5F0] text-[#18181B] border border-[#E6E2D8] rounded-bl-none shadow-2xs"
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                  </div>
                  {msg.timestamp && (
                    <span className="mt-1 px-1 text-[9px] text-[#8E8A82]">
                      {msg.timestamp}
                    </span>
                  )}
                </div>
              );
            })}

            {isLoading && (
              <div className="flex items-center gap-2 rounded-xl bg-[#F7F5F0] p-3 text-xs text-[#716D65] border border-[#E6E2D8] w-fit">
                <RefreshCw className="h-3.5 w-3.5 animate-spin text-[#9C8262]" />
                <span>Arkas veritabanı taranıyor...</span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Quick Prompt Chips */}
          <div className="border-t border-[#F0EDE6] bg-[#F7F5F0] px-3 py-2">
            <div className="flex items-center gap-1.5 overflow-x-auto pb-0.5 scrollbar-none">
              {quickChips.map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSend(chip)}
                  disabled={isLoading}
                  className="shrink-0 rounded-full border border-[#E6E2D8] bg-white px-2.5 py-1 text-[10px] font-semibold text-[#52525B] transition hover:border-[#D5CFC2] hover:bg-[#EAE6DD] hover:text-[#18181B] disabled:opacity-50"
                >
                  {chip}
                </button>
              ))}
            </div>
          </div>

          {/* Input Bar */}
          <div className="border-t border-[#E6E2D8] bg-white p-3">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex items-center gap-2"
            >
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Örn: Araç kaç km? Koltuk ısıtma var mı?"
                disabled={isLoading}
                className="flex-1 rounded-xl border border-[#E6E2D8] bg-[#F7F5F0] px-3.5 py-2.5 text-xs text-[#18181B] placeholder-[#8E8A82] transition focus:border-[#18181B] focus:bg-white focus:outline-none"
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#18181B] text-white transition hover:bg-[#27272A] active:scale-95 disabled:opacity-40"
              >
                <Send className="h-3.5 w-3.5 text-[#C2A676]" />
              </button>
            </form>
          </div>

        </div>
      )}
    </>
  );
}
