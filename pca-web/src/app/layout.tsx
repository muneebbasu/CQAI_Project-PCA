import type { Metadata } from "next";
import { Inter, Merriweather } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const merriweather = Merriweather({
  weight: ["300", "400", "700", "900"],
  subsets: ["latin"],
  variable: "--font-merriweather"
});

export const metadata: Metadata = {
  title: "PCA Xpert",
  description: "Learn and Apply Principal Component Analysis effectively.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body suppressHydrationWarning={true} className={`${inter.variable} ${merriweather.variable} font-sans min-h-screen bg-slate-50`}>
        <Navbar />
        <main className="min-h-screen p-8 transition-all duration-300 pt-8 pb-20">
          {children}
        </main>
        <footer className="w-full py-6 bg-slate-900 text-slate-400 text-center text-sm">
          © 2024 Quantum Inno Visionaries team in CQAI lead by Muneeb Basu
        </footer>
      </body>
    </html>
  );
}
