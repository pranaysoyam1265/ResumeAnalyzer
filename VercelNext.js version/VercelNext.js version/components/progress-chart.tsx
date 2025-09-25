"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts"

interface SkillProgress {
  skill: string
  category: string
  startLevel: number
  currentLevel: number
  targetLevel: number
  progress: number
  trend: "up" | "down" | "stable"
}

interface ProgressChartProps {
  skillProgress: SkillProgress[]
  timelineData: Array<{ month: string; overallProgress: number; skillsImproved: number }>
}

export function ProgressChart({ skillProgress, timelineData }: ProgressChartProps) {
  const getTrendColor = (trend: string) => {
    switch (trend) {
      case "up":
        return "text-green-500"
      case "down":
        return "text-red-500"
      default:
        return "text-gray-500"
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "up":
        return "↗"
      case "down":
        return "↘"
      default:
        return "→"
    }
  }

  return (
    <div className="space-y-6">
      {/* Overall Progress Timeline */}
      <Card className="border-border">
        <CardHeader>
          <CardTitle>Progress Over Time</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="month" className="text-muted-foreground" />
                <YAxis className="text-muted-foreground" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="overallProgress"
                  stroke="hsl(var(--primary))"
                  strokeWidth={2}
                  dot={{ fill: "hsl(var(--primary))" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Skills Improved Per Month */}
      <Card className="border-border">
        <CardHeader>
          <CardTitle>Skills Improved Monthly</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="month" className="text-muted-foreground" />
                <YAxis className="text-muted-foreground" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                />
                <Bar dataKey="skillsImproved" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Individual Skill Progress */}
      <Card className="border-border">
        <CardHeader>
          <CardTitle>Individual Skill Progress</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {skillProgress.map((skill) => (
            <div key={skill.skill} className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="font-medium">{skill.skill}</span>
                  <Badge variant="secondary" className="text-xs">
                    {skill.category}
                  </Badge>
                  <span className={`text-sm ${getTrendColor(skill.trend)}`}>
                    {getTrendIcon(skill.trend)} {skill.trend}
                  </span>
                </div>
                <div className="text-sm text-muted-foreground">
                  {skill.currentLevel}% / {skill.targetLevel}%
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>Start: {skill.startLevel}%</span>
                  <span>Current: {skill.currentLevel}%</span>
                  <span>Target: {skill.targetLevel}%</span>
                </div>
                <div className="relative">
                  <Progress value={(skill.currentLevel / skill.targetLevel) * 100} className="h-3" />
                  <div
                    className="absolute top-0 left-0 h-3 bg-muted rounded-full"
                    style={{ width: `${(skill.startLevel / skill.targetLevel) * 100}%` }}
                  />
                </div>
                <div className="text-xs text-muted-foreground">Progress: {skill.progress}% towards target</div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
