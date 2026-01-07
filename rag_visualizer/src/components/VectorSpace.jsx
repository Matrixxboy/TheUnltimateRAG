import React from "react"
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts"

const VectorSpace = ({ data }) => {
  // Transform data for Recharts
  const chartData = React.useMemo(() => {
    if (!data) return []

    const points = []

    // Add Query Point
    if (data.query_point) {
      points.push({
        ...data.query_point,
        id: "query",
        type: "query",
      })
    }

    // Add Documents
    if (data.points) {
      data.points.forEach((pt, idx) => {
        points.push({
          ...pt,
          id: `doc-${idx}`,
          type: "doc",
        })
      })
    }

    return points
  }, [data])

  return (
    <div className="glass-panel p-6 rounded-2xl h-600 min-h-[400px] flex flex-col border-l-4 border-l-blue-500">
      <h2 className="text-xl font-bold mb-4 text-slate-800 flex justify-between items-center">
        Vector Space Visualization
        {chartData.length > 0 && (
          <span className="text-xs font-medium text-purple-700 bg-purple-100 px-2 py-1 rounded-full border border-purple-200">
            PCA Reduced (3D → 2D)
          </span>
        )}
      </h2>

      <div className="w-full flex-1 min-h-[300px] min-w-0">
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis
                type="number"
                dataKey="x"
                name="PC1"
                stroke="#94a3b8"
                tick={{ fontSize: 10 }}
                tickLine={false}
                axisLine={{ stroke: "#e2e8f0" }}
              />
              <YAxis
                type="number"
                dataKey="y"
                name="PC2"
                stroke="#94a3b8"
                tick={{ fontSize: 10 }}
                tickLine={false}
                axisLine={{ stroke: "#e2e8f0" }}
              />
              <Tooltip
                content={<CustomTooltip />}
                cursor={{ strokeDasharray: "3 3", stroke: "#cbd5e1" }}
              />
              <Scatter name="Vectors" data={chartData} fill="#8884d8">
                {chartData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={entry.type === "query" ? "#f472b6" : "#60a5fa"}
                    stroke={entry.type === "query" ? "#db2777" : "#2563eb"}
                    strokeWidth={1}
                  />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        ) : (
          <div className=" flex flex-col h-full min-h-[400px] items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 bg-slate-50/50 rounded-xl">
            <p>Start chatting to visualize vector relationships</p>
          </div>
        )}
      </div>

      <p className="text-[10px] text-slate-400 mt-2 text-center">
        * Visualizing semantic proximity between query and retrieved documents
      </p>
    </div>
  )
}

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload
    return (
      <div className="bg-white/95 backdrop-blur border border-slate-200 p-3 rounded-xl shadow-xl max-w-xs z-50 text-slate-800">
        <p
          className={`font-semibold mb-1 ${
            data.type === "query" ? "text-pink-600" : "text-blue-600"
          }`}
        >
          {data.type === "query" ? "User Query" : "Document Chunk"}
        </p>
        <p className="text-xs text-slate-600 line-clamp-3">
          {data.text || "No text content"}
        </p>
        {data.metadata && (
          <div className="mt-2 text-[10px] text-slate-400 border-t border-slate-100 pt-1">
            {Object.entries(data.metadata).map(([key, val]) => (
              <div key={key}>
                {key}: {String(val)}
              </div>
            ))}
          </div>
        )}
      </div>
    )
  }
  return null
}

export default VectorSpace
