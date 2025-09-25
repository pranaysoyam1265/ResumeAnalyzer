"use client"

import { Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from "recharts"

const trendData = [
  { month: "Jan", ai: 85, cloud: 78, frontend: 65, backend: 70 },
  { month: "Feb", ai: 88, cloud: 80, frontend: 67, backend: 72 },
  { month: "Mar", ai: 92, cloud: 82, frontend: 69, backend: 74 },
  { month: "Apr", ai: 95, cloud: 85, frontend: 71, backend: 76 },
  { month: "May", ai: 98, cloud: 87, frontend: 73, backend: 78 },
  { month: "Jun", ai: 102, cloud: 90, frontend: 75, backend: 80 },
]

export function MarketTrendsChart() {
  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={trendData}>
          <defs>
            <linearGradient id="aiGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(var(--theme-primary))" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(var(--theme-primary))" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="cloudGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(var(--theme-secondary))" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(var(--theme-secondary))" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
          <XAxis dataKey="month" className="text-xs fill-muted-foreground" tick={{ fontSize: 12 }} />
          <YAxis className="text-xs fill-muted-foreground" tick={{ fontSize: 12 }} />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "8px",
              fontSize: "12px",
            }}
          />
          <Area
            type="monotone"
            dataKey="ai"
            stroke="hsl(var(--theme-primary))"
            fillOpacity={1}
            fill="url(#aiGradient)"
            strokeWidth={2}
          />
          <Area
            type="monotone"
            dataKey="cloud"
            stroke="hsl(var(--theme-secondary))"
            fillOpacity={1}
            fill="url(#cloudGradient)"
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="frontend"
            stroke="hsl(var(--theme-accent))"
            strokeWidth={2}
            strokeDasharray="5 5"
          />
          <Line type="monotone" dataKey="backend" stroke="hsl(var(--chart-4))" strokeWidth={2} strokeDasharray="2 2" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
