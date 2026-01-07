import React from "react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts"

const AnalyticsPanel = ({ visualizationData }) => {
  // Relevance score distribution (Mock Logic for now, can be derived from distances)
  const relevanceData = React.useMemo(() => {
    if (!visualizationData || !visualizationData.points) return []
    return visualizationData.points.map((pt, i) => ({
      name: `Doc ${i + 1}`,
      score: Math.max(0, 100 - (pt.metadata?.distance || 10)), // Mock score conversion
    }))
  }, [visualizationData])

  const relevanceDataMock = [
    { name: "Doc 1", score: 85 },
    { name: "Doc 2", score: 72 },
    { name: "Doc 3", score: 90 },
    { name: "Doc 4", score: 65 },
    { name: "Doc 5", score: 45 },
  ]

  const compositionData = [
    { name: "PDFs", value: 400 },
    { name: "Text Files", value: 300 },
    { name: "Other", value: 300 },
  ]

  const COLORS = ["#8884d8", "#82ca9d", "#ffc658"]

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-indigo-500">
        <h3 className="text-lg font-bold mb-4 text-slate-800">
          Relevance Scores
        </h3>
        <div className="h-64 w-full min-w-0">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={
                relevanceData.length > 0 ? relevanceData : relevanceDataMock
              }
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="name" stroke="#64748b" tick={{ fontSize: 10 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#ffffff",
                  borderColor: "#e2e8f0",
                  color: "#1e293b",
                  borderRadius: "12px",
                  boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                }}
                cursor={{ fill: "#f1f5f9" }}
              />
              <Bar dataKey="score" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <p className="text-xs text-slate-400 mt-2 text-center">
          * Similarity score of retrieved chunks relative to your query
        </p>
      </div>

      <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-emerald-500">
        <h3 className="text-lg font-bold mb-4 text-slate-800">
          Knowledge Composition
        </h3>
        <div className="h-64 w-full min-w-0">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={compositionData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
              >
                {compositionData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "#ffffff",
                  borderColor: "#e2e8f0",
                  color: "#1e293b",
                  borderRadius: "12px",
                  boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                }}
              />
              <Legend wrapperStyle={{ paddingTop: "20px" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default AnalyticsPanel
