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
  title: "Arkas 2. El Pazarlama AI — Minimalist Kreatif Stüdyo",
  description: "Duygusal satış noktaları ve 5 açılı yüksek çözünürlüklü afişlerle donatılmış minimalist ve modern 2. el pazarlama vitrini.",
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
      <body className="min-h-screen bg-[#F7F5F0] text-[#18181B] font-sans antialiased selection:bg-[#18181B] selection:text-[#F7F5F0]">
        {children}
      </body>
    </html>
  );
}
