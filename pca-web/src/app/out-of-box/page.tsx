"use client"

import InteractivePCA from "@/components/InteractivePCA"
import PixelCloud from "@/components/PixelCloud"
import { useState } from "react"
import { Upload } from "lucide-react"

export default function OutOfBoxPage() {
    const [image, setImage] = useState<string | null>(null)

    const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.[0]) {
            setImage(URL.createObjectURL(e.target.files[0]))
        }
    }

    return (
        <div className="max-w-6xl mx-auto space-y-16 pb-20">
            <section className="text-center space-y-6">
                <h1 className="text-5xl font-black text-slate-900 tracking-tight">Out-of-Box Understanding</h1>
                <p className="text-xl text-slate-600 max-w-2xl mx-auto">
                    Intuition comes from experimentation. Play with raw data and see PCA in action instantly.
                </p>
            </section>

            {/* Tool 1: 2D Playground */}
            <section className="space-y-6">
                <div className="flex items-center gap-4 mb-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center text-blue-600 font-bold text-xl">1</div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">2D Data Playground</h2>
                        <p className="text-slate-500">Click to add points. See how the principal component (Red Arrow) finds the "Best Fit".</p>
                    </div>
                </div>
                <InteractivePCA />
            </section>

            {/* Tool 2: 3D Visualization */}
            <section className="space-y-6">
                <div className="flex items-center gap-4 mb-4">
                    <div className="w-12 h-12 bg-purple-100 rounded-2xl flex items-center justify-center text-purple-600 font-bold text-xl">2</div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">3D Pixel Cloud</h2>
                        <p className="text-slate-500">Upload an image to see its colors as a point cloud in 3D space.</p>
                    </div>
                </div>

                <div className="bg-white p-8 rounded-2xl shadow-xl border border-slate-200">
                    <div className="flex gap-8 mb-6 h-32 items-center">
                        <div className="relative border-2 border-dashed border-slate-300 rounded-lg w-32 h-32 flex-shrink-0 flex items-center justify-center bg-slate-50 overflow-hidden hover:bg-slate-100 transition-colors cursor-pointer">
                            <input type="file" onChange={handleUpload} className="absolute inset-0 opacity-0 cursor-pointer" />
                            {image ? <img src={image} className="w-full h-full object-cover" /> : <Upload className="text-slate-400" />}
                        </div>
                        <p className="text-slate-600 max-w-md">
                            Upload a colorful image. We will sample 2000 pixels and plot them in RGB space (Red, Green, Blue axes).
                            You will see PCA finding the "main colors" of your image.
                        </p>
                    </div>

                    <PixelCloud imageSrc={image} />
                </div>
            </section>
        </div>
    )
}
