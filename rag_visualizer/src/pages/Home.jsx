import React, { useState, useEffect } from "react"
import {
  motion,
  useScroll,
  useTransform,
  useSpring,
  useMotionValue,
} from "framer-motion"
import { NavLink } from "react-router-dom"
import {
  SiPypi,
  SiPython,
  SiDocker,
  SiFastapi,
  SiPostgresql,
} from "react-icons/si"
import {
  ArrowRight,
  Database,
  Brain,
  Zap,
  Layers,
  Terminal,
  Star,
  GitFork,
  Scale,
  Code,
  Command,
  Box,
  Check,
  Cpu,
  Workflow,
  Search,
  MessageSquare,
  FileText,
} from "lucide-react"
import TechMarquee from "../components/TechMarquee"

const Home = () => {
  const { scrollYProgress } = useScroll()
  const scale = useTransform(scrollYProgress, [0, 0.2], [1, 0.9])
  const opacity = useTransform(scrollYProgress, [0, 0.2], [1, 0.5])
  const [stats, setStats] = useState({ stars: 0, forks: 0, loading: true })

  const command = "pip install ultimaterag"
  const [copied, setCopied] = useState(false)

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(command)
      setCopied(true)

      setTimeout(() => {
        setCopied(false)
      }, 2000)
    } catch (err) {
      console.error("Copy failed", err)
    }
  }

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(
          "https://api.github.com/repos/Matrixxboy/TheUnltimateRAG"
        )
        if (response.ok) {
          const data = await response.json()
          setStats({
            stars: data.stargazers_count,
            forks: data.forks_count,
            loading: false,
          })
        } else {
          setStats((prev) => ({ ...prev, loading: false }))
        }
      } catch (error) {
        console.error("Failed to fetch GitHub stats", error)
        setStats((prev) => ({ ...prev, loading: false }))
      }
    }
    fetchStats()
  }, [])

  // Mouse Follow Logic for Parallax Background
  const mouseX = useMotionValue(0)
  const mouseY = useMotionValue(0)

  const handleMouseMove = (e) => {
    const { clientX, clientY } = e
    const moveX = clientX - window.innerWidth / 2
    const moveY = clientY - window.innerHeight / 2
    mouseX.set(moveX)
    mouseY.set(moveY)
  }

  const springX = useSpring(mouseX, { stiffness: 50, damping: 20 })
  const springY = useSpring(mouseY, { stiffness: 50, damping: 20 })

  const moveBackgroundX = useTransform(springX, (value) => value / 20)
  const moveBackgroundY = useTransform(springY, (value) => value / 20)
  const moveBackgroundXReverse = useTransform(springX, (value) => -value / 30)
  const moveBackgroundYReverse = useTransform(springY, (value) => -value / 30)

  return (
    <div
      className="min-h-screen pt-28 overflow-x-hidden"
      onMouseMove={handleMouseMove}
    >
      {/* Hero Section */}
      <section className="min-h-[85vh] flex flex-col items-center justify-center relative px-6 text-center">
        <motion.div
          style={{ scale, opacity }}
          className="z-10 w-full max-w-5xl mx-auto"
          >
          <div className="flex flex-col items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="mb-8 w-[300px] flex flex-col items-center justify-center gap-2"
          >
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900/5 text-slate-600 text-sm font-semibold border border-slate-200 backdrop-blur-sm cursor-default hover:bg-slate-100 transition-colors">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              v1.0 Production Ready
            </span>
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900/5 text-slate-600 text-sm font-semibold border border-slate-200 backdrop-blur-sm cursor-default hover:bg-slate-100 transition-colors">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-yellow-500"></span>
              </span>
              Developement Status : 3 - Alpha
            </span>
          </motion.div>
        </div>
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="flex mb-8 items-center justify-center"
          >
            <img
              src="/mainLOGO.png"
              alt="TUG Logo"
              className="md:w-48 md:h-48 w-32 h-32 drop-shadow-2xl hover:scale-105 transition-transform duration-300"
            />
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
            className="text-6xl md:text-8xl font-bold text-slate-900 tracking-tight mb-8"
          >
            The Ultimate
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 ml-3 inline-block hover:scale-105 transition-transform cursor-default">
              RAG
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4, ease: "easeOut" }}
            className="text-xl md:text-2xl text-slate-600 max-w-3xl mx-auto mb-12 leading-relaxed"
          >
            A production-grade framework for Retrieval Augmented Generation.{" "}
            <br className="hidden md:block" />
            <span className="text-slate-500 text-lg mt-2 block">
              Modular. Scalable. Developer-First.
            </span>
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6, ease: "easeOut" }}
            className="flex flex-col md:flex-row items-center justify-center gap-6 mb-16"
          >
            {/* Demo Button - Visible on Mobile */}
            <NavLink
              to="/demo"
              className="w-full md:w-auto bg-slate-900 text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-slate-800 transition-all shadow-xl hover:shadow-2xl hover:scale-105 flex items-center justify-center gap-2 md:hidden"
            >
              View Live Demo
              <ArrowRight className="w-5 h-5" />
            </NavLink>

            {/* Terminal Command - Interactive */}
            <div className="w-full md:w-auto group relative">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full opacity-30 blur group-hover:opacity-60 transition duration-300"></div>
              <div
                onClick={copyToClipboard}
                className="relative flex items-center bg-zinc-900 border border-zinc-800 rounded-full px-6 py-4 font-mono text-zinc-300 text-sm shadow-2xl md:min-w-[420px] cursor-pointer hover:bg-zinc-800 transition-colors"
                role="button"
                aria-label="Copy install command"
              >
                <div className="flex items-center gap-2 mr-3 border-r border-zinc-700 pr-3">
                  <SiPypi className="w-5 h-5 text-zinc-400" />
                  <span className="text-zinc-500 select-none">$</span>
                </div>

                <div className="flex-1 text-left font-medium">{command}</div>

                <div
                  className={`ml-4 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider transition-all duration-200 ${
                    copied
                      ? "text-emerald-400"
                      : "text-indigo-400 group-hover:text-indigo-300"
                  }`}
                >
                  {copied ? (
                    <>
                      <Check className="w-3.5 h-3.5" />
                      <span>Copied</span>
                    </>
                  ) : (
                    <span className="opacity-0 group-hover:opacity-100 transition-opacity">
                      Copy
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Action Buttons - Desktop */}
            <div className="hidden md:flex gap-4">
              <NavLink
                to="/docs"
                className="px-6 py-4 rounded-full font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors border border-transparent hover:border-slate-200"
              >
                Documentation
              </NavLink>
              <NavLink
                to="/demo"
                className="px-6 py-4 rounded-full bg-slate-100 font-semibold text-slate-900 hover:bg-slate-200 transition-colors flex items-center gap-2"
              >
                Live Demo <ArrowRight className="w-4 h-4" />
              </NavLink>
            </div>
          </motion.div>
        </motion.div>

        {/* Abstract Interactive Background */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden -z-10">
          <motion.div
            style={{ x: moveBackgroundX, y: moveBackgroundY }}
            className="absolute top-20 left-10 w-[500px] h-[500px] bg-purple-200/40 rounded-full mix-blend-multiply filter blur-[120px] opacity-70"
          />
          <motion.div
            style={{ x: moveBackgroundXReverse, y: moveBackgroundYReverse }}
            className="absolute bottom-40 right-10 w-[600px] h-[600px] bg-blue-200/30 rounded-full mix-blend-multiply filter blur-[120px] opacity-70"
          />
        </div>
      </section>

      {/* Tech Marquee - Adds dynamic movement */}
      <TechMarquee />

      {/* Architecture Flow Section (New interaction) */}
      <section className="py-24 px-6 bg-white relative">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              How TUG Works
            </h2>
            <p className="text-slate-600 max-w-2xl mx-auto">
              A seamless pipeline from document to answer. Visualize the flow of
              data through our modular architecture.
            </p>
          </div>

          <div className="relative">
            {/* Connection Line */}
            <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-slate-200 to-transparent -translate-y-1/2 z-0"></div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative z-10">
              <FlowStep
                icon={FileText}
                step="01"
                title="Ingest"
                desc="Parse PDF, TXT, or MD files via CLI or API. Content is automatically cleaned and chunked."
              />
              <FlowStep
                icon={Database}
                step="02"
                title="Embed & Store"
                desc="Generate embeddings using OpenAI or local models. Store vectors in Chroma or Pinecone."
              />
              <FlowStep
                icon={Search}
                step="03"
                title="Retrieve"
                desc="Semantic search finds the most relevant context chunks for the user's query."
              />
              <FlowStep
                icon={MessageSquare}
                step="04"
                title="Generate"
                desc="LLM synthesizes the retrieved context into a precise, cited answer."
              />
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section with Glassmorphism */}
      <section className="py-12 px-6">
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 p-8 bg-slate-900 rounded-3xl text-white shadow-2xl relative overflow-hidden"
          >
            {/* Background glow */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/20 blur-[80px] rounded-full pointer-events-none"></div>

            <StatItem
              icon={Star}
              label="GitHub Stars"
              value={stats.loading ? "..." : stats.stars}
              color="text-yellow-400"
            />
            <StatItem
              icon={GitFork}
              label="Forks"
              value={stats.loading ? "..." : stats.forks}
              color="text-blue-400"
            />
            <StatItem
              icon={Scale}
              label="License"
              value="MIT"
              color="text-green-400"
            />
            <StatItem
              icon={SiPython}
              label="100% Python"
              value="v3.10+"
              color="text-yellow-300"
            />
          </motion.div>
        </div>
      </section>

      {/* Features Grid - Enhanced */}
      <section className="py-24 px-6 bg-slate-50 relative overflow-hidden">
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="mb-20 text-center max-w-3xl mx-auto">
            <h2 className="text-4xl font-bold text-slate-900 mb-6">
              Engineered for Production
            </h2>
            <p className="text-lg text-slate-600">
              We've handled the complexities of RAG architectures so you don't
              have to. Scalable, modular, and ready for deployment.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <FeatureCard
              icon={Database}
              title="Vector Stores"
              desc="Pre-configured integrations with ChromaDB, Pinecone, and more. Switch providers with a single config change."
              badge="Flexible"
            />
            <FeatureCard
              icon={Brain}
              title="LLM Agnostic"
              desc="Drop-in support for OpenAI, Anthropic, or local LLMs via Ollama. You choose the intelligence."
              badge="Powerful"
            />
            <FeatureCard
              icon={Zap}
              title="Smart Ingestion"
              desc="Robust processing pipeline for documents. Handles parsing, cleaning, and chunking automatically."
              badge="Fast"
            />
            <FeatureCard
              icon={Layers}
              title="Modular API"
              desc="Built on FastAPI. Fully typed, documented (OpenAPI), and ready to extend with custom endpoints."
              badge="Modern"
            />
            <FeatureCard
              icon={Terminal}
              title="Developer CLI"
              desc="Powerful command-line tools for ingestion, server management, and system diagnostics."
            />
            <FeatureCard
              icon={Box}
              title="Containerized"
              desc="One-command startup with Docker Compose. Service isolation for database, API, and frontend."
            />
            <FeatureCard
              icon={Workflow}
              title="Workflows"
              desc="Create complex agentic workflows with self-correction and multi-step reasoning capabilities."
              badge="New"
            />
            <FeatureCard
              icon={Search}
              title="Hybrid Search"
              desc="Combine keyword search with semantic search for optimal retrieval accuracy."
            />
            <FeatureCard
              icon={Cpu}
              title="Observation"
              desc="Full visibility into the RAG pipeline. Trace requests, view retrieved chunks, and debug in real-time."
              badge="Insight"
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 px-6">
        <div className="max-w-6xl mx-auto relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-[2.5rem] opacity-30 blur-lg group-hover:opacity-50 transition duration-1000"></div>
          <div className="bg-slate-900 rounded-[2.5rem] p-12 md:p-24 relative overflow-hidden text-center isolate">
            <div className="absolute top-0 left-0 w-full h-full -z-10">
              {/* Animated grain or gradient could go here */}
              <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-purple-900/40 via-slate-900 to-slate-900"></div>
              <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-indigo-500/10 rounded-full blur-[100px]"></div>
            </div>

            <h2 className="text-4xl md:text-6xl font-bold text-white mb-8 tracking-tight">
              Ready to ship your RAG?
            </h2>
            <p className="text-xl text-slate-300 mb-12 max-w-2xl mx-auto">
              Stop fighting with boilerplate. Start building intelligent
              features users love.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
              <NavLink
                to="/demo"
                className="w-full sm:w-auto bg-white text-slate-900 px-10 py-5 rounded-full font-bold text-lg hover:bg-indigo-50 transition-colors shadow-lg shadow-white/10"
              >
                Start Building Now
              </NavLink>
              <NavLink
                to="/contact"
                className="w-full sm:w-auto px-10 py-5 rounded-full font-medium text-lg text-white border border-white/20 hover:bg-white/10 transition-colors backdrop-blur-sm"
              >
                Contact Sales
              </NavLink>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

// --- Sub Components ---

const StatItem = ({ icon: Icon, label, value, color }) => (
  <div className="flex flex-col items-center justify-center p-4 rounded-2xl transition-colors hover:bg-white/5">
    <div className="flex items-center gap-3 text-white font-bold text-3xl mb-1">
      <Icon size={24} className={color || "text-indigo-400"} />
      {value}
    </div>
    <div className="text-xs font-semibold text-slate-400 uppercase tracking-widest">
      {label}
    </div>
  </div>
)

const FlowStep = ({ icon: Icon, step, title, desc }) => (
  <motion.div
    whileHover={{ y: -5 }}
    className="flex flex-col items-center text-center bg-white p-6 rounded-2xl border border-slate-100 shadow-sm relative z-10 group"
  >
    <div className="w-16 h-16 bg-slate-50 rounded-2xl flex items-center justify-center mb-6 border border-slate-100 group-hover:bg-indigo-50 group-hover:border-indigo-100 transition-colors">
      <Icon className="w-8 h-8 text-slate-400 group-hover:text-indigo-600 transition-colors" />
    </div>
    <span className="text-slate-200 font-black text-6xl absolute top-4 right-4 opacity-20 select-none group-hover:text-indigo-100 transition-colors -z-10">
      {step}
    </span>

    <h3 className="text-xl font-bold text-slate-900 mb-3">{title}</h3>
    <p className="text-slate-500 text-sm leading-relaxed">{desc}</p>
  </motion.div>
)

const FeatureCard = ({ icon: Icon, title, desc, badge }) => (
  <motion.div
    whileHover={{ y: -8, scale: 1.02 }}
    className="relative p-8 rounded-3xl bg-white border border-slate-200/60 shadow-lg shadow-slate-200/50 hover:shadow-2xl hover:shadow-indigo-500/10 transition-all cursor-default overflow-hidden group"
  >
    {/* Decoration gradient */}
    <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-bl-[100px] -mr-8 -mt-8 transition-transform group-hover:scale-150 duration-500"></div>

    <div className="relative">
      <div className="flex justify-between items-start mb-6">
        <div className="w-14 h-14 bg-white border border-slate-100 rounded-2xl flex items-center justify-center shadow-sm group-hover:scale-110 transition-transform duration-300">
          <Icon size={28} className="text-indigo-600" />
        </div>
        {badge && (
          <span className="px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-bold rounded-full uppercase tracking-wide">
            {badge}
          </span>
        )}
      </div>

      <h3 className="text-xl font-bold text-slate-900 mb-3 group-hover:text-indigo-700 transition-colors">
        {title}
      </h3>
      <p className="text-slate-600 leading-relaxed text-sm">{desc}</p>
    </div>
  </motion.div>
)

export default Home
