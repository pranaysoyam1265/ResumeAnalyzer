"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import { TrendingUp, Target, Clock, BookOpen, Users, Calendar, Download, BarChart3, Activity, Zap } from "lucide-react"

interface AnalyticsData {
  learningProgress: Array<{
    date: string
    hoursStudied: number
    skillsLearned: number
    coursesCompleted: number
  }>
  skillDistribution: Array<{
    category: string
    count: number
    proficiency: number
    marketDemand: number
  }>
  performanceMetrics: {
    totalHours: number
    coursesCompleted: number
    skillsAcquired: number
    averageScore: number
    streakDays: number
    focusScore: number
  }
  marketInsights: Array<{
    skill: string
    demand: number
    salary: number
    growth: number
  }>
  learningVelocity: Array<{
    week: string
    velocity: number
    efficiency: number
    retention: number
  }>
  goalProgress: Array<{
    goal: string
    progress: number
    target: number
    deadline: string
  }>
}

const COLORS = ["#3B82F6", "#8B5CF6", "#10B981", "#F59E0B", "#EF4444", "#6366F1", "#EC4899", "#14B8A6"]

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState("30d")
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate loading analytics data
    const loadAnalytics = async () => {
      setIsLoading(true)
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // Mock data - in real app, this would come from your analytics API
      setAnalyticsData({
        learningProgress: [
          { date: "2024-01-01", hoursStudied: 2.5, skillsLearned: 1, coursesCompleted: 0 },
          { date: "2024-01-02", hoursStudied: 3.2, skillsLearned: 2, coursesCompleted: 0 },
          { date: "2024-01-03", hoursStudied: 1.8, skillsLearned: 1, coursesCompleted: 1 },
          { date: "2024-01-04", hoursStudied: 4.1, skillsLearned: 3, coursesCompleted: 0 },
          { date: "2024-01-05", hoursStudied: 2.9, skillsLearned: 2, coursesCompleted: 1 },
          { date: "2024-01-06", hoursStudied: 3.7, skillsLearned: 2, coursesCompleted: 0 },
          { date: "2024-01-07", hoursStudied: 2.1, skillsLearned: 1, coursesCompleted: 1 },
        ],
        skillDistribution: [
          { category: "Frontend", count: 12, proficiency: 85, marketDemand: 92 },
          { category: "Backend", count: 8, proficiency: 72, marketDemand: 88 },
          { category: "DevOps", count: 5, proficiency: 65, marketDemand: 95 },
          { category: "Data Science", count: 6, proficiency: 58, marketDemand: 89 },
          { category: "Mobile", count: 4, proficiency: 45, marketDemand: 76 },
          { category: "Design", count: 7, proficiency: 78, marketDemand: 71 },
        ],
        performanceMetrics: {
          totalHours: 127.5,
          coursesCompleted: 8,
          skillsAcquired: 42,
          averageScore: 87.3,
          streakDays: 15,
          focusScore: 92,
        },
        marketInsights: [
          { skill: "React", demand: 95, salary: 95000, growth: 12.5 },
          { skill: "TypeScript", demand: 88, salary: 92000, growth: 18.2 },
          { skill: "Python", demand: 92, salary: 89000, growth: 15.7 },
          { skill: "AWS", demand: 89, salary: 105000, growth: 22.1 },
          { skill: "Docker", demand: 85, salary: 87000, growth: 19.8 },
        ],
        learningVelocity: [
          { week: "Week 1", velocity: 75, efficiency: 82, retention: 88 },
          { week: "Week 2", velocity: 82, efficiency: 85, retention: 91 },
          { week: "Week 3", velocity: 78, efficiency: 88, retention: 89 },
          { week: "Week 4", velocity: 85, efficiency: 91, retention: 93 },
        ],
        goalProgress: [
          { goal: "Complete React Certification", progress: 75, target: 100, deadline: "2024-02-15" },
          { goal: "Learn 5 New Skills", progress: 3, target: 5, deadline: "2024-03-01" },
          { goal: "Study 100 Hours", progress: 67, target: 100, deadline: "2024-02-28" },
        ],
      })
      setIsLoading(false)
    }

    loadAnalytics()
  }, [timeRange])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
        <div className="container mx-auto px-4 py-8">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-slate-200 dark:bg-slate-800 rounded w-1/4"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-32 bg-slate-200 dark:bg-slate-800 rounded-lg"></div>
              ))}
            </div>
            <div className="h-96 bg-slate-200 dark:bg-slate-800 rounded-lg"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!analyticsData) return null

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Analytics & Insights</h1>
            <p className="text-slate-600 dark:text-slate-400 mt-2">
              Track your learning progress and discover insights
            </p>
          </div>
          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            <Select value={timeRange} onValueChange={setTimeRange}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="7d">Last 7 days</SelectItem>
                <SelectItem value="30d">Last 30 days</SelectItem>
                <SelectItem value="90d">Last 90 days</SelectItem>
                <SelectItem value="1y">Last year</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" className="flex items-center gap-2 bg-transparent">
              <Download className="w-4 h-4" />
              Export
            </Button>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Total Hours</p>
                  <p className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                    {analyticsData.performanceMetrics.totalHours}
                  </p>
                </div>
                <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full">
                  <Clock className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
              </div>
              <div className="flex items-center mt-2">
                <TrendingUp className="w-4 h-4 text-green-600 mr-1" />
                <span className="text-sm text-green-600">+12% from last month</span>
              </div>
            </CardContent>
          </Card>

          <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Courses Completed</p>
                  <p className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                    {analyticsData.performanceMetrics.coursesCompleted}
                  </p>
                </div>
                <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-full">
                  <BookOpen className="w-6 h-6 text-green-600 dark:text-green-400" />
                </div>
              </div>
              <div className="flex items-center mt-2">
                <TrendingUp className="w-4 h-4 text-green-600 mr-1" />
                <span className="text-sm text-green-600">+3 this month</span>
              </div>
            </CardContent>
          </Card>

          <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Skills Acquired</p>
                  <p className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                    {analyticsData.performanceMetrics.skillsAcquired}
                  </p>
                </div>
                <div className="p-3 bg-purple-100 dark:bg-purple-900/30 rounded-full">
                  <Target className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                </div>
              </div>
              <div className="flex items-center mt-2">
                <TrendingUp className="w-4 h-4 text-green-600 mr-1" />
                <span className="text-sm text-green-600">+7 this month</span>
              </div>
            </CardContent>
          </Card>

          <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Focus Score</p>
                  <p className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                    {analyticsData.performanceMetrics.focusScore}%
                  </p>
                </div>
                <div className="p-3 bg-orange-100 dark:bg-orange-900/30 rounded-full">
                  <Zap className="w-6 h-6 text-orange-600 dark:text-orange-400" />
                </div>
              </div>
              <div className="flex items-center mt-2">
                <TrendingUp className="w-4 h-4 text-green-600 mr-1" />
                <span className="text-sm text-green-600">+5% this week</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Analytics */}
        <Tabs defaultValue="progress" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
            <TabsTrigger value="progress" className="flex items-center gap-2">
              <Activity className="w-4 h-4" />
              Progress
            </TabsTrigger>
            <TabsTrigger value="skills" className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              Skills
            </TabsTrigger>
            <TabsTrigger value="performance" className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Performance
            </TabsTrigger>
            <TabsTrigger value="market" className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              Market
            </TabsTrigger>
            <TabsTrigger value="goals" className="flex items-center gap-2">
              <Target className="w-4 h-4" />
              Goals
            </TabsTrigger>
          </TabsList>

          {/* Progress Analytics */}
          <TabsContent value="progress" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                <CardHeader>
                  <CardTitle>Learning Progress</CardTitle>
                  <CardDescription>Daily hours studied and skills learned</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={analyticsData.learningProgress}>
                      <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                      <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                      <YAxis tick={{ fontSize: 12 }} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "rgba(255, 255, 255, 0.9)",
                          border: "none",
                          borderRadius: "8px",
                          boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                        }}
                      />
                      <Area
                        type="monotone"
                        dataKey="hoursStudied"
                        stackId="1"
                        stroke="#3B82F6"
                        fill="#3B82F6"
                        fillOpacity={0.6}
                      />
                      <Area
                        type="monotone"
                        dataKey="skillsLearned"
                        stackId="2"
                        stroke="#10B981"
                        fill="#10B981"
                        fillOpacity={0.6}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                <CardHeader>
                  <CardTitle>Learning Velocity</CardTitle>
                  <CardDescription>Weekly learning efficiency and retention</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={analyticsData.learningVelocity}>
                      <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                      <XAxis dataKey="week" tick={{ fontSize: 12 }} />
                      <YAxis tick={{ fontSize: 12 }} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "rgba(255, 255, 255, 0.9)",
                          border: "none",
                          borderRadius: "8px",
                          boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                        }}
                      />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="velocity"
                        stroke="#8B5CF6"
                        strokeWidth={2}
                        dot={{ fill: "#8B5CF6" }}
                      />
                      <Line
                        type="monotone"
                        dataKey="efficiency"
                        stroke="#10B981"
                        strokeWidth={2}
                        dot={{ fill: "#10B981" }}
                      />
                      <Line
                        type="monotone"
                        dataKey="retention"
                        stroke="#F59E0B"
                        strokeWidth={2}
                        dot={{ fill: "#F59E0B" }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Skills Analytics */}
          <TabsContent value="skills" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                <CardHeader>
                  <CardTitle>Skill Distribution</CardTitle>
                  <CardDescription>Your skills across different categories</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={analyticsData.skillDistribution}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ category, count }) => `${category}: ${count}`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="count"
                      >
                        {analyticsData.skillDistribution.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                <CardHeader>
                  <CardTitle>Skill Proficiency vs Market Demand</CardTitle>
                  <CardDescription>How your skills align with market needs</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <RadarChart data={analyticsData.skillDistribution}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="category" tick={{ fontSize: 12 }} />
                      <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fontSize: 10 }} />
                      <Radar
                        name="Your Proficiency"
                        dataKey="proficiency"
                        stroke="#3B82F6"
                        fill="#3B82F6"
                        fillOpacity={0.3}
                      />
                      <Radar
                        name="Market Demand"
                        dataKey="marketDemand"
                        stroke="#10B981"
                        fill="#10B981"
                        fillOpacity={0.3}
                      />
                      <Legend />
                    </RadarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Performance Analytics */}
          <TabsContent value="performance" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                <CardHeader className="text-center">
                  <CardTitle className="text-lg">Average Score</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <div className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                    {analyticsData.performanceMetrics.averageScore}%
                  </div>
                  <Badge variant="secondary" className="text-xs">
                    Above Average
                  </Badge>
                </CardContent>
              </Card>

              <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                <CardHeader className="text-center">
                  <CardTitle className="text-lg">Learning Streak</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <div className="text-4xl font-bold text-green-600 dark:text-green-400 mb-2">
                    {analyticsData.performanceMetrics.streakDays}
                  </div>
                  <Badge variant="secondary" className="text-xs">
                    Days
                  </Badge>
                </CardContent>
              </Card>

              <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                <CardHeader className="text-center">
                  <CardTitle className="text-lg">Focus Score</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <div className="text-4xl font-bold text-purple-600 dark:text-purple-400 mb-2">
                    {analyticsData.performanceMetrics.focusScore}%
                  </div>
                  <Badge variant="secondary" className="text-xs">
                    Excellent
                  </Badge>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Market Analytics */}
          <TabsContent value="market" className="space-y-6">
            <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
              <CardHeader>
                <CardTitle>Market Insights</CardTitle>
                <CardDescription>Salary and demand trends for your skills</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={analyticsData.marketInsights}>
                    <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                    <XAxis dataKey="skill" tick={{ fontSize: 12 }} />
                    <YAxis yAxisId="left" tick={{ fontSize: 12 }} />
                    <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12 }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "rgba(255, 255, 255, 0.9)",
                        border: "none",
                        borderRadius: "8px",
                        boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                      }}
                    />
                    <Legend />
                    <Bar yAxisId="left" dataKey="demand" fill="#3B82F6" name="Market Demand %" />
                    <Bar yAxisId="right" dataKey="salary" fill="#10B981" name="Average Salary ($)" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Goals Analytics */}
          <TabsContent value="goals" className="space-y-6">
            <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
              <CardHeader>
                <CardTitle>Goal Progress</CardTitle>
                <CardDescription>Track your learning goals and deadlines</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {analyticsData.goalProgress.map((goal, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <h4 className="font-medium text-slate-900 dark:text-slate-100">{goal.goal}</h4>
                        <Badge variant={goal.progress >= goal.target ? "default" : "secondary"}>
                          {Math.round((goal.progress / goal.target) * 100)}%
                        </Badge>
                      </div>
                      <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${Math.min((goal.progress / goal.target) * 100, 100)}%` }}
                        ></div>
                      </div>
                      <div className="flex items-center justify-between text-sm text-slate-600 dark:text-slate-400">
                        <span>
                          {goal.progress} / {goal.target}
                        </span>
                        <span className="flex items-center">
                          <Calendar className="w-4 h-4 mr-1" />
                          {new Date(goal.deadline).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
