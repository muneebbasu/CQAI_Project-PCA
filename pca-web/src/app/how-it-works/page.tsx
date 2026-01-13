"use client"

import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
    TrendingUp, Combine, Split, ExternalLink, Code2,
    Calculator, Layers, Upload, Loader2, Play, Cpu
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"


// --- Components ---

function MatrixDisplay({ data, title, desc, color = "blue" }: { data: number[][], title: string, desc?: string, color?: "blue" | "red" | "green" }) {
    if (!data || data.length === 0) return null;

    const colorStyles = {
        blue: "bg-blue-50 text-blue-700 border-blue-200",
        red: "bg-red-50 text-red-700 border-red-200",
        green: "bg-green-50 text-green-700 border-green-200",
    }

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-xl shadow-md border border-slate-200 overflow-hidden hover:shadow-xl transition-shadow duration-300"
        >
            <div className={cn("px-4 py-3 border-b flex justify-between items-center", colorStyles[color])}>
                <span className="font-bold text-sm flex items-center gap-2">
                    <Calculator className="w-3 h-3" /> {title}
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider opacity-70">Top 5x5</span>
            </div>
            <div className="p-4 overflow-x-auto relative">
                <div className="absolute top-0 right-0 p-1 opacity-5">
                    <Code2 className="w-20 h-20" />
                </div>
                <table className="border-collapse w-full relative z-10">
                    <tbody>
                        {data.map((row, i) => (
                            <tr key={i}>
                                {row.map((val, j) => (
                                    <td key={j} className="p-2 text-right font-mono text-xs text-slate-600 border border-slate-50">
                                        {val.toFixed(2)}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            {desc && <div className="px-4 pb-4 pt-2 bg-slate-50/50 text-xs text-slate-500 border-t border-slate-100 italic">{desc}</div>}
        </motion.div>
    )
}

function WikiLink({ href }: { href: string }) {
    return (
        <a href={href} target="_blank" rel="noopener noreferrer" className="inline-flex items-center justify-center p-1 rounded-full text-blue-400 hover:text-blue-600 hover:bg-blue-50 transition-colors" title="Read more on Wikipedia">
            <ExternalLink className="w-3 h-3" />
        </a>
    )
}

function InsightCard({ title, children, icon: Icon, color = "blue" }: { title: string, children: React.ReactNode, icon: any, color?: string }) {
    const colors: any = {
        blue: "bg-blue-50 text-blue-700 border-blue-100",
        purple: "bg-purple-50 text-purple-700 border-purple-100",
        amber: "bg-amber-50 text-amber-700 border-amber-100",
        green: "bg-green-50 text-green-700 border-green-100",
    }
    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className={`p-5 rounded-2xl border ${colors[color]} flex gap-4 items-start shadow-sm`}
        >
            <div className={`mt-1 bg-white p-2 rounded-xl shadow-sm shrink-0`}>
                <Icon className="w-5 h-5" />
            </div>
            <div>
                <h4 className="font-bold mb-1 text-lg">{title}</h4>
                <div className="text-sm opacity-90 leading-relaxed font-medium">{children}</div>
            </div>
        </motion.div>
    )
}

function Step({ id, title, children, active, isLast }: { id: number, title: string, children: React.ReactNode, active: boolean, isLast: boolean }) {
    return (
        <div className={`relative pl-12 md:pl-24 py-8 ${active ? 'opacity-100' : 'opacity-40 grayscale blur-[1px]'} transition-all duration-700`}>
            {/* Timeline Line */}
            {!isLast && (
                <div className="absolute left-[22px] md:left-[46px] top-20 bottom-0 w-1 bg-slate-200 rounded-full">
                    <motion.div
                        initial={{ height: "0%" }}
                        whileInView={{ height: socketActive(active) }}
                        className="w-full bg-blue-500 rounded-full"
                    />
                </div>
            )}

            {/* Number Bubble */}
            <div className={`absolute left-0 md:left-4 top-8 w-12 h-12 md:w-16 md:h-16 rounded-2xl rotate-3 flex items-center justify-center font-black text-xl md:text-2xl shadow-xl z-10 border-4 border-white
                ${active ? 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white scale-110' : 'bg-slate-100 text-slate-400'}`}>
                {id}
            </div>

            <div className="space-y-8">
                <h2 className="text-3xl md:text-4xl font-black text-slate-800 tracking-tight">
                    {title}
                </h2>
                <div className="prose max-w-none text-slate-600 leading-8 text-lg">
                    {children}
                </div>
            </div>
        </div>
    )
}

function CodeRunner({ onRun, results }: { onRun: () => void, results: React.ReactNode }) {
    const [status, setStatus] = useState<"idle" | "running" | "done">("idle")
    const [output, setOutput] = useState<string[]>([])

    const run = () => {
        setStatus("running")
        setOutput([])
        let steps = [
            "Centering data... Done.",
            "Computing Covariance Matrix... Done.",
            "Solving Eigensystem... Done.",
            "Sorting components... Done."
        ]

        steps.forEach((step, i) => {
            setTimeout(() => {
                setOutput(prev => [...prev, step])
                if (i === steps.length - 1) setStatus("done")
            }, (i + 1) * 600)
        })
    }

    return (
        <div className="space-y-4">
            {status === "idle" ? (
                <div className="h-64 bg-slate-100 rounded-xl border-2 border-dashed border-slate-300 flex flex-col items-center justify-center text-slate-400 gap-4">
                    <p className="font-medium text-slate-500">Ready to compute?</p>
                    <Button onClick={run} className="bg-slate-800 text-white hover:bg-slate-900 shadow-xl">
                        <Play className="w-4 h-4 mr-2" /> Run Algorithm
                    </Button>
                </div>
            ) : (
                <div className="space-y-4">
                    <div className="bg-black text-green-400 font-mono text-xs p-4 rounded-xl shadow-inner h-32 overflow-y-auto">
                        <div className="flex items-center gap-2 border-b border-green-900/50 pb-2 mb-2">
                            <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                            <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                            <span className="opacity-50">terminal</span>
                        </div>
                        {output.map((line, i) => (
                            <div key={i}>$ {line}</div>
                        ))}
                        {status === "running" && <div className="animate-pulse">_</div>}
                    </div>

                    <AnimatePresence>
                        {status === "done" && (
                            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                                {results}
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            )}
        </div>
    )
}

function LinkDisplay({ active }: { active: boolean }) { return null; } // Placeholder helper

function socketActive(a: boolean) { return a ? "100%" : "0%" }

export default function HowItWorksPage() {
    const [image, setImage] = useState<string | null>(null)
    const [analysis, setAnalysis] = useState<any | null>(null)
    const [loading, setLoading] = useState(false)

    // Channels
    const [channels, setChannels] = useState<{ r: string, g: string, b: string } | null>(null);

    // Helpers
    const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.[0]) {
            const url = URL.createObjectURL(e.target.files[0])
            setImage(url); setAnalysis(null);
        }
    }

    // Canvas Logic (Client Side visual separation)
    useEffect(() => {
        if (!image) return;
        const img = new Image(); img.src = image;
        img.onload = () => {
            const w = img.width; h = img.height;
            const canvas = document.createElement('canvas'); canvas.width = w; canvas.height = h;
            const ctx = canvas.getContext('2d'); if (!ctx) return;
            ctx.drawImage(img, 0, 0);
            const data = ctx.getImageData(0, 0, w, h).data;

            const makeCH = (idx: number) => {
                const c = document.createElement('canvas'); c.width = w; c.height = h;
                const ct = c.getContext('2d'); const d = ct!.createImageData(w, h);
                for (let i = 0; i < data.length; i += 4) {
                    d.data[i] = idx === 0 ? data[i] : 0;
                    d.data[i + 1] = idx === 1 ? data[i + 1] : 0;
                    d.data[i + 2] = idx === 2 ? data[i + 2] : 0;
                    d.data[i + 3] = 255;
                }
                ct!.putImageData(d, 0, 0); return c.toDataURL();
            }
            setChannels({ r: makeCH(0), g: makeCH(1), b: makeCH(2) });
        }
        var h: number;
    }, [image]);

    const runSimulation = async () => {
        if (!image) return;
        setLoading(true);
        try {
            const res = await fetch(image); const blob = await res.blob();
            const fd = new FormData(); fd.append('image', blob);
            const r = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/analyze`, { method: 'POST', body: fd });
            if (!r.ok) throw new Error;
            setAnalysis(await r.json());
        } catch (e) { alert("Analysis Error"); }
        finally { setLoading(false); }
    }

    return (
        <div className="max-w-6xl mx-auto pb-40 px-6">
            <section className="text-center py-20 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-100 via-white to-white rounded-b-3xl mb-12">
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="inline-block">
                    <span className="px-4 py-1.5 rounded-full border border-blue-200 bg-blue-50 text-blue-700 font-bold text-sm tracking-wide uppercase mb-6 inline-block">
                        Interactive Pedagogy
                    </span>
                </motion.div>
                <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="text-5xl md:text-7xl font-black text-slate-900 tracking-tight font-serif mb-6">
                    The Anatomy of PCA
                </motion.h1>
                <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
                    Follow the transformation of your image from raw pixels to mathematical abstractions, and back again.
                </motion.p>
            </section>

            {/* Step 1 */}
            <Step id={1} title="Input & Data Grid" active={true} isLast={false}>
                <div className="grid lg:grid-cols-2 gap-12 items-center">
                    <div className="space-y-6">
                        <p>
                            Everything starts with your image. To the algorithm, this isn't a picture—it's a massive grid of numbers.
                            Each pixel has a Red, Green, and Blue value (0-255).
                        </p>
                        <InsightCard title="The Data Matrix" icon={Layers} color="blue">
                            If your image is 100x100 pixels, we have 10,000 data points. Each point has 3 dimensions (R, G, B). PCA will try to reduce these dimensions.
                        </InsightCard>
                        <div className="py-6">
                            <label className="block w-full border-3 border-dashed border-slate-300 rounded-3xl p-10 text-center hover:bg-slate-50 hover:border-blue-400 transition-all cursor-pointer group bg-slate-50/50">
                                <input type="file" onChange={handleUpload} className="hidden" />
                                <Upload className="w-12 h-12 text-slate-400 mx-auto mb-4 group-hover:scale-110 group-hover:text-blue-500 transition-all" />
                                <span className="font-bold text-lg text-slate-600 group-hover:text-slate-900 block">
                                    {image ? "Select Valid Image" : "Upload Image to Begin"}
                                </span>
                                <span className="text-sm text-slate-400">Supports PNG, JPG</span>
                            </label>
                        </div>
                    </div>
                    <div className="relative h-[400px] bg-slate-100 rounded-3xl border border-slate-200 flex items-center justify-center shadow-inner overflow-hidden">
                        {image ? (
                            <img src={image} className="max-w-full max-h-full object-contain shadow-2xl rounded-lg" />
                        ) : (
                            <div className="text-center opacity-30">
                                <div className="text-8xl mb-4">🖼️</div>
                                <div className="font-black text-2xl">NO IMAGE</div>
                            </div>
                        )}
                    </div>
                </div>
                {image && !analysis && (
                    <div className="flex justify-center pt-8">
                        <Button onClick={runSimulation} size="lg" className="h-16 px-10 text-xl rounded-full shadow-xl shadow-blue-200/50 hover:scale-105 transition-transform bg-blue-600 text-white hover:bg-blue-700">
                            {loading ? <Loader2 className="animate-spin mr-2" /> : <Play className="mr-2 fill-current" />}
                            Initialize Algorithm
                        </Button>
                    </div>
                )}
            </Step>

            {/* Step 2 */}
            <AnimatePresence>
                {analysis && channels && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1 }}>
                        <Step id={2} title="Channel Decomposition" active={true} isLast={false}>
                            <div className="space-y-6">
                                <p>
                                    PCA is often applied to each color channel independently. We split your image into three separate matrices:
                                    <span className="text-red-600 font-bold"> Red</span>,
                                    <span className="text-green-600 font-bold"> Green</span>, and
                                    <span className="text-blue-600 font-bold"> Blue</span>.
                                </p>
                                <div className="grid md:grid-cols-3 gap-8">
                                    <div className="space-y-3 group">
                                        <div className="aspect-[4/3] bg-red-50 rounded-2xl border-2 border-red-100 p-2 overflow-hidden shadow-sm group-hover:shadow-lg transition-all">
                                            <img src={channels.r} className="w-full h-full object-contain mix-blend-multiply" />
                                        </div>
                                        <p className="text-center font-bold text-red-700">Red Matrix (R)</p>
                                    </div>
                                    <div className="space-y-3 group">
                                        <div className="aspect-[4/3] bg-green-50 rounded-2xl border-2 border-green-100 p-2 overflow-hidden shadow-sm group-hover:shadow-lg transition-all">
                                            <img src={channels.g} className="w-full h-full object-contain mix-blend-multiply" />
                                        </div>
                                        <p className="text-center font-bold text-green-700">Green Matrix (G)</p>
                                    </div>
                                    <div className="space-y-3 group">
                                        <div className="aspect-[4/3] bg-blue-50 rounded-2xl border-2 border-blue-100 p-2 overflow-hidden shadow-sm group-hover:shadow-lg transition-all">
                                            <img src={channels.b} className="w-full h-full object-contain mix-blend-multiply" />
                                        </div>
                                        <p className="text-center font-bold text-blue-700">Blue Matrix (B)</p>
                                    </div>
                                </div>
                            </div>
                        </Step>

                        <Step id={3} title="Calculating Variance" active={true} isLast={false}>
                            <div className="grid md:grid-cols-2 gap-12">
                                <div className="space-y-6">
                                    <InsightCard title="Covariance Matrix" icon={TrendingUp} color="amber">
                                        This matrix tells us how pixel intensities vary <WikiLink href="https://en.wikipedia.org/wiki/Covariance_matrix" />. The <b>Diagonal</b> shows the variance (information) within the channel. The <b>Off-Diagonal</b> shows how they correlate.
                                    </InsightCard>
                                    <p>
                                        For the <b>Red Channel</b>, we calculate the covariance matrix. High variance means "lots of interesting information".
                                        Low variance means "flat, boring background".
                                    </p>
                                </div>
                                <div>
                                    <MatrixDisplay
                                        data={analysis.red.cov}
                                        title="Red Channel Covariance"
                                        desc="Notice the values. High numbers indicate strong relationships."
                                        color="red"
                                    />
                                </div>
                            </div>
                        </Step>

                        <Step id={4} title="Eigen Decomposition" active={true} isLast={false}>
                            <div className="space-y-8">
                                <p>
                                    This is the magic step. We ask the matrix: <i>"In which direction does the data vary the most?"</i>
                                    <br />The answer is the <b>Eigenvector</b> <WikiLink href="https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors" />. The amount of variance is the <b>Eigenvalue</b>.
                                </p>

                                <div className="grid lg:grid-cols-2 gap-8">
                                    <div className="bg-[#1e1e1e] text-slate-300 p-6 rounded-2xl font-mono text-xs md:text-sm shadow-2xl relative overflow-hidden border border-slate-800">
                                        <div className="absolute top-0 right-0 p-4 opacity-10"><Code2 className="w-24 h-24" /></div>
                                        <div className="flex items-center gap-2 mb-4 border-b border-slate-700 pb-2">
                                            <div className="flex gap-1.5">
                                                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                                                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                                                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                                            </div>
                                            <span className="text-slate-500 ml-2">pca_algorithm.py</span>
                                        </div>
                                        <div className="space-y-1.5 overflow-x-auto">
                                            <p><span className="text-purple-400">def</span> <span className="text-blue-400">compute_pca</span>(data):</p>
                                            <p className="pl-4 text-slate-500"># 1. Standardize (Center) the data</p>
                                            <p className="pl-4">mean = np.mean(data, axis=0)</p>
                                            <p className="pl-4">centered = data - mean</p>

                                            <p className="pl-4 text-slate-500 mt-2"># 2. Covariance Matrix</p>
                                            <p className="pl-4">cov = np.cov(centered, rowvar=<span className="text-blue-400">False</span>)</p>

                                            <p className="pl-4 text-slate-500 mt-2"># 3. Eigen Decomposition</p>
                                            <p className="pl-4"><span className="text-yellow-400">vals</span>, <span className="text-purple-400">vecs</span> = np.linalg.eig(cov)</p>

                                            <p className="pl-4 text-slate-500 mt-2"># 4. Sort by Variance (High to Low)</p>
                                            <p className="pl-4">idx = vals.argsort()[::-1]</p>
                                            <p className="pl-4">sorted_vecs = vecs[:, idx]</p>

                                            <p className="pl-4 text-slate-500 mt-2"># 5. Project Data (Compression)</p>
                                            <p className="pl-4"><span className="text-purple-400">return</span> np.dot(centered, sorted_vecs)</p>
                                        </div>
                                    </div>
                                    <div className="space-y-4">
                                        <CodeRunner
                                            onRun={() => { /* logic handled inside */ }}
                                            results={
                                                <>
                                                    <MatrixDisplay
                                                        data={analysis.red.eigVecs}
                                                        title="Principal Components (Vectors)"
                                                        color="blue"
                                                        desc="These vectors point in the direction of the greatest variance."
                                                    />
                                                    <div className="flex gap-2 flex-wrap mt-4">
                                                        {analysis.red.eigVals.map((v: number, i: number) => (
                                                            <div key={i} className="bg-yellow-50 text-yellow-700 px-3 py-1 rounded-lg border border-yellow-100 text-xs font-bold font-mono">
                                                                λ{i + 1}: {v.toFixed(1)}
                                                            </div>
                                                        ))}
                                                    </div>
                                                    <p className="text-xs text-slate-500 italic mt-2">
                                                        *Higher λ (Eigenvalue) = More Importance. We can throw away vectors with low λ.
                                                    </p>
                                                </>
                                            }
                                        />
                                    </div>
                                </div>
                            </div>
                        </Step>

                        <Step id={5} title="Reconstruction & Stacking" active={true} isLast={true}>
                            <div className="space-y-8">
                                <InsightCard title="The Final Assembly" icon={Combine} color="green">
                                    To compress the image, we keep only the top vectors (e.g., top 50). We assume the rest is noise.
                                    Then we stack the reconstructed R', G', and B' channels back together.
                                </InsightCard>

                                <div className="flex flex-col md:flex-row items-center justify-center gap-4 py-8">
                                    <div className="relative w-32 h-32 bg-red-100 rounded-lg border-2 border-red-300 shadow-lg transform -rotate-6 z-10 flex items-center justify-center font-bold text-red-500">R'</div>
                                    <div className="text-2xl font-bold text-slate-300">+</div>
                                    <div className="relative w-32 h-32 bg-green-100 rounded-lg border-2 border-green-300 shadow-lg transform rotate-0 z-20 flex items-center justify-center font-bold text-green-500">G'</div>
                                    <div className="text-2xl font-bold text-slate-300">+</div>
                                    <div className="relative w-32 h-32 bg-blue-100 rounded-lg border-2 border-blue-300 shadow-lg transform rotate-6 z-10 flex items-center justify-center font-bold text-blue-500">B'</div>
                                    <div className="text-2xl font-bold text-slate-800 px-4">=</div>
                                    <div className="relative w-40 h-40 bg-white rounded-xl border-4 border-slate-900 shadow-2xl flex items-center justify-center overflow-hidden">
                                        <img src={image || ""} className="w-full h-full object-cover opacity-90 blur-[1px]" />
                                        <div className="absolute inset-0 flex items-center justify-center bg-black/10 font-bold text-white text-shadow">Compressed</div>
                                    </div>
                                </div>

                                <div className="text-center">
                                    <p className="text-slate-600 mb-8 max-w-2xl mx-auto">
                                        You have seen the math. Now experience the power of PCA by actually compressing this image and choosing how many components to keep.
                                    </p>
                                    <Button onClick={() => window.location.href = '/compress'} size="lg" className="rounded-full px-12 h-14 text-lg bg-slate-900 text-white hover:bg-slate-800 shadow-2xl hover:shadow-black/20 hover:-translate-y-1 transition-all">
                                        Start Compression Studio
                                    </Button>
                                </div>
                            </div>
                        </Step>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    )
}
