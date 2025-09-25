"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
} from "recharts"
import { TrendingUp, Clock, Target, Brain, Zap, Calendar } from "lucide-react"

interface ProgressAnalyticsProps {
  detailed?: boolean
}

export function ProgressAnalytics({ detailed = false }: ProgressAnalyticsProps) {
  const weeklyData = [
    { day: "Mon", hours: 2.5, focus: 85, retention: 78 },
    { day: "Tue", hours: 3.2, focus: 88, retention: 82 },
    { day: "Wed", hours: 1.8, focus: 75, retention: 70 },
    { day: "Thu", hours: 4.1, focus: 92, retention: 88 },
    { day: "Fri", hours: 2.9, focus: 87, retention: 85 },
    { day: "Sat", hours: 3.5, focus: 90, retention: 89 },
    { day: "Sun", hours: 2.2, focus: 82, retention: 79 },
  ]

  const skillDistribution = [
    { name: "Programming", value: 35, color: "#3b82f6" },
    { name: "DevOps", value: 25, color: "#10b981" },
    { name: "Cloud", value: 20, color: "#f59e0b" },
    { name: "AI/ML", value: 15, color: "#8b5cf6" },
    { name: "Other", value: 5, color: "#6b7280" },
  ]

  const learningPatterns = {
    peakHours: "2-4 PM",
    averageSession: "2.8 hours",
    bestDay: "Thursday",
    focusScore: 87,
    consistencyScore: 92,
  }

  return (
    <div className="space-y-6">
      {/* Analytics Overview */}
      <Card className="glass-card border-theme-primary/20 hover-lift">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Brain className="h-6 w-6 text-theme-primary" />
            <span>Learning Analytics Dashboard</span>
            <Badge className="bg-blue-100 text-blue-700 border-blue-200">AI-Powered</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-5 gap-4">
            <div className="text-center p-3 bg-theme-primary/5 rounded-lg">
              <Clock className="h-5 w-5 mx-auto mb-2 text-theme-primary" />
              <div className="text-lg font-bold text-theme-primary">{learningPatterns.averageSession}</div>
              <div className="text-xs text-muted-foreground">Avg Session</div>
            </div>
            <div className="text-center p-3 bg-green-500/5 rounded-lg">
              <Calendar className="h-5 w-5 mx-auto mb-2 text-green-600" />
              <div className="text-lg font-bold text-green-600">{learningPatterns.bestDay}</div>
              <div className="text-xs text-muted-foreground">Best Day</div>
            </div>
            <div className="text-center p-3 bg-blue-500/5 rounded-lg">
              <Target className="h-5 w-5 mx-auto mb-2 text-blue-600" />
              <div className="text-lg font-bold text-blue-600">{learningPatterns.focusScore}%</div>
              <div className="text-xs text-muted-foreground">Focus Score</div>
            </div>
            <div className="text-center p-3 bg-purple-500/5 rounded-lg">
              <Zap className="h-5 w-5 mx-auto mb-2 text-purple-600" />
              <div className="text-lg font-bold text-purple-600">{learningPatterns.consistencyScore}%</div>
              <div className="text-xs text-muted-foreground">Consistency</div>
            </div>
            <div className="text-center p-3 bg-orange-500/5 rounded-lg">
              <TrendingUp className="h-5 w-5 mx-auto mb-2 text-orange-600" />
              <div className="text-lg font-bold text-orange-600">{learningPatterns.peakHours}</div>
              <div className="text-xs text-muted-foreground">Peak Hours</div>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Weekly Learning Pattern */}
        <Card className="glass-card border-theme-secondary/20 hover-lift">
          <CardHeader>
            <CardTitle>Weekly Learning Pattern</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={weeklyData}>
                  <defs>
                    <linearGradient id="hoursGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="hsl(var(--theme-primary))" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="hsl(var(--theme-primary))" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis dataKey="day" className="text-xs fill-muted-foreground" />
                  <YAxis className="text-xs fill-muted-foreground" />
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
                    dataKey="hours"
                    stroke="hsl(var(--theme-primary))"
                    fillOpacity={1}
                    fill="url(#hoursGradient)"
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Skill Distribution */}
        <Card className="glass-card border-theme-accent/20 hover-lift">
          <CardHeader>
            <CardTitle>Learning Focus Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={skillDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {skillDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                      fontSize: "12px",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex flex-wrap gap-2 mt-4">
              {skillDistribution.map((skill) => (
                <div key={skill.name} className="flex items-center space-x-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: skill.color }} />
                  <span className="text-xs text-muted-foreground">
                    {skill.name} ({skill.value}%)
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {detailed && (
        <Card className="glass-card border-theme-primary/20 hover-lift">
          <CardHeader>
            <CardTitle>Focus & Retention Trends</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={weeklyData}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis dataKey="day" className="text-xs fill-muted-foreground" />
                  <YAxis className="text-xs fill-muted-foreground" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                      fontSize: "12px",
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="focus"
                    stroke="hsl(var(--theme-primary))"
                    strokeWidth={2}
                    dot={{ fill: "hsl(var(--theme-primary))" }}
                  />
                  <Line
                    type="monotone"
                    dataKey="retention"
                    stroke="hsl(var(--theme-secondary))"
                    strokeWidth={2}
                    dot={{ fill: "hsl(var(--theme-secondary))" }}
                    strokeDasharray="5 5"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
