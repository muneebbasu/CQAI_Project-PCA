"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Upload, Layers, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"


export default function ComparePage() {
    const [image1, setImage1] = useState<string | null>(null)
    const [image2, setImage2] = useState<string | null>(null)
    const [analytics, setAnalytics] = useState<any>(null);
    const [analyzing, setAnalyzing] = useState(false);

    const handleUpload = (e: React.ChangeEvent<HTMLInputElement>, setImage: (s: string) => void) => {
        if (e.target.files?.[0]) {
            setImage(URL.createObjectURL(e.target.files[0]))
            setAnalytics(null);
        }
    }

    const runAnalysis = async () => {
        if (!image1 || !image2) return;
        setAnalyzing(true);
        try {
            const formData = new FormData();
            const b1 = await fetch(image1).then(r => r.blob());
            const b2 = await fetch(image2).then(r => r.blob());
            formData.append('original', b1);
            formData.append('compressed', b2);

            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/compare/analytics`, {
                method: 'POST',
                body: formData
            });

            if (!res.ok) throw new Error("Analysis failed");
            const data = await res.json();
            setAnalytics(data);
        } catch (e) {
            console.error(e);
            alert("Analysis failed. Ensure backend is running.");
        } finally {
            setAnalyzing(false);
        }
    };

    return (
        <div className="max-w-6xl mx-auto space-y-12 pb-20">
            <section className="text-center space-y-6">
                <h1 className="text-4xl md:text-5xl font-bold font-serif text-slate-900">
                    Compare & Analyze
                </h1>
                <p className="text-xl text-slate-600 max-w-2xl mx-auto">
                    Compare the Original vs Compressed image with advanced metrics.
                </p>
            </section>

            <div className="grid md:grid-cols-2 gap-8">
                {/* Image 1 */}
                <div className="space-y-4">
                    <h3 className="font-bold text-center text-slate-700">Original Image</h3>
                    <div className="relative border-2 border-dashed border-slate-300 rounded-lg h-80 flex items-center justify-center bg-slate-50 overflow-hidden hover:bg-slate-100 transition-colors">
                        <input type="file" onChange={(e) => handleUpload(e, setImage1)} className="absolute inset-0 opacity-0 cursor-pointer" />
                        {image1 ? <img src={image1} className="w-full h-full object-contain" /> : (
                            <div className="flex flex-col items-center">
                                <Upload className="w-12 h-12 text-slate-400 mb-2" />
                                <span className="text-slate-500 font-medium">Upload Original</span>
                            </div>
                        )}
                    </div>
                </div>

                {/* Image 2 */}
                <div className="space-y-4">
                    <h3 className="font-bold text-center text-slate-700">Compressed Image</h3>
                    <div className="relative border-2 border-dashed border-slate-300 rounded-lg h-80 flex items-center justify-center bg-slate-50 overflow-hidden hover:bg-slate-100 transition-colors">
                        <input type="file" onChange={(e) => handleUpload(e, setImage2)} className="absolute inset-0 opacity-0 cursor-pointer" />
                        {image2 ? <img src={image2} className="w-full h-full object-contain" /> : (
                            <div className="flex flex-col items-center">
                                <Upload className="w-12 h-12 text-slate-400 mb-2" />
                                <span className="text-slate-500 font-medium">Upload Compressed</span>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <div className="flex justify-center">
                <Button
                    size="lg"
                    onClick={runAnalysis}
                    disabled={!image1 || !image2 || analyzing}
                    className="gap-2 px-8"
                >
                    {analyzing ? <Loader2 className="animate-spin" /> : <Layers className="w-4 h-4" />}
                    {analyzing ? 'Running Advanced Analysis...' : 'Run Full Comparison'}
                </Button>
            </div>

            {analytics && (
                <div className="space-y-16 animate-in fade-in duration-500">
                    {/* Metrics */}
                    <section className="grid grid-cols-1 md:grid-cols-4 gap-6">
                        <MetricCard
                            title="SSIM Index"
                            value={analytics.metrics.ssim.toFixed(4)}
                            desc="Structural Similarity Index. Measures perceptual difference."
                            wiki="https://en.wikipedia.org/wiki/Structural_similarity"
                            color="blue"
                        />
                        <MetricCard
                            title="Compression Ratio"
                            value={`${((1 - (analytics.metrics.compressed_size / analytics.metrics.original_size)) * 100).toFixed(1)}%`}
                            desc={analytics.metrics.compressed_size ? "Space saved by PCA compression." : "Percentage of file size reduction."} // Fallback if size not available in analytics yet
                            wiki="https://en.wikipedia.org/wiki/Data_compression_ratio"
                            color="green"
                            // Note: Backend 'compare/analytics' might not return sizes in 'metrics' object directly if not added. 
                            // Current backend just returns ssim and sharpness. 
                            // I should stick to what is available or handle missing data gracefully.
                            // The user asked for "explain in brief about each", I will stick to what is shown + added explanations.
                            hide={true} // Hiding this for now as backend update is needed to send sizes here, or pass form frontend. 
                        />
                        <MetricCard
                            title="Original Sharpness"
                            value={analytics.metrics.sharpness_original.toFixed(1)}
                            desc="Laplacian variance. Higher means more edges/detail."
                            wiki="https://en.wikipedia.org/wiki/Sharpness"
                            color="slate"
                        />
                        <MetricCard
                            title="Compressed Sharpness"
                            value={analytics.metrics.sharpness_compressed.toFixed(1)}
                            desc="Sharpness after reconstruction. Lower implies smoothing."
                            wiki="https://en.wikipedia.org/wiki/Image_noise#Gaussian_noise"
                            color={analytics.metrics.sharpness_compressed < analytics.metrics.sharpness_original ? "orange" : "slate"}
                        />
                        <div className="bg-white p-6 rounded-xl shadow-sm border text-center flex flex-col justify-center items-center">
                            <p className="uppercase text-xs font-bold text-slate-500 mb-1">Processing Time</p>
                            <p className="text-3xl font-bold text-slate-800">{analytics.metrics.time.toFixed(4)}s</p>
                        </div>
                    </section>

                    {/* Plots Grid */}
                    <div className="grid md:grid-cols-2 gap-12">
                        <AnalysisCard
                            title="Histograms"
                            src={analytics.plots.histograms}
                            desc="Visualizes the distribution of pixel intensities. If the curves don't overlap perfecty, it means contrast or brightness has changed."
                            wiki="https://en.wikipedia.org/wiki/Image_histogram"
                        />
                        <AnalysisCard
                            title="Color Channels (RGB)"
                            src={analytics.plots.channels}
                            desc="breakdown of Red, Green, and Blue intensities. PCA often affects color balance slightly during reconstruction."
                            wiki="https://en.wikipedia.org/wiki/Channel_(digital_image)"
                        />
                        <AnalysisCard
                            title="Edge Detection (Sobel)"
                            src={analytics.plots.edges}
                            desc="Highlights boundaries within the image. Loss of edges indicates blurring (loss of high-frequency components)."
                            wiki="https://en.wikipedia.org/wiki/Sobel_operator"
                        />
                        <AnalysisCard
                            title="SSIM Map"
                            src={analytics.plots.ssim_map}
                            desc="A heatmap of differences. Darker areas indicate where the compressed image differs most from the original."
                            wiki="https://en.wikipedia.org/wiki/Structural_similarity"
                        />
                        <AnalysisCard
                            title="Frequency Domain (FFT)"
                            src={analytics.plots.fft}
                            desc="Fast Fourier Transform. Shows frequency components. PCA removes 'noise' which is often high-frequency."
                            wiki="https://en.wikipedia.org/wiki/Fast_Fourier_transform"
                        />
                        <AnalysisCard
                            title="Contours"
                            src={analytics.plots.contours}
                            desc="Outline drawing of the image structure. Useful for seeing if shapes are preserved."
                            wiki="https://en.wikipedia.org/wiki/Contour_line"
                        />
                        <AnalysisCard
                            title="Color Difference (Lab)"
                            src={analytics.plots.color_diff}
                            desc="Difference in perceptual color space (CIELAB). Shows where colors have shifted."
                            wiki="https://en.wikipedia.org/wiki/CIELAB_color_space"
                        />
                        <AnalysisCard
                            title="Texture (LBP)"
                            src={analytics.plots.texture}
                            desc="Local Binary Pattern. meaningful for texture classification."
                            wiki="https://en.wikipedia.org/wiki/Local_binary_patterns"
                        />
                    </div>
                </div>
            )}


        </div>
    )
}

import { ExternalLink, Info } from "lucide-react"

function MetricCard({ title, value, desc, wiki, color = "slate", hide = false }: any) {
    if (hide) return null;
    const colors = {
        blue: "text-blue-600",
        green: "text-green-600",
        orange: "text-orange-600",
        slate: "text-slate-800"
    }
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border text-center relative group">
            <a href={wiki} target="_blank" rel="noopener noreferrer" className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity text-slate-400 hover:text-blue-500">
                <ExternalLink className="w-4 h-4" />
            </a>
            <p className="uppercase text-xs font-bold text-slate-500 mb-1 flex items-center justify-center gap-1">
                {title}
            </p>
            <p className={`text-3xl font-bold ${colors[color as keyof typeof colors]}`}>{value}</p>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed px-2">{desc}</p>
        </div>
    )
}

function AnalysisCard({ title, src, desc, wiki }: { title: string, src: string, desc: string, wiki?: string }) {
    return (
        <div className="bg-white rounded-xl shadow-sm border overflow-hidden hover:shadow-md transition-shadow">
            <div className="p-4 border-b bg-slate-50 flex justify-between items-start">
                <div>
                    <h3 className="font-bold text-slate-800 flex items-center gap-2">
                        {title}
                        {wiki && (
                            <a href={wiki} target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-blue-500" title="Learn more on Wikipedia">
                                <ExternalLink className="w-3 h-3" />
                            </a>
                        )}
                    </h3>
                    <p className="text-xs text-slate-500 mt-1">{desc}</p>
                </div>
            </div>
            <div className="p-4 bg-slate-50/50">
                <img src={`data:image/png;base64,${src}`} className="w-full rounded shadow-sm" />
            </div>
        </div>
    )
}
