"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Star, MessageSquare, Send, Loader2, User } from "lucide-react"
import { Button } from "@/components/ui/button"


export default function FeedbackPage() {
    const [rating, setRating] = useState(0)
    const [hover, setHover] = useState(0)
    const [data, setData] = useState({ name: "", comment: "" })
    const [feedbacks, setFeedbacks] = useState<any[]>([])
    const [loading, setLoading] = useState(false)

    const fetchFeedbacks = async () => {
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/feedback`);
            if (res.ok) {
                const list = await res.json();
                setFeedbacks(list);
            }
        } catch (e) { console.error("Failed to fetch feedbacks", e); }
    }

    useEffect(() => {
        fetchFeedbacks();
    }, [])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true);
        try {
            await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/feedback`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: data.name,
                    rating: rating,
                    comment: data.comment
                })
            });
            setData({ name: "", comment: "" });
            setRating(0);
            fetchFeedbacks();
        } catch (e) {
            alert("Failed to submit");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="max-w-4xl mx-auto space-y-12 pb-20">
            <section className="text-center space-y-6">
                <h1 className="text-4xl md:text-5xl font-bold font-serif text-slate-900">
                    We Value Your Feedback
                </h1>
                <p className="text-xl text-slate-600 max-w-2xl mx-auto">
                    Help us improve PCA ImageXpert by sharing your experience.
                </p>
            </section>

            <div className="grid md:grid-cols-2 gap-12">
                {/* Form */}
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 h-fit">
                    <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                        <MessageSquare className="w-5 h-5 text-blue-600" />
                        Leave a Review
                    </h2>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-700">How would you rate your experience?</label>
                            <div className="flex gap-2">
                                {[1, 2, 3, 4, 5].map((star) => (
                                    <button
                                        key={star}
                                        type="button"
                                        className="focus:outline-none transition-transform hover:scale-110"
                                        onMouseEnter={() => setHover(star)}
                                        onMouseLeave={() => setHover(0)}
                                        onClick={() => setRating(star)}
                                    >
                                        <Star
                                            className={`w-8 h-8 transition-colors ${star <= (hover || rating)
                                                ? "fill-yellow-400 text-yellow-400"
                                                : "text-slate-300"
                                                }`}
                                        />
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-700">Your Name</label>
                            <input
                                type="text"
                                required
                                value={data.name}
                                onChange={e => setData({ ...data, name: e.target.value })}
                                className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                                placeholder="John Doe"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-700">Comments</label>
                            <textarea
                                required
                                rows={4}
                                value={data.comment}
                                onChange={e => setData({ ...data, comment: e.target.value })}
                                className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none"
                                placeholder="Tell us what you think..."
                            />
                        </div>

                        <Button type="submit" disabled={loading || !rating} className="w-full gap-2">
                            {loading ? <Loader2 className="animate-spin" /> : <Send className="w-4 h-4" />}
                            Submit Feedback
                        </Button>
                    </form>
                </div>

                {/* List */}
                <div className="space-y-6">
                    <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                        <User className="w-5 h-5 text-green-600" />
                        Recent Reviews
                    </h2>
                    <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
                        {feedbacks.length === 0 ? (
                            <div className="text-center py-10 bg-slate-50 rounded-xl border border-dashed border-slate-200">
                                <p className="text-slate-500 italic">No reviews yet. Be the first!</p>
                            </div>
                        ) : (
                            feedbacks.map((fb, i) => (
                                <motion.div
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: i * 0.1 }}
                                    key={i}
                                    className="bg-white p-6 rounded-xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow"
                                >
                                    <div className="flex justify-between items-start mb-2">
                                        <div>
                                            <h3 className="font-bold text-slate-900">{fb.name}</h3>
                                            <p className="text-xs text-slate-400">{fb.timestamp}</p>
                                        </div>
                                        <div className="flex gap-0.5">
                                            {[...Array(5)].map((_, idx) => (
                                                <Star
                                                    key={idx}
                                                    className={`w-3 h-3 ${idx < fb.rating ? "fill-yellow-400 text-yellow-400" : "text-slate-200"}`}
                                                />
                                            ))}
                                        </div>
                                    </div>
                                    <p className="text-slate-600 text-sm leading-relaxed">
                                        {fb.comment}
                                    </p>
                                </motion.div>
                            ))
                        )}
                    </div>
                </div>
            </div>


        </div>
    )
}
