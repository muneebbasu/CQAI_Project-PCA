"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Activity, Home, Layers, BookOpen, MessageSquare, Settings as LucideSettings } from "lucide-react" // Renamed Settings from lucide-react to LucideSettings
import { cn } from "@/lib/utils"
import Settings from "./Settings" // Assuming this is a new component to be imported

export default function Navbar() {
    const pathname = usePathname()

    const navItems = [
        { name: "Home", href: "/", icon: Home },
        { name: "Compress", href: "/compress", icon: Layers },
        { name: "Compare", href: "/compare", icon: Activity }, // Changed icon
        { name: "How it Works", href: "/how-it-works", icon: BookOpen },
        { name: "Datasets", href: "/datasets", icon: Layers }, // Added new item for Datasets
        { name: "Out Of Box", href: "/out-of-box", icon: Layers }, // Added new item with a placeholder icon
        { name: "Learn", href: "/learn", icon: Settings }, // Settings -> Learn? Maybe use BookOpen or GraduationCap
        { name: "Feedback", href: "/feedback", icon: MessageSquare }
    ]

    // Custom icon fix for Learn
    const LearnIcon = ({ className }: { className?: string }) => (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M22 10v6M2 10l10-5 10 5-10 5z" /><path d="M6 12v5c3 3 9 3 12 0v-5" /></svg>
    )

    return (
        <nav className="sticky top-0 z-50 w-full border-b border-white/10 bg-white/80 backdrop-blur-xl supports-[backdrop-filter]:bg-white/60">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2 rounded-lg text-white shadow-lg">
                            <Layers className="w-5 h-5" />
                        </div>
                        <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                            PCA Xpert
                        </span>
                    </div>

                    <div className="hidden md:block">
                        <div className="flex items-center space-x-1">
                            {navItems.map((item) => {
                                const isActive = pathname === item.href
                                const Icon = item.name === 'Learn' ? LearnIcon : item.icon
                                return (
                                    <Link
                                        key={item.href}
                                        href={item.href}
                                        className={cn(
                                            "flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-300",
                                            isActive
                                                ? "bg-slate-900 text-white shadow-md transform scale-105"
                                                : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                                        )}
                                    >
                                        <Icon className={cn("w-4 h-4", isActive ? "text-blue-300" : "text-slate-400")} />
                                        {item.name}
                                    </Link>
                                )
                            })}
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    )
}
