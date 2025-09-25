"use client"

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from "recharts"

const skillData = [
  {
    category: "Programming",
    current: 85,
    target: 95,
    market: 90,
  },
  {
    category: "AI/ML",
    current: 65,
    target: 85,
    market: 95,
  },
  {
    category: "Frontend",
    current: 78,
    target: 85,
    market: 80,
  },
  {
    category: "Backend",
    current: 72,
    target: 80,
    market: 85,
  },
  {
    category: "DevOps",
    current: 45,
    target: 70,
    market: 88,
  },
  {
    category: "Data Science",
    current: 60,
    target: 80,
    market: 92,
  },
]

export function SkillRadarChart() {
  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={skillData}>
          <PolarGrid className="stroke-muted" />
          <PolarAngleAxis dataKey="category" className="text-xs fill-muted-foreground" tick={{ fontSize: 12 }} />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            className="text-xs fill-muted-foreground"
            tick={{ fontSize: 10 }}
          />
          <Radar
            name="Current Skills"
            dataKey="current"
            stroke="hsl(var(--theme-primary))"
            fill="hsl(var(--theme-primary))"
            fillOpacity={0.2}
            strokeWidth={2}
          />
          <Radar
            name="Target Level"
            dataKey="target"
            stroke="hsl(var(--theme-secondary))"
            fill="hsl(var(--theme-secondary))"
            fillOpacity={0.1}
            strokeWidth={2}
            strokeDasharray="5 5"
          />
          <Radar
            name="Market Demand"
            dataKey="market"
            stroke="hsl(var(--theme-accent))"
            fill="hsl(var(--theme-accent))"
            fillOpacity={0.05}
            strokeWidth={1}
            strokeDasharray="2 2"
          />
          <Legend wrapperStyle={{ fontSize: "12px" }} iconType="line" />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}
