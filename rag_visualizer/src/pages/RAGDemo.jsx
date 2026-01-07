import React, { useState } from "react"
import {
  Network,
  BarChart3,
  Users,
  PlayCircle,
  Share2,
  Search,
  ArrowUpRight,
} from "lucide-react"
import IngestionPanel from "../components/IngestionPanel"
import ChatPanel from "../components/ChatPanel"
import VectorSpace from "../components/VectorSpace"
import AnalyticsPanel from "../components/AnalyticsPanel"
import MaintenanceScreen from "../components/MaintenanceScreen"
import { v4 as uuidv4 } from "uuid"

const RAGDemo = () => {
  const [activeTab, setActiveTab] = useState("personal")
  const [visualizationData, setVisualizationData] = useState(null)
  const [messages, setMessages] = useState([])
  const [sessionId] = React.useState(uuidv4())

  const renderContent = () => {
    switch (activeTab) {
      case "personal":
        return (
          <div className="grid grid-cols-12 gap-6 animate-in fade-in duration-500">
            {/* Sidebar: 4 Columns */}
            <div className="col-span-12 lg:col-span-4 space-y-6 h-full flex flex-col">
              <IngestionPanel accessLevel="private" />
              <div className="flex-1 min-h-0">
                <ChatPanel
                  setVisualizationData={setVisualizationData}
                  messages={messages}
                  setMessages={setMessages}
                  sessionId={sessionId}
                />
              </div>
            </div>

            {/* Main Content: 8 Columns */}
            <div className="col-span-12 lg:col-span-8 space-y-6 h-full">
              <VectorSpace data={visualizationData} />
              {/* Detailed Status Panel */}
              <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-purple-500 bg-purple-50/50 flex flex-col md:flex-row items-center justify-between gap-4">
                <div>
                  <h3 className="font-semibold text-slate-800 flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                    Workspace Active
                  </h3>
                  <p className="text-sm text-slate-500">
                    Data ingestion pipeline is ready. Upload documents to see
                    vector embeddings in real-time.
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <div className="text-xs px-2 py-1 rounded bg-slate-200 text-slate-600 font-mono">
                    ID: {sessionId.slice(0, 8)}
                  </div>
                  <span className="bg-white px-3 py-1 rounded-full text-xs font-medium text-purple-600 border border-purple-100 shadow-sm">
                    Ready
                  </span>
                </div>
              </div>
            </div>
          </div>
        )
      case "common":
        return (
          <div className="grid grid-cols-12 gap-6 animate-in fade-in duration-500">
            {/* Sidebar: 4 Columns */}
            <div className="col-span-12 lg:col-span-4 space-y-6 h-full flex flex-col">
              <IngestionPanel accessLevel="common" />
              <div className="flex-1 min-h-0">
                <ChatPanel
                  setVisualizationData={setVisualizationData}
                  messages={messages}
                  setMessages={setMessages}
                  sessionId={sessionId}
                />
              </div>
            </div>

            {/* Main Content: 8 Columns */}
            <div className="col-span-12 lg:col-span-8 space-y-6 h-full">
              <div className="glass-panel p-6 rounded-2xl mb-6 border-l-4 border-l-blue-500 bg-white/80">
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-xl font-bold mb-2 text-slate-800 flex items-center gap-2">
                      <Users size={20} className="text-blue-500" />
                      Common Knowledge Base
                    </h2>
                    <p className="text-sm text-slate-500 max-w-xl">
                      Files uploaded here are accessible to all users. Use this
                      for shared documentation, guidelines, or public datasets.
                    </p>
                  </div>
                  <button className="text-xs flex items-center gap-1 text-blue-600 hover:text-blue-800 font-medium bg-blue-50 px-3 py-1.5 rounded-lg transition-colors">
                    <Share2 size={12} /> Share Access
                  </button>
                </div>
              </div>

              {/* Enhanced Placeholder for Visualizer */}
              <div className="relative">
                <VectorSpace data={visualizationData} />
                {!visualizationData && (
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                    {/* Optional empty state hint if desired, though VectorSpace handles empty state too */}
                  </div>
                )}
              </div>
            </div>
          </div>
        )
      case "analytics":
        return (
          <div className="grid grid-cols-12 gap-6 animate-in fade-in duration-500">
            {/* Left Column: 6 Columns */}
            <div className="col-span-12 lg:col-span-6 space-y-6">
              <AnalyticsPanel visualizationData={visualizationData} />

              {!visualizationData && (
                <div className="glass-panel p-6 rounded-2xl border-dashed border-2 border-slate-200 bg-slate-50/50 flex flex-col items-center justify-center text-center py-12">
                  <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center text-indigo-500 mb-4">
                    <BarChart3 size={24} />
                  </div>
                  <h4 className="font-semibold text-slate-700">
                    No Analytics Data Yet
                  </h4>
                  <p className="text-sm text-slate-500 max-w-xs mt-2">
                    Perform a query in the Personal or Common tab to generate
                    retrieval metrics.
                  </p>
                </div>
              )}
            </div>

            {/* Right Column: 6 Columns */}
            <div className="col-span-12 lg:col-span-6 space-y-6">
              <VectorSpace data={visualizationData} />
              <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-indigo-500 bg-white/80">
                <h3 className="text-lg font-bold mb-2 text-slate-800">
                  Performance Insights
                </h3>
                <p className="text-sm text-slate-500">
                  View real-time retrieval latency, token usage, and embedding
                  distribution density.
                </p>
              </div>
            </div>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen text-slate-800 p-6 flex flex-col selection:bg-purple-100 pt-24">
      <MaintenanceScreen />
      <header className="mb-8 flex flex-col md:flex-row items-center justify-between border-b border-slate-200 pb-6 gap-6">
        <div className="flex items-center gap-4">
          <div className="bg-gradient-to-br from-slate-900 to-slate-800 p-3 rounded-2xl shadow-lg text-white ring-4 ring-slate-100">
            <Network className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-slate-900 tracking-tight flex items-center gap-3">
              Visualizer Desktop
              <span className="text-xs font-bold text-purple-600 ml-1 bg-purple-50 px-2 py-0.5 rounded-full border border-purple-100 uppercase tracking-widest">
                v2.1
              </span>
            </h1>
            <p className="text-slate-500 text-sm font-medium flex items-center gap-2 mt-1">
              Interactive RAG Debugger
              <span className="w-1 h-1 rounded-full bg-slate-300"></span>
              Connected to LocalHost
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex bg-slate-100/50 p-1.5 rounded-2xl border border-slate-200 shadow-inner overflow-x-auto">
          {[
            { id: "personal", label: "Personal Workspace" },
            { id: "common", label: "Common Data" },
            { id: "analytics", label: "Analytics" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-200 whitespace-nowrap ${
                activeTab === tab.id
                  ? "bg-white text-slate-900 shadow-md ring-1 ring-black/5"
                  : "text-slate-500 hover:text-slate-700 hover:bg-white/50"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </header>

      <main className="flex-1">{renderContent()}</main>
    </div>
  )
}

export default RAGDemo
