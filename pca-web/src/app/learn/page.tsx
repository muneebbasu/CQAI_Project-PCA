"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { BookOpen, CheckCircle2, Lock, Play, ArrowRight, Brain, Lightbulb, GraduationCap } from "lucide-react"
import { Button } from "@/components/ui/button"

import { cn } from "@/lib/utils"

const tutorials = [
    {
        id: 1,
        title: "Tutorial 1: Understanding Eigenvalues and Eigenvectors",
        pdf: "/pdfs/tutorial1.pdf",
        quiz: [
            {
                question: "What happens when you multiply a matrix by a vector?",
                options: [
                    "The vector's direction always changes.",
                    "The vector may get rotated or scaled.",
                    "The vector remains unchanged."
                ],
                correct: 1 // Index
            },
            {
                question: "Which of the following is true about eigenvectors?",
                options: [
                    "Eigenvectors change direction when multiplied by a matrix.",
                    "Eigenvectors disappear when multiplied by a matrix.",
                    "Eigenvectors retain their direction but may be scaled."
                ],
                correct: 2
            },
            {
                question: "What does an eigenvalue represent in the context of matrix multiplication with an eigenvector?",
                options: [
                    "The rotation angle of the vector.",
                    "The factor by which the eigenvector is scaled.",
                    "The determinant of the matrix"
                ],
                correct: 1
            }
        ]
    },
    {
        id: 2,
        title: "Tutorial 2: Mathematical Foundation",
        pdf: "/pdfs/tutorial2.pdf",
        quiz: [
            {
                question: "What is Eigenvalue?",
                options: [
                    "A value associated with matrix",
                    "A statistical measure",
                    "A type of variable"
                ],
                correct: 0
            },
            {
                question: "PCA is based on which decomposition?",
                options: [
                    "SVD",
                    "QR Decomposition",
                    "Cholesky Decomposition"
                ],
                correct: 0
            },
            {
                question: "What is the output of PCA?",
                options: [
                    "Principal Components",
                    "Coefficients",
                    "Basis Vectors"
                ],
                correct: 0
            }
        ]
    },
    {
        id: 3,
        title: "Tutorial 3: PCA in Practice",
        pdf: "/pdfs/tutorial3.pdf",
        quiz: [
            {
                question: "What is the main purpose of PCA?",
                options: ["Data compression", "Data classification", "Dimensionality reduction"],
                correct: 2
            },
            {
                question: "Which preprocessing step is important before applying PCA?",
                options: ["Data normalization", "Data encryption", "Data augmentation"],
                correct: 0
            },
            {
                question: "How do you choose the number of principal components?",
                options: ["Based on explained variance ratio", "Always choose half of original dimensions", "Random selection"],
                correct: 0
            }
        ]
    }
]

export default function LearnPage() {
    const [currentTutorial, setCurrentTutorial] = useState(0)
    const [completedTutorials, setCompletedTutorials] = useState<number[]>([])
    const [quizAnswers, setQuizAnswers] = useState<Record<string, number>>({})
    const [showQuiz, setShowQuiz] = useState(false)
    const [quizResult, setQuizResult] = useState<"success" | "failure" | null>(null)

    const activeTutorial = tutorials[currentTutorial]
    const isCompleted = completedTutorials.includes(activeTutorial.id);

    const handleAnswer = (qIndex: number, optionIndex: number) => {
        setQuizAnswers(prev => ({ ...prev, [`${currentTutorial}-${qIndex}`]: optionIndex }))
    }

    const submitQuiz = () => {
        const allCorrect = activeTutorial.quiz.every((q, i) => quizAnswers[`${currentTutorial}-${i}`] === q.correct)
        if (allCorrect) {
            setQuizResult("success")
            if (!completedTutorials.includes(activeTutorial.id)) {
                setCompletedTutorials(prev => [...prev, activeTutorial.id])
            }
        } else {
            setQuizResult("failure")
        }
    }

    return (
        <div className="max-w-6xl mx-auto space-y-8 pb-12">
            {/* Header */}
            <div className="relative bg-gradient-to-r from-blue-600 to-indigo-600 rounded-3xl p-8 md:p-12 text-white overflow-hidden shadow-2xl">
                <div className="absolute top-0 right-0 p-12 opacity-10">
                    <BookOpen className="w-64 h-64" />
                </div>
                <div className="relative z-10 space-y-4">
                    <div className="flex items-center gap-2 text-blue-100 font-medium">
                        <GraduationCap className="w-5 h-5" />
                        <span>Your Progress</span>
                    </div>
                    <h1 className="text-4xl md:text-5xl font-bold font-serif">Master PCA Conceptually</h1>
                    <p className="text-blue-100 max-w-xl text-lg">
                        Step-by-step interactive tutorials designed to take you from beginner to expert.
                    </p>

                    {/* Progress Bar */}
                    <div className="max-w-md mt-6">
                        <div className="flex justify-between text-sm mb-2 font-bold">
                            <span>{Math.round((completedTutorials.length / tutorials.length) * 100)}% Complete</span>
                            <span>{completedTutorials.length}/{tutorials.length} Tutorials</span>
                        </div>
                        <div className="h-3 bg-blue-900/30 rounded-full overflow-hidden backdrop-blur-sm">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${(completedTutorials.length / tutorials.length) * 100}%` }}
                                className="h-full bg-white rounded-full"
                            />
                        </div>
                    </div>
                </div>
            </div>

            <div className="grid lg:grid-cols-4 gap-8">
                {/* Sidebar Navigation */}
                <div className="space-y-4">
                    {tutorials.map((t, i) => {
                        const isLocked = i > 0 && !completedTutorials.includes(tutorials[i - 1].id)
                        const isActive = i === currentTutorial
                        const isDone = completedTutorials.includes(t.id)

                        return (
                            <motion.button
                                key={t.id}
                                whileHover={!isLocked ? { scale: 1.02 } : {}}
                                whileTap={!isLocked ? { scale: 0.98 } : {}}
                                onClick={() => !isLocked && setCurrentTutorial(i)}
                                disabled={isLocked}
                                className={cn(
                                    "w-full text-left p-4 rounded-xl border transition-all duration-300 flex items-center justify-between group shadow-sm",
                                    isActive
                                        ? "border-blue-500 bg-white ring-2 ring-blue-500/20 shadow-blue-200"
                                        : "border-slate-200 bg-white hover:border-blue-300 hover:shadow-md",
                                    isLocked && "opacity-60 cursor-not-allowed bg-slate-50 border-slate-100"
                                )}
                            >
                                <div className="space-y-1">
                                    <div className="text-xs uppercase font-bold tracking-wider text-slate-400">
                                        Lesson {t.id}
                                    </div>
                                    <span className={cn("font-bold block", isActive ? "text-blue-700" : "text-slate-700")}>
                                        {t.title.split(":")[1] || t.title}
                                    </span>
                                </div>
                                {isDone ? (
                                    <div className="bg-green-100 p-1.5 rounded-full">
                                        <CheckCircle2 className="w-4 h-4 text-green-600" />
                                    </div>
                                ) : isLocked ? (
                                    <Lock className="w-4 h-4 text-slate-300" />
                                ) : (
                                    <div className={cn("w-2 h-2 rounded-full", isActive ? "bg-blue-500 animate-pulse" : "bg-slate-300")} />
                                )}
                            </motion.button>
                        )
                    })}
                </div>

                {/* Content */}
                <div className="md:col-span-3 space-y-6">
                    <motion.div
                        key={activeTutorial.id}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm"
                    >
                        <div className="p-6 border-b border-slate-100 flex justify-between items-center">
                            <h2 className="text-xl font-bold text-slate-800">{activeTutorial.title}</h2>
                            <Button variant="outline" onClick={() => setShowQuiz(!showQuiz)}>
                                {showQuiz ? "Hide Quiz" : "Take Quiz"}
                            </Button>
                        </div>

                        <div className="p-1 bg-slate-100 h-[600px]">
                            <iframe src={activeTutorial.pdf} className="w-full h-full rounded-b-xl" />
                        </div>
                    </motion.div>

                    <AnimatePresence>
                        {showQuiz && (
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: 20 }}
                                className="bg-white rounded-2xl border border-slate-200 p-8 shadow-lg"
                            >
                                <h3 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                                    <BookOpen className="w-6 h-6 text-blue-600" /> Quiz Time
                                </h3>

                                <div className="space-y-8">
                                    {activeTutorial.quiz.map((q, i) => (
                                        <div key={i} className="space-y-3">
                                            <p className="font-medium text-lg text-slate-800">Q{i + 1}: {q.question}</p>
                                            <div className="space-y-2">
                                                {q.options.map((opt, optIdx) => (
                                                    <label key={optIdx} className="flex items-center gap-3 p-3 rounded-lg border border-slate-200 hover:bg-slate-50 cursor-pointer transition-colors">
                                                        <input
                                                            type="radio"
                                                            name={`q-${currentTutorial}-${i}`}
                                                            checked={quizAnswers[`${currentTutorial}-${i}`] === optIdx}
                                                            onChange={() => handleAnswer(i, optIdx)}
                                                            className="w-4 h-4 text-blue-600"
                                                        />
                                                        <span className="text-slate-600">{opt}</span>
                                                    </label>
                                                ))}
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                <div className="mt-8 flex items-center gap-4">
                                    <Button onClick={submitQuiz} className="bg-blue-600 hover:bg-blue-700 text-lg px-8">
                                        Submit Answers
                                    </Button>
                                    {quizResult === "success" && (
                                        <span className="text-green-600 font-bold flex items-center gap-2">
                                            <CheckCircle2 className="w-5 h-5" /> Correct! Tutorial Completed.
                                        </span>
                                    )}
                                    {quizResult === "failure" && (
                                        <span className="text-red-600 font-bold flex items-center gap-2">
                                            <AlertCircle className="w-5 h-5" /> Some answers are incorrect. Try again!
                                        </span>
                                    )}
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>



            {/* Resources Section */}
            <div className="mt-20">
                <div className="flex items-center gap-3 mb-8">
                    <div className="bg-purple-100 p-2 rounded-lg">
                        <Brain className="w-6 h-6 text-purple-600" />
                    </div>
                    <h2 className="text-3xl font-bold text-slate-900">External Resources</h2>
                </div>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Wikipedia */}
                    <a href="https://en.wikipedia.org/wiki/Principal_component_analysis" target="_blank" rel="noreferrer" className="group block bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-xl hover:border-blue-300 transition-all">
                        <div className="flex items-start justify-between mb-4">
                            <div className="bg-slate-100 p-3 rounded-xl group-hover:bg-blue-50 transition-colors">
                                <BookOpen className="w-6 h-6 text-slate-600 group-hover:text-blue-600" />
                            </div>
                            <ArrowRight className="w-5 h-5 text-slate-300 group-hover:text-blue-500 -translate-x-2 opacity-0 group-hover:translate-x-0 group-hover:opacity-100 transition-all" />
                        </div>
                        <h3 className="text-lg font-bold text-slate-900 mb-2">Wikipedia Article</h3>
                        <p className="text-slate-500 text-sm leading-relaxed">The definitive technical reference. Covers mathematical derivation, covariance method, and SVD.</p>
                    </a>

                    {/* 3Blue1Brown */}
                    <a href="https://www.youtube.com/watch?v=PFDu9oVAE-g" target="_blank" rel="noreferrer" className="group block bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-xl hover:border-red-300 transition-all">
                        <div className="flex items-start justify-between mb-4">
                            <div className="bg-red-50 p-3 rounded-xl group-hover:bg-red-100 transition-colors">
                                <Play className="w-6 h-6 text-red-600 fill-current" />
                            </div>
                            <ArrowRight className="w-5 h-5 text-slate-300 group-hover:text-red-500 -translate-x-2 opacity-0 group-hover:translate-x-0 group-hover:opacity-100 transition-all" />
                        </div>
                        <h3 className="text-lg font-bold text-slate-900 mb-2">3Blue1Brown: Linear Algebra</h3>
                        <p className="text-slate-500 text-sm leading-relaxed">Essential background on Eigenvectors and Linear Transformations. Visually stunning explanations.</p>
                    </a>

                    {/* StatQuest */}
                    <a href="https://www.youtube.com/watch?v=FgakZw6K1QQ" target="_blank" rel="noreferrer" className="group block bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-xl hover:border-orange-300 transition-all">
                        <div className="flex items-start justify-between mb-4">
                            <div className="bg-orange-50 p-3 rounded-xl group-hover:bg-orange-100 transition-colors">
                                <Play className="w-6 h-6 text-orange-600 fill-current" />
                            </div>
                            <ArrowRight className="w-5 h-5 text-slate-300 group-hover:text-orange-500 -translate-x-2 opacity-0 group-hover:translate-x-0 group-hover:opacity-100 transition-all" />
                        </div>
                        <h3 className="text-lg font-bold text-slate-900 mb-2">StatQuest: PCA</h3>
                        <p className="text-slate-500 text-sm leading-relaxed">"Double Bam!" A gentle, step-by-step introduction making the math accessible to everyone.</p>
                    </a>

                    {/* Google Search */}
                    <a href="https://www.google.com/search?q=principal+component+analysis+tutorial" target="_blank" rel="noreferrer" className="group block bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-xl hover:border-green-300 transition-all">
                        <div className="flex items-start justify-between mb-4">
                            <div className="bg-green-50 p-3 rounded-xl group-hover:bg-green-100 transition-colors">
                                <Lightbulb className="w-6 h-6 text-green-600" />
                            </div>
                            <ArrowRight className="w-5 h-5 text-slate-300 group-hover:text-green-500 -translate-x-2 opacity-0 group-hover:translate-x-0 group-hover:opacity-100 transition-all" />
                        </div>
                        <h3 className="text-lg font-bold text-slate-900 mb-2">Google Resources</h3>
                        <p className="text-slate-500 text-sm leading-relaxed">Browse the latest tutorials, articles, and discussions on PCA across the web.</p>
                    </a>

                    {/* Setosa Visualization */}
                    <a href="https://setosa.io/ev/principal-component-analysis/" target="_blank" rel="noreferrer" className="group block bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-xl hover:border-indigo-300 transition-all">
                        <div className="flex items-start justify-between mb-4">
                            <div className="bg-indigo-50 p-3 rounded-xl group-hover:bg-indigo-100 transition-colors">
                                <Brain className="w-6 h-6 text-indigo-600" />
                            </div>
                            <ArrowRight className="w-5 h-5 text-slate-300 group-hover:text-indigo-500 -translate-x-2 opacity-0 group-hover:translate-x-0 group-hover:opacity-100 transition-all" />
                        </div>
                        <h3 className="text-lg font-bold text-slate-900 mb-2">Setosa.io Visualization</h3>
                        <p className="text-slate-500 text-sm leading-relaxed">A famous interactive article where you can play with 2D and 3D data points.</p>
                    </a>
                </div>
            </div>
        </div>
    )
}
