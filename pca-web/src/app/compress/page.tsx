import { motion } from "framer-motion"
import Compressor from "@/components/Compressor"


export default function CompressPage() {
    return (
        <div className="max-w-6xl mx-auto space-y-8">
            <div>
                <h1 className="text-3xl font-bold font-serif text-slate-900">Compress Image</h1>
                <p className="text-slate-600 mt-2">Upload an image to see how PCA reduces dimensionality while preserving features.</p>
            </div>

            <div className="bg-white rounded-3xl p-6 shadow-xl shadow-slate-200/50 border border-slate-100">
                <Compressor />
            </div>


        </div>
    )
}
