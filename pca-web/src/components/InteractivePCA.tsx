"use client"

import { useState, useEffect, useRef } from "react"
import { ArrowRight, RefreshCw, MousePointerClick } from "lucide-react"

export default function InteractivePCA() {
    const [points, setPoints] = useState<{ x: number, y: number }[]>([])
    const [eigenVectors, setEigenVectors] = useState<{ x: number, y: number, eigenvalue: number }[]>([])
    const [mean, setMean] = useState<{ x: number, y: number } | null>(null)
    const [error, setError] = useState<string | null>(null)
    const svgRef = useRef<SVGSVGElement>(null)

    const addPoint = (e: React.MouseEvent) => {
        if (!svgRef.current) return
        const rect = svgRef.current.getBoundingClientRect()
        const x = e.clientX - rect.left
        const y = e.clientY - rect.top
        setPoints([...points, { x, y }])
    }

    const clearPoints = () => {
        setPoints([])
        setEigenVectors([])
        setMean(null)
        setError(null)
    }

    useEffect(() => {
        if (points.length < 2) {
            setEigenVectors([]);
            setMean(null);
            setError(null);
            return;
        }

        try {
            setError(null);

            // 1. Calculate Mean
            const n = points.length;
            const meanX = points.reduce((s, p) => s + p.x, 0) / n;
            const meanY = points.reduce((s, p) => s + p.y, 0) / n;
            setMean({ x: meanX, y: meanY });

            // 2. Center Data
            const centered = points.map(p => ({ x: p.x - meanX, y: p.y - meanY }));

            // 3. Compute Covariance Matrix (2x2)
            // Var(X) = sum(x^2) / (n-1)
            // Var(Y) = sum(y^2) / (n-1)
            // Cov(X,Y) = sum(xy) / (n-1)

            let sumXX = 0, sumYY = 0, sumXY = 0;
            for (let p of centered) {
                sumXX += p.x * p.x;
                sumYY += p.y * p.y;
                sumXY += p.x * p.y;
            }

            const varX = sumXX / (n - 1);
            const varY = sumYY / (n - 1);
            const covXY = sumXY / (n - 1);

            // Matrix is:
            // [ a  b ]
            // [ b  d ]
            const a = varX;
            const b = covXY;
            const d = varY;

            // 4. Solve Mean Eigenvalues for 2x2 Matrix
            // Characteristic eq: lambda^2 - Tr(A)lambda + Det(A) = 0
            // lambda = (Tr +/- sqrt(Tr^2 - 4Det))/2
            const trace = a + d;
            const det = a * d - b * b;
            const discriminan = trace * trace - 4 * det;

            if (discriminan < 0) {
                // Should technically not happen for Covariance matrix (semi-positive definite)
                throw new Error("Complex eigenvalues - Check data.");
            }

            const sqrtDisc = Math.sqrt(discriminan);
            const lambda1 = (trace + sqrtDisc) / 2;
            const lambda2 = (trace - sqrtDisc) / 2;

            // 5. Solve eigenvectors
            // For 2x2 symm matrix:
            // if b != 0, v1 = [lambda1 - d, b], v2 = [lambda2 - d, b]
            // if b == 0, matrix is diagonal. v1=[1,0], v2=[0,1]

            const getEigenvector = (lambda: number) => {
                let vx, vy;
                if (Math.abs(b) > 1e-10) {
                    vx = lambda - d;
                    vy = b;
                } else if (Math.abs(lambda - a) < Math.abs(lambda - d)) {
                    // lambda corresponds to d (y-axis)
                    vx = 0; vy = 1;
                } else {
                    vx = 1; vy = 0;
                }
                // Normalize
                const mag = Math.sqrt(vx * vx + vy * vy);
                return { x: vx / mag, y: vy / mag };
            }

            const v1 = getEigenvector(lambda1);
            const v2 = getEigenvector(lambda2);

            // 6. Format results
            const scale = 2.5;
            const vecs = [
                { x: v1.x * Math.sqrt(lambda1) * scale, y: v1.y * Math.sqrt(lambda1) * scale, eigenvalue: lambda1 },
                { x: v2.x * Math.sqrt(lambda2) * scale, y: v2.y * Math.sqrt(lambda2) * scale, eigenvalue: lambda2 }
            ];

            vecs.sort((a, b) => b.eigenvalue - a.eigenvalue);
            setEigenVectors(vecs);

        } catch (e: any) {
            console.error("PCA Error:", e);
            setError(e.message || "Math error in PCA calculation.");
        }
    }, [points])

    return (
        <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
                <div>
                    <h3 className="text-xl font-bold text-slate-800">2D PCA Playground</h3>
                    <p className="text-slate-500 text-sm">Click anywhere to add data points.</p>
                </div>
                <button onClick={clearPoints} className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 text-slate-600 transition-colors">
                    <RefreshCw className="w-4 h-4" /> Reset
                </button>
            </div>

            {error && (
                <div className="bg-red-50 text-red-600 px-6 py-2 text-sm border-b border-red-100 flex items-center gap-2">
                    <span className="font-bold">Error:</span> {error}
                </div>
            )}

            <div className="relative h-[500px] w-full bg-slate-50 cursor-crosshair group">
                {points.length === 0 && (
                    <div className="absolute inset-0 flex items-center justify-center text-slate-300 pointer-events-none">
                        <div className="flex flex-col items-center gap-4">
                            <MousePointerClick className="w-12 h-12" />
                            <p className="text-lg font-medium">Click to place points</p>
                        </div>
                    </div>
                )}

                <svg ref={svgRef} onClick={addPoint} className="w-full h-full">
                    {/* Grid lines (optional) */}

                    {/* Points */}
                    {points.map((p, i) => (
                        <circle key={i} cx={p.x} cy={p.y} r="6" className="fill-blue-500 hover:fill-blue-600 transition-colors" />
                    ))}

                    {/* Mean Center */}
                    {mean && (
                        <circle cx={mean.x} cy={mean.y} r="4" className="fill-yellow-500 animate-pulse" />
                    )}

                    {/* Eigenvectors */}
                    {mean && eigenVectors.map((v, i) => (
                        <g key={i}>
                            {/* Positive Direction */}
                            <line
                                x1={mean.x}
                                y1={mean.y}
                                x2={mean.x + v.x}
                                y2={mean.y + v.y}
                                stroke={i === 0 ? "#ef4444" : "#22c55e"}
                                strokeWidth={i === 0 ? 4 : 2}
                                markerEnd={`url(#arrowhead-${i})`}
                            />
                            {/* Negative Direction (PCA axis line usually goes both ways, but vector is direction) */}
                            <line
                                x1={mean.x}
                                y1={mean.y}
                                x2={mean.x - v.x}
                                y2={mean.y - v.y}
                                stroke={i === 0 ? "#ef4444" : "#22c55e"}
                                strokeWidth={i === 0 ? 4 : 2}
                                opacity="0.5"
                                strokeDasharray="4"
                            />
                            <defs>
                                <marker id={`arrowhead-${i}`} markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                    <polygon points="0 0, 10 3.5, 0 7" fill={i === 0 ? "#ef4444" : "#22c55e"} />
                                </marker>
                            </defs>
                        </g>
                    ))}
                </svg>

                <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur p-4 rounded-xl border border-slate-200 shadow-lg text-sm">
                    <p className="font-bold text-slate-700 mb-2">Metrics</p>
                    {eigenVectors.map((v, i) => (
                        <div key={i} className="flex items-center gap-2 mb-1">
                            <div className={`w-3 h-3 rounded-full ${i === 0 ? "bg-red-500" : "bg-green-500"}`}></div>
                            <span className="text-slate-600">PC{i + 1} Variance: {v.eigenvalue.toFixed(1)}</span>
                        </div>
                    ))}
                    {points.length < 2 && <p className="text-slate-400 italic">Add 2+ points</p>}
                </div>
            </div>
        </div>
    )
}
