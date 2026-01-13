"use client"

import { useEffect, useRef, useState } from "react"

export default function PixelCloud({ imageSrc }: { imageSrc: string | null }) {
    const [points, setPoints] = useState<number[][]>([])
    const canvasRef = useRef<HTMLCanvasElement>(null)

    useEffect(() => {
        if (!imageSrc) return;
        const img = new Image();
        img.src = imageSrc;
        img.onload = () => {
            const canvas = document.createElement("canvas");
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext("2d");
            if (!ctx) return;
            ctx.drawImage(img, 0, 0);

            // Sample pixels
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;
            const p = [];

            // Limit to 3000 points
            const step = Math.max(1, Math.floor((canvas.width * canvas.height) / 3000));

            for (let i = 0; i < data.length; i += 4 * step) {
                p.push([data[i], data[i + 1], data[i + 2]]); // R, G, B
            }
            setPoints(p);
        }
    }, [imageSrc])

    // Draw 2D Plots
    useEffect(() => {
        if (!canvasRef.current || points.length === 0) return;
        const ctx = canvasRef.current.getContext('2d');
        if (!ctx) return;

        const w = canvasRef.current.width;
        const h = canvasRef.current.height;
        ctx.clearRect(0, 0, w, h);

        // Grid 1: Red vs Green
        drawPlot(ctx, points, 0, 1, "Red", "Green", 0, 0, w / 3, h);

        // Grid 2: Green vs Blue
        drawPlot(ctx, points, 1, 2, "Green", "Blue", w / 3, 0, w / 3, h);

        // Grid 3: Blue vs Red
        drawPlot(ctx, points, 2, 0, "Blue", "Red", 2 * w / 3, 0, w / 3, h);

    }, [points])

    function drawPlot(ctx: CanvasRenderingContext2D, pts: number[][], xIdx: number, yIdx: number, xLabel: string, yLabel: string, xOff: number, yOff: number, w: number, h: number) {
        // Background
        ctx.fillStyle = "#f8fafc";
        ctx.fillRect(xOff + 10, yOff + 10, w - 20, h - 40);
        ctx.strokeStyle = "#e2e8f0";
        ctx.strokeRect(xOff + 10, yOff + 10, w - 20, h - 40);

        // Points
        pts.forEach(p => {
            const x = (p[xIdx] / 255) * (w - 40) + xOff + 20;
            const y = (1 - (p[yIdx] / 255)) * (h - 60) + yOff + 20; // Flip Y
            ctx.fillStyle = `rgb(${p[0]}, ${p[1]}, ${p[2]})`;
            ctx.fillRect(x, y, 2, 2);
        });

        // Labels
        ctx.fillStyle = "#64748b";
        ctx.font = "bold 12px sans-serif";
        ctx.textAlign = "center";

        // X Axis
        ctx.fillText(xLabel, xOff + w / 2, h - 5);

        // Y Axis
        ctx.save();
        ctx.translate(xOff + 15, h / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText(yLabel, 0, -5);
        ctx.restore();
    }

    if (!imageSrc) return <div className="h-full flex items-center justify-center text-slate-400">Upload an image above to visualize its color distribution</div>

    return (
        <div className="h-[400px] w-full bg-white rounded-xl overflow-hidden relative border border-slate-200">
            <canvas ref={canvasRef} width={900} height={400} className="w-full h-full" />
            <div className="absolute top-2 right-2 flex gap-4 text-xs font-mono text-slate-500 bg-white/80 p-2 rounded border">
                <span>R vs G</span>
                <span>G vs B</span>
                <span>B vs R</span>
            </div>
        </div>
    )
}
