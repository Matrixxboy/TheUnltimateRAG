import React, { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  Book,
  Code,
  Terminal,
  AlertCircle,
  CheckCircle,
  Cpu,
  Database,
  Layers,
  Search,
  Menu,
  X,
  ChevronRight,
  Copy,
  ChevronDown,
} from "lucide-react"
import { Link } from "react-router-dom"

const Docs = () => {
  const [activeSection, setActiveSection] = useState("introduction")
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const scrollToSection = (id) => {
    const element = document.getElementById(id)
    if (element) {
      const yOffset = -100
      const y = element.getBoundingClientRect().top + window.scrollY + yOffset
      window.scrollTo({ top: y, behavior: "smooth" })
      setActiveSection(id)
      setMobileMenuOpen(false)
    }
  }

  useEffect(() => {
    const handleScroll = () => {
      const sections = [
        "introduction",
        "getting-started",
        "core-concepts",
        "api-reference",
        "troubleshooting",
      ]
      for (const section of sections) {
        const element = document.getElementById(section)
        if (element) {
          const rect = element.getBoundingClientRect()
          if (rect.top >= 0 && rect.top <= 300) {
            setActiveSection(section)
            break
          }
        }
      }
    }
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const sidebarLinks = [
    { id: "introduction", label: "Introduction", icon: Book },
    { id: "getting-started", label: "Getting Started", icon: Layers },
    { id: "core-concepts", label: "Core Concepts", icon: Cpu },
    { id: "api-reference", label: "API Reference", icon: Code },
    { id: "troubleshooting", label: "Troubleshooting", icon: AlertCircle },
  ]

  return (
    /* FIX 1 & 2: Added max-w-[100vw] and overflow-x-hidden. 
           Removed 'flex-col' for mobile (default block is safer) */
    <div className="min-h-screen w-full max-w-[100vw] overflow-x-hidden pt-20 md:pt-24 pb-12 px-4 md:px-8 mx-auto md:flex md:gap-8 relative bg-slate-50/30">
      {/* Mobile Menu Toggle */}
      <button
        className="md:hidden fixed bottom-6 right-6 z-50 bg-slate-900 text-white p-4 rounded-full shadow-xl hover:bg-slate-800 transition-transform active:scale-95"
        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        aria-label="Toggle Menu"
      >
        {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Mobile Backdrop */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-30 md:hidden"
            onClick={() => setMobileMenuOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Sidebar Navigation */}
      <aside
        className={`
                fixed inset-y-0 left-0 z-40 w-[280px] bg-white border-r border-slate-200 shadow-2xl 
                transform transition-transform duration-300 ease-in-out 
                md:transform-none md:static md:bg-transparent md:border-none md:w-64 md:shadow-none shrink-0
                ${mobileMenuOpen ? "translate-x-0" : "-translate-x-full"}
            `}
      >
        <div className="h-full overflow-y-auto md:overflow-visible pt-24 md:pt-0 pb-8 px-6 md:px-0 md:sticky md:top-24 space-y-1">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 px-2">
            Documentation
          </h3>
          <nav className="space-y-1">
            {sidebarLinks.map((link) => (
              <button
                key={link.id}
                onClick={() => scrollToSection(link.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                  activeSection === link.id
                    ? "bg-indigo-50 text-indigo-600 shadow-sm ring-1 ring-indigo-100"
                    : "text-slate-600 hover:bg-white/60 hover:text-slate-900"
                }`}
              >
                <link.icon
                  size={18}
                  className={
                    activeSection === link.id
                      ? "text-indigo-600"
                      : "text-slate-400"
                  }
                />
                {link.label}
              </button>
            ))}
          </nav>

          <div className="mt-8 px-2">
            <div className="p-4 rounded-xl bg-gradient-to-br from-indigo-600 to-violet-600 text-white shadow-lg">
              <h4 className="font-bold flex items-center gap-2 mb-2 text-sm">
                <Terminal size={16} /> Need help?
              </h4>
              <p className="text-xs text-indigo-100 mb-3 leading-relaxed opacity-90">
                Check our detailed guides or contact support for assistance.
              </p>
              <Link
                to="/contact"
                className="text-xs bg-white/10 hover:bg-white/20 border border-white/10 px-3 py-2 rounded-lg transition-colors block text-center w-full font-medium"
              >
                Contact Support
              </Link>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      {/* FIX 3: Added min-w-0 to prevent flex blowout and w-full */}
      <main className="flex-1 w-full min-w-0 space-y-16 pb-24 md:pb-0">
        <Section id="introduction" title="Introduction">
          <p className="text-lg text-slate-600 leading-relaxed mb-8">
            Welcome to the <strong>The Ultimate RAG (TUG)</strong>{" "}
            documentation. This visualizer tool bridges the gap between complex
            AI concepts and understandable visual representations.
          </p>

          <div className="space-y-6 md:space-y-8 mb-12">
            <div className="glass-panel p-6 border-l-4 border-l-red-400 bg-white shadow-sm rounded-xl">
              <h3 className="text-lg font-bold text-slate-800 mb-2">
                The Problem: Hallucinations
              </h3>
              <p className="text-slate-600 leading-relaxed text-sm">
                LLMs often confidently invent facts ("hallucinate") when asked
                about recent events or private data because they don't know what
                they don't know.
              </p>
            </div>

            <div className="glass-panel p-6 border-l-4 border-l-emerald-500 bg-white shadow-sm rounded-xl">
              <h3 className="text-lg font-bold text-slate-800 mb-2">
                The Solution: RAG
              </h3>
              <div className="text-slate-600 leading-relaxed text-sm">
                RAG gives the LLM an "open book" exam by retrieving facts before
                generating an answer.
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FeatureCard
              icon={Database}
              title="Vector Database"
              description="Visualize how text is converted into numbers (embeddings) and stored in high-dimensional space."
            />
            <FeatureCard
              icon={Search}
              title="Semantic Search"
              description="See how the AI finds relevant info by matching meaning rather than just keywords."
            />
          </div>
        </Section>

        <Section id="getting-started" title="Getting Started">
          <div className="space-y-6">
            <Step index="1" title="Upload Documents">
              <div className="mb-2">Upload your PDF, TXT, or MD files.</div>
              <ul className="text-xs text-slate-500 list-disc pl-5 space-y-1">
                <li>
                  <strong>Chunking:</strong> Splitting text into pieces.
                </li>
                <li>
                  <strong>Embedding:</strong> Converting text to vectors.
                </li>
              </ul>
            </Step>
            <Step index="2" title="Configure Embeddings">
              Choose your preferred embedding model (e.g., OpenAI, HuggingFace).
            </Step>
            <Step index="3" title="Run a Query">
              Type a natural language question in the search bar.
            </Step>
          </div>
        </Section>

        <Section id="core-concepts" title="Core Concepts">
          <div className="space-y-12">
            <div>
              <h3 className="text-lg font-bold text-slate-800 mb-4">
                1. Embeddings & Vector Space
              </h3>
              <div className="glass-panel p-6 bg-white rounded-xl shadow-sm border border-slate-100">
                <p className="font-mono text-sm text-slate-600 mb-3">
                  "The cat sits on the mat"
                </p>
                {/* Scrollable vector array */}
                <div className="flex items-center gap-2 text-xs font-mono text-indigo-500 overflow-x-auto pb-2 scrollbar-hide">
                  <span className="bg-slate-50 px-2 py-1 rounded border border-slate-200 shadow-sm shrink-0">
                    [0.12,
                  </span>
                  <span className="bg-slate-50 px-2 py-1 rounded border border-slate-200 shadow-sm shrink-0">
                    -0.45,
                  </span>
                  <span className="bg-slate-50 px-2 py-1 rounded border border-slate-200 shadow-sm shrink-0">
                    0.88,
                  </span>
                  <span className="bg-slate-50 px-2 py-1 rounded border border-slate-200 shadow-sm shrink-0">
                    ...
                  </span>
                  <span className="bg-slate-50 px-2 py-1 rounded border border-slate-200 shadow-sm shrink-0">
                    0.03]
                  </span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-bold text-slate-800 mb-4">
                2. The RAG Workflow
              </h3>
              <div className="glass-panel p-4 bg-white rounded-xl shadow-sm border border-slate-100">
                <div className="flex flex-col md:flex-row items-center justify-center gap-4 p-2">
                  <ConceptNode
                    label="User Query"
                    color="bg-blue-50 text-blue-700 border-blue-200"
                  />
                  <Arrow />
                  <ConceptNode
                    label="Retrieval"
                    color="bg-purple-50 text-purple-700 border-purple-200"
                  />
                  <Arrow />
                  <ConceptNode
                    label="Augmentation"
                    color="bg-amber-50 text-amber-700 border-amber-200"
                  />
                  <Arrow />
                  <ConceptNode
                    label="Generation"
                    color="bg-emerald-50 text-emerald-700 border-emerald-200"
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="mt-12">
            <h3 className="text-lg font-bold text-slate-800 mb-4">
              Comparison Table
            </h3>
            <div className="w-full overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse min-w-[600px]">
                  <thead>
                    <tr className="bg-slate-50 border-b border-slate-100 text-slate-500 text-xs uppercase tracking-wider">
                      <th className="p-4 font-semibold">Feature</th>
                      <th className="p-4 font-semibold">Fine-Tuning</th>
                      <th className="p-4 font-semibold text-purple-600">
                        RAG (TUG)
                      </th>
                    </tr>
                  </thead>
                  <tbody className="text-sm text-slate-600 divide-y divide-slate-100">
                    <tr>
                      <td className="p-4 font-medium text-slate-800">Note</td>
                      <td className="p-4">Teaching new behavior</td>
                      <td className="p-4 bg-purple-50/30 text-purple-700 font-medium">
                        Providing new facts
                      </td>
                    </tr>
                    <tr>
                      <td className="p-4 font-medium text-slate-800">
                        Freshness
                      </td>
                      <td className="p-4">Static</td>
                      <td className="p-4 bg-purple-50/30 text-purple-700 font-medium">
                        Real-time
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </Section>

        <Section id="api-reference" title="API Reference">
          <p className="text-slate-600 mb-6">
            Integrate TUG directly into your application.
          </p>
          <CodeBlock
            title="Querying the Knowledge Base"
            code={`const response = await fetch('https://api.tug.com/v1/query', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer KEY'
  },
  body: JSON.stringify({
    query: "How does vector search work?",
    top_k: 5
  })
});`}
          />
        </Section>

        <Section id="troubleshooting" title="Troubleshooting">
          <div className="space-y-4">
            <TroubleshootItem
              question="Why are my results irrelevant?"
              answer="Check your chunk size (too small = no context) and ensure your embedding model matches your domain."
            />
            <TroubleshootItem
              question="The visualizer is slow."
              answer="Enable hardware acceleration for WebGL rendering."
            />
          </div>
        </Section>
      </main>
    </div>
  )
}

// --- Subcomponents ---

const Section = ({ id, title, children }) => (
  <section id={id} className="scroll-mt-24 md:scroll-mt-28">
    <h2 className="text-2xl font-bold text-slate-900 mb-6 pb-2 border-b border-slate-200/60">
      {title}
    </h2>
    <div className="space-y-6">{children}</div>
  </section>
)

const FeatureCard = ({ icon: Icon, title, description }) => (
  <div className="p-6 bg-white rounded-xl border border-slate-200/60 shadow-sm hover:shadow-md transition-shadow">
    <div className="w-10 h-10 bg-indigo-50 rounded-lg flex items-center justify-center text-indigo-600 mb-3">
      <Icon size={20} />
    </div>
    <h3 className="font-semibold text-slate-800 mb-1">{title}</h3>
    <p className="text-slate-500 text-sm leading-relaxed">{description}</p>
  </div>
)

const Step = ({ index, title, children }) => (
  <div className="flex gap-4">
    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-sm shadow-md">
      {index}
    </div>
    <div>
      <h4 className="font-semibold text-slate-800 mb-1">{title}</h4>
      <div className="text-slate-600 text-sm leading-relaxed">{children}</div>
    </div>
  </div>
)

const ConceptNode = ({ label, color }) => (
  <div
    className={`px-6 py-3 rounded-lg border ${color} font-medium text-sm shadow-sm w-full md:w-auto text-center`}
  >
    {label}
  </div>
)

const Arrow = () => (
  <div className="text-slate-300">
    <ChevronRight size={20} className="hidden md:block" />
    <ChevronDown size={20} className="block md:hidden" />
  </div>
)

const CodeBlock = ({ title, code }) => {
  const [copied, setCopied] = useState(false)
  const handleCopy = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="rounded-xl overflow-hidden border border-slate-200 shadow-sm bg-slate-900 w-full max-w-full">
      <div className="flex items-center justify-between px-4 py-2 bg-slate-800 border-b border-slate-700">
        <span className="text-xs font-mono text-slate-400 truncate">
          {title}
        </span>
        <button
          onClick={handleCopy}
          className="text-slate-400 hover:text-white"
        >
          {copied ? (
            <CheckCircle size={14} className="text-emerald-400" />
          ) : (
            <Copy size={14} />
          )}
        </button>
      </div>
      {/* Added overflow-x-auto to wrapper to contain long lines */}
      <div className="p-4 overflow-x-auto">
        <pre className="text-sm font-mono text-slate-300">
          <code>{code}</code>
        </pre>
      </div>
    </div>
  )
}

const TroubleshootItem = ({ question, answer }) => {
  const [isOpen, setIsOpen] = useState(false)
  return (
    <div className="border border-slate-200 rounded-xl bg-white overflow-hidden shadow-sm">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 text-left hover:bg-slate-50 transition-colors"
      >
        <span className="font-medium text-slate-800 text-sm pr-4">
          {question}
        </span>
        <ChevronRight
          size={18}
          className={`text-slate-400 transition-transform ${
            isOpen ? "rotate-90" : ""
          }`}
        />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: "auto" }}
            exit={{ height: 0 }}
            className="overflow-hidden"
          >
            <div className="p-4 pt-0 text-slate-600 text-sm bg-slate-50/50 border-t border-slate-100">
              {answer}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default Docs