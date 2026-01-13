"use client"

import { useState, useCallback } from "react"
import { motion } from "framer-motion"
import { Upload, Download, Loader2, Info, Image as ImageIcon } from "lucide-react"
import { useDropzone } from "react-dropzone"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

export default function Compressor() {
    const [originalImage, setOriginalImage] = useState<string | null>(null)
    const [processedImage, setProcessedImage] = useState<string | null>(null)
    const [isProcessing, setIsProcessing] = useState(false)
    const [numComponents, setNumComponents] = useState(10)
    const [maxComponents, setMaxComponents] = useState(100)
    const [metrics, setMetrics] = useState({ originalSize: 0, compressedSize: 0, time: 0 })



    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = acceptedFiles[0]
        if (!file) return

        setMetrics(prev => ({ ...prev, originalSize: file.size }))
        const reader = new FileReader()
        reader.onload = (e) => {
            const src = e.target?.result as string
            setOriginalImage(src)

            const img = new Image()
            img.src = src
            img.onload = () => {
                const max = Math.min(img.width, img.height)
                setMaxComponents(max)
                setNumComponents(Math.min(50, max))
                processImage(img, Math.min(50, max))
            }
        }
        reader.readAsDataURL(file)
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: { 'image/*': ['.jpeg', '.jpg', '.png'] } })

    const processImage = async (img: HTMLImageElement, k: number) => {
        setIsProcessing(true);
        try {
            // We need the original file blob or recreate it.
            // Since we have originalImage URL (blob url), we can fetch it.
            if (!originalImage) return;
            const resBlob = await fetch(originalImage);
            const blob = await resBlob.blob();

            const formData = new FormData();
            formData.append('image', blob);
            formData.append('num_components', k.toString());

            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/compress`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Compression failed');

            const timeHeader = response.headers.get('X-Processing-Time');
            const processingTime = timeHeader ? parseFloat(timeHeader) : 0;

            const compressedBlob = await response.blob();
            const compressedUrl = URL.createObjectURL(compressedBlob);

            setProcessedImage(compressedUrl);
            setMetrics(prev => ({
                ...prev,
                compressedSize: compressedBlob.size,
                time: processingTime
            }));
        } catch (error) {
            console.error(error);
            alert("Compression failed. Make sure Python backend is running!");
        } finally {
            setIsProcessing(false);
        }
    }

    const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNumComponents(parseInt(e.target.value))
    }

    const handleApply = () => {
        if (!originalImage) return;
        const img = new Image();
        img.src = originalImage;
        img.onload = () => processImage(img, numComponents);
    }

    return (
        <div className="space-y-8">
            {!originalImage ? (
                <div {...getRootProps()} className={cn(
                    "border-4 border-dashed rounded-3xl p-12 text-center cursor-pointer transition-colors h-96 flex flex-col items-center justify-center",
                    isDragActive ? "border-blue-500 bg-blue-50" : "border-slate-200 hover:border-blue-400"
                )}>
                    <input {...getInputProps()} />
                    <Upload className="w-16 h-16 text-slate-400 mb-4" />
                    <p className="text-xl font-medium text-slate-600">Drag & drop an image here, or click to select</p>
                    <p className="text-sm text-slate-400 mt-2">Supports JPG, PNG (Max 50MB)</p>
                </div>
            ) : (
                <div className="space-y-8">
                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col md:flex-row gap-8 items-center justify-between">
                        <div className="w-full md:w-1/2 space-y-4">
                            <label className="text-lg font-semibold text-slate-700 flex justify-between">
                                <span>Principal Components: <span className="text-blue-600">{numComponents}</span></span>
                                <span className="text-xs text-slate-400">Max: {maxComponents}</span>
                            </label>
                            <input
                                type="range"
                                min="1"
                                max={maxComponents}
                                value={numComponents}
                                onChange={handleSliderChange}
                                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                            />
                            <div className="flex gap-4">
                                <Button onClick={handleApply} disabled={isProcessing} className="bg-blue-600 hover:bg-blue-700">
                                    {isProcessing ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Processing...</> : "Apply PCA"}
                                </Button>
                                <Button variant="outline" onClick={() => setOriginalImage(null)}>
                                    Upload New Image
                                </Button>
                            </div>
                        </div>

                        {/* Metrics */}
                        <div className="flex gap-8 text-center bg-slate-50 p-4 rounded-xl">
                            <div>
                                <p className="text-xs text-slate-500 uppercase tracking-wider">Original</p>
                                <p className="text-lg font-bold">{(metrics.originalSize / 1024).toFixed(1)} KB</p>
                            </div>
                            <div>
                                <p className="text-xs text-slate-500 uppercase tracking-wider">Compressed</p>
                                <p className="text-lg font-bold">{(metrics.compressedSize / 1024).toFixed(1)} KB</p>
                            </div>
                            <div>
                                <p className="text-xs text-slate-500 uppercase tracking-wider">Ratio</p>
                                <p className="text-lg font-bold text-green-600">
                                    {(100 - (metrics.compressedSize / metrics.originalSize * 100)).toFixed(1)}%
                                </p>
                            </div>
                            <div>
                                <p className="text-xs text-slate-500 uppercase tracking-wider">Time</p>
                                <p className="text-lg font-bold text-blue-600">
                                    {metrics.time.toFixed(4)}s
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-8">
                        <div className="space-y-2">
                            <h3 className="font-semibold text-slate-600 flex items-center gap-2"><ImageIcon className="w-4 h-4" /> Original</h3>
                            <img src={originalImage} alt="Original" className="rounded-xl shadow-md w-full" />
                        </div>
                        <div className="space-y-2 relative">
                            <h3 className="font-semibold text-slate-600 flex items-center gap-2"><ImageIcon className="w-4 h-4" /> Compressed</h3>
                            {processedImage ? (
                                <img src={processedImage} alt="Compressed" className="rounded-xl shadow-md w-full" />
                            ) : (
                                <div className="w-full h-64 bg-slate-100 rounded-xl flex items-center justify-center text-slate-400">
                                    Waiting for processing...
                                </div>
                            )}
                            {isProcessing && (
                                <div className="absolute inset-0 bg-white/50 backdrop-blur-sm flex items-center justify-center rounded-xl">
                                    <Loader2 className="w-12 h-12 text-blue-600 animate-spin" />
                                </div>
                            )}
                        </div>
                    </div>

                    {processedImage && (
                        <div className="flex justify-center">
                            <a href={processedImage} download="pca-compressed.jpg" className="flex items-center gap-2 bg-green-600 text-white px-6 py-3 rounded-full hover:bg-green-700 transition-colors shadow-lg">
                                <Download className="w-5 h-5" /> Download Compressed Image
                            </a>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
