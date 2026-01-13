"use client"

import { useState, useEffect } from "react"
import { Settings as SettingsIcon, X, Moon, Sun, Monitor, Palette } from "lucide-react"
import { Button } from "@/components/ui/button"
import { motion, AnimatePresence } from "framer-motion"

export default function Settings() {
    const [isOpen, setIsOpen] = useState(false)
    const [theme, setTheme] = useState("light") // Default light for now
    const [accent, setAccent] = useState("blue")

    // In a real app, we would persist this or use a Context
    // For now, we simulate the UI

    return (
        <>
            <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsOpen(true)}
                className="text-slate-500 hover:text-slate-900"
            >
                <SettingsIcon className="w-5 h-5" />
            </Button>

            <AnimatePresence>
                {isOpen && (
                    <>
                        {/* Backdrop */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsOpen(false)}
                            className="fixed inset-0 bg-black/20 backdrop-blur-sm z-50"
                        />

                        {/* Slide-over Panel */}
                        <motion.div
                            initial={{ x: "100%" }}
                            animate={{ x: 0 }}
                            exit={{ x: "100%" }}
                            transition={{ type: "spring", damping: 25, stiffness: 200 }}
                            className="fixed inset-y-0 right-0 w-80 bg-white shadow-2xl z-50 p-6 space-y-8 border-l border-slate-100"
                        >
                            <div className="flex items-center justify-between">
                                <h2 className="text-xl font-bold text-slate-900">Settings</h2>
                                <Button variant="ghost" size="icon" onClick={() => setIsOpen(false)}>
                                    <X className="w-5 h-5 text-slate-400 hover:text-slate-900" />
                                </Button>
                            </div>

                            {/* Theme Section */}
                            <div className="space-y-4">
                                <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                                    <Monitor className="w-4 h-4" /> Appearance
                                </h3>
                                <div className="grid grid-cols-2 gap-3">
                                    <button
                                        onClick={() => setTheme("light")}
                                        className={`p-3 rounded-xl border flex flex-col items-center gap-2 transition-all ${theme === "light"
                                            ? "border-blue-500 bg-blue-50 text-blue-700 ring-1 ring-blue-500"
                                            : "border-slate-200 text-slate-600 hover:bg-slate-50"
                                            }`}
                                    >
                                        <Sun className="w-6 h-6" />
                                        <span className="text-xs font-bold">Light</span>
                                    </button>
                                    <button
                                        onClick={() => setTheme("dark")}
                                        className={`p-3 rounded-xl border flex flex-col items-center gap-2 transition-all ${theme === "dark"
                                            ? "border-purple-500 bg-purple-50 text-purple-700 ring-1 ring-purple-500"
                                            : "border-slate-200 text-slate-600 hover:bg-slate-50"
                                            }`}
                                    >
                                        <Moon className="w-6 h-6" />
                                        <span className="text-xs font-bold">Dark</span>
                                    </button>
                                </div>
                                <p className="text-xs text-slate-400 italic">
                                    Dark mode is currently a demo placeholder.
                                </p>
                            </div>

                            {/* Accent Color Section */}
                            <div className="space-y-4">
                                <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                                    <Palette className="w-4 h-4" /> Accent Color
                                </h3>
                                <div className="grid grid-cols-4 gap-3">
                                    {["blue", "purple", "green", "orange"].map((c) => (
                                        <button
                                            key={c}
                                            onClick={() => setAccent(c)}
                                            className={`w-12 h-12 rounded-full border-2 flex items-center justify-center transition-all ${accent === c
                                                ? "border-slate-900 scale-110 shadow-md"
                                                : "border-transparent hover:scale-105"
                                                }`}
                                            style={{ backgroundColor: `var(--color-${c}, ${getColorHex(c)})` }}
                                        >
                                            {accent === c && <div className="w-2 h-2 rounded-full bg-white" />}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            {/* Info */}
                            <div className="pt-8 border-t border-slate-100">
                                <p className="text-xs text-center text-slate-400">
                                    PCA Xpert v2.1 <br />
                                    Designed by QIV Team
                                </p>
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </>
    )
}

function getColorHex(name: string) {
    const map: any = {
        blue: "#2563eb",
        purple: "#9333ea",
        green: "#16a34a",
        orange: "#ea580c"
    }
    return map[name]
}
