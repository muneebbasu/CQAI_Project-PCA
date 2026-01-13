"use client"

import { Button } from "@/components/ui/button"
import Link from "next/link"
import { ArrowRight, BarChart3, Upload, Zap, BookOpen, Layers, Activity, Plus, Minus } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import { useState } from "react"

const FAQ_ITEMS = [
  {
    question: "What is PCA used for?",
    answer: "PCA is used primarily for dimensionality reduction and data visualization, allowing us to reduce the number of variables in our data without losing much information."
  },
  {
    question: "Can PCA be used for classification?",
    answer: "PCA itself is not a classification technique, but it can be used as a preprocessing step to reduce the number of features before applying classification algorithms."
  },
  {
    question: "Is PCA sensitive to data scaling?",
    answer: "Yes, PCA is sensitive to the scale of the data. It is generally recommended to standardize or normalize the data before applying PCA."
  },
  {
    question: "How many principal components should I retain?",
    answer: "This depends on your specific needs. A common approach is to retain enough components to explain a certain percentage (e.g., 95%) of the variance in your data."
  },
  {
    question: "What are the limitations of PCA?",
    answer: "PCA assumes linear relationships between variables, is sensitive to outliers, and may not work well with non-linear data. It also requires standardized data for optimal results."
  },
  {
    question: "What's the difference between PCA and factor analysis?",
    answer: "While both reduce dimensionality, PCA focuses on explaining maximum variance, while factor analysis focuses on identifying underlying factors that explain correlations between variables."
  },
  {
    question: "Can PCA handle categorical data?",
    answer: "PCA is designed for continuous numerical data. Categorical data should be properly encoded (e.g., one-hot encoding) before applying PCA, though other techniques might be more appropriate."
  },
  {
    question: "Is PCA computationally expensive?",
    answer: "For small to medium datasets, PCA is relatively fast. However, for very large datasets, computational cost can increase significantly, especially when computing the covariance matrix."
  }
]

export default function HomePage() {
  return (
    <div className="space-y-32 pb-20">
      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-100 via-white to-white opacity-70"></div>
        <div className="max-w-5xl mx-auto px-6 text-center space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <span className="px-4 py-2 rounded-full bg-blue-50 text-blue-700 font-bold text-sm tracking-wide border border-blue-100">
              v2.0 Now With Interactive Pedagogy
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-6xl md:text-8xl font-black text-slate-900 tracking-tighter"
          >
            Master <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Data</span> <br />
            <span className="text-4xl md:text-6xl font-serif font-normal italic text-slate-600">through Dimensions.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed"
          >
            Uncover hidden patterns in complex data. Use Principal Component Analysis to reduce dimensionality, remove noise, and visualize structure.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row justify-center gap-4 pt-4"
          >
            <Link href="/compress">
              <Button size="lg" className="h-14 px-8 text-lg rounded-full bg-slate-900 text-white hover:bg-slate-800 shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-300">
                Start Compression
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
            <Link href="/how-it-works">
              <Button size="lg" variant="outline" className="h-14 px-8 text-lg rounded-full border-2 hover:bg-slate-50">
                How It Works
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-7xl mx-auto px-6">
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={Zap}
            title="FastAPI Backend"
            desc="Powered by Python's NumPy for lightning-fast matrix computations and instant results."
          />
          <FeatureCard
            icon={Layers} // Changed from Eye
            title="Visual Stacking"
            desc="See exactly how R, G, and B channels are reconstructed and stacked to form the final image."
          />
          <FeatureCard
            icon={BookOpen}
            title="Pedagogical Flow"
            desc="Step-by-step interactive lessons explaining variance, covariance, and eigenvalues."
          />
        </div>
      </section>

      {/* Why Grid */}
      <section className="max-w-7xl mx-auto px-6 bg-slate-900 rounded-[3rem] p-12 md:p-24 text-white text-center space-y-12">
        <h2 className="text-4xl md:text-5xl font-bold font-serif">Why PCA Xpert?</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12 text-center">
          <div>
            <div className="text-5xl font-bold text-blue-400 mb-2">Data</div>
            <p className="text-slate-400 font-medium">Simplification</p>
          </div>
          <div>
            <div className="text-5xl font-bold text-purple-400 mb-2">Noise</div>
            <p className="text-slate-400 font-medium">Reduction</p>
          </div>
          <div>
            <div className="text-5xl font-bold text-green-400 mb-2">Visual</div>
            <p className="text-slate-400 font-medium">Insights</p>
          </div>
          <div>
            <div className="text-5xl font-bold text-amber-400 mb-2">∞</div>
            <p className="text-slate-400 font-medium">Applications</p>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="max-w-3xl mx-auto px-6">
        <h2 className="text-3xl font-bold text-center mb-12 text-slate-800">Frequently Asked Questions</h2>
        <div className="space-y-4">
          {FAQ_ITEMS.map((item, i) => (
            <FAQItem key={i} question={item.question} answer={item.answer} />
          ))}
        </div>
      </section>
    </div>
  )
}

function FeatureCard({ icon: Icon, title, desc }: { icon: any, title: string, desc: string }) {
  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="p-8 rounded-3xl bg-white border border-slate-100 shadow-lg hover:shadow-xl transition-all"
    >
      <div className="w-14 h-14 bg-blue-50 rounded-2xl flex items-center justify-center mb-6 text-blue-600">
        <Icon className="w-7 h-7" />
      </div>
      <h3 className="text-xl font-bold text-slate-800 mb-3">{title}</h3>
      <p className="text-slate-600 leading-relaxed">
        {desc}
      </p>
    </motion.div>
  )
}

function FAQItem({ question, answer }: { question: string, answer: string }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="border border-slate-200 rounded-2xl bg-white overflow-hidden shadow-sm hover:shadow-md transition-shadow">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-6 text-left font-bold text-slate-800 hover:bg-slate-50 transition-colors"
      >
        {question}
        {isOpen ? <Minus className="w-5 h-5 text-blue-500" /> : <Plus className="w-5 h-5 text-slate-400" />}
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
          >
            <div className="p-6 pt-0 text-slate-600 leading-relaxed border-t border-slate-100/50">
              {answer}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
