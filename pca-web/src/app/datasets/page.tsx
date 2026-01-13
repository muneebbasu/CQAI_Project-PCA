"use client"

import { Database, Construction } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function DatasetsPage() {
    return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center text-center space-y-8">
            <div className="relative">
                <div className="absolute inset-0 bg-blue-100 rounded-full animate-ping opacity-20"></div>
                <div className="bg-gradient-to-br from-blue-100 to-indigo-100 p-8 rounded-full shadow-xl">
                    <Database className="w-16 h-16 text-blue-600" />
                </div>
                <div className="absolute -bottom-2 -right-2 bg-amber-100 p-2 rounded-lg border-2 border-white shadow-lg">
                    <Construction className="w-6 h-6 text-amber-600" />
                </div>
            </div>

            <div className="space-y-4 max-w-lg">
                <h1 className="text-4xl md:text-5xl font-black text-slate-900 tracking-tight">
                    PCA on Datasets
                </h1>
                <h2 className="text-2xl font-serif italic text-blue-600 font-medium">
                    Coming Soon
                </h2>
                <p className="text-slate-500 text-lg leading-relaxed">
                    We are building a powerful engine to analyze your own <strong>CSV and Excel</strong> files.
                    Soon you will be able to visualize high-dimensional tabular data directly in your browser.
                </p>
            </div>

            <Link href="/">
                <Button variant="outline" className="mt-8">
                    Return Home
                </Button>
            </Link>
        </div>
    )
}
