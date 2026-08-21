import type { Metadata } from "next";
import { Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";

const plusJakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
  display: "swap",
  variable: "--font-jakarta",
});

export const metadata: Metadata = {
  title: "AutoAI Showroom — Yeni Nesil Bilişsel AI Otomotiv & Kreatif Vitrin",
  description: "Duygusal satış noktaları, 5 açılı yüksek çözünürlüklü afişler ve bilişsel AI satış danışmanıyla donatılmış yeni nesil dijital otomotiv vitrini.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="tr" className={`${plusJakarta.variable}`}>
      <head>
        <meta name="referrer" content="no-referrer" />
      </head>
      <body className="min-h-screen bg-[#F7F5F0] text-[#18181B] font-sans antialiased selection:bg-[#18181B] selection:text-[#F7F5F0]">
        {children}
      </body>
    </html>
  );
}
