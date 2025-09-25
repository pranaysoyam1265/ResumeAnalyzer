"use client"

import { useState, useEffect } from "react"
import { DashboardNav } from "@/components/dashboard-nav"
import { ProgressChart } from "@/components/progress-chart"
import { CourseProgress } from "@/components/course-progress"
import { Achievements } from "@/components/achievements"
import { RealTimeTracker } from "@/components/real-time-tracker"
import { LiveProgressFeed } from "@/components/live-progress-feed"
import { ProgressAnalytics } from "@/components/progress-analytics"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { TrendingUp, BookOpen, Trophy, Target, Zap, Activity, Bell } from "lucide-react"

// Mock data
const skillProgressData = [
  {
    skill: "Kubernetes",
    category: "DevOps",
    startLevel: 20,
    currentLevel: 65,
    targetLevel: 85,
    progress: 56,
    trend: "up" as const,
  },
  {
    skill: "TypeScript",
    category: "Programming",
    startLevel: 45,
    currentLevel: 78,
    targetLevel: 90,
    progress: 73,
    trend: "up" as const,
  },
  {
    skill: "System Design",
    category: "Architecture",
    startLevel: 30,
    currentLevel: 55,
    targetLevel: 80,
    progress: 50,
    trend: "up" as const,
  },
  {
    skill: "AWS",
    category: "Cloud",
    startLevel: 40,
    currentLevel: 62,
    targetLevel: 75,
    progress: 63,
    trend: "stable" as const,
  },
]

const timelineData = [
  { month: "Jan", overallProgress: 35, skillsImproved: 2 },
  { month: "Feb", overallProgress: 42, skillsImproved: 3 },
  { month: "Mar", overallProgress: 48, skillsImproved: 2 },
  { month: "Apr", overallProgress: 55, skillsImproved: 4 },
  { month: "May", overallProgress: 62, skillsImproved: 3 },
  { month: "Jun", overallProgress: 68, skillsImproved: 2 },
]

const courseProgressData = [
  {
    id: "1",
    title: "Kubernetes for Developers",
    provider: "Pluralsight",
    status: "completed" as const,
    progress: 100,
    completedLessons: 24,
    totalLessons: 24,
    timeSpent: "12h 30m",
    estimatedTimeRemaining: "0h",
    skills: ["Kubernetes", "Docker", "Container Orchestration"],
    priority: "Critical" as const,
  },
  {
    id: "2",
    title: "TypeScript Complete Developer Guide",
    provider: "Udemy",
    status: "in-progress" as const,
    progress: 75,
    completedLessons: 18,
    totalLessons: 24,
    timeSpent: "18h 15m",
    estimatedTimeRemaining: "6h",
    skills: ["TypeScript", "JavaScript", "Type Safety"],
    priority: "Critical" as const,
  },
  {
    id: "3",
    title: "System Design Interview Preparation",
    provider: "Coursera",
    status: "in-progress" as const,
    progress: 40,
    completedLessons: 6,
    totalLessons: 15,
    timeSpent: "6h 45m",
    estimatedTimeRemaining: "9h 15m",
    skills: ["System Design", "Scalability", "Architecture"],
    priority: "High" as const,
  },
  {
    id: "4",
    title: "AWS Solutions Architect",
    provider: "A Cloud Guru",
    status: "not-started" as const,
    progress: 0,
    completedLessons: 0,
    totalLessons: 32,
    timeSpent: "0h",
    estimatedTimeRemaining: "32h",
    skills: ["AWS", "Cloud Architecture", "EC2"],
    priority: "High" as const,
  },
]

const achievementsData = [
  {
    id: "1",
    title: "First Course Completed",
    description: "Complete your first course",
    icon: "trophy",
    earned: true,
    earnedDate: "March 15, 2024",
  },
  {
    id: "2",
    title: "Skill Master",
    description: "Reach 80% proficiency in any skill",
    icon: "star",
    earned: true,
    earnedDate: "April 22, 2024",
  },
  {
    id: "3",
    title: "Learning Streak",
    description: "Complete lessons for 7 consecutive days",
    icon: "zap",
    earned: true,
    earnedDate: "May 8, 2024",
  },
  {
    id: "4",
    title: "Goal Achiever",
    description: "Complete all courses for a career goal",
    icon: "target",
    earned: false,
    progress: 3,
    maxProgress: 5,
  },
  {
    id: "5",
    title: "Knowledge Seeker",
    description: "Complete 10 courses",
    icon: "award",
    earned: false,
    progress: 1,
    maxProgress: 10,
  },
]

export default function ProgressPage() {
  const [realTimeData, setRealTimeData] = useState({
    currentStreak: 7,
    todayProgress: 45,
    activeSession: true,
    sessionTime: "2h 15m",
    liveUpdates: [],
  })

  const [notifications, setNotifications] = useState([
    {
      id: "1",
      type: "milestone",
      message: "Congratulations! You've reached 70% in TypeScript",
      timestamp: new Date(),
      read: false,
    },
    {
      id: "2",
      type: "streak",
      message: "7-day learning streak! Keep it up!",
      timestamp: new Date(Date.now() - 300000),
      read: false,
    },
  ])

  useEffect(() => {
    const interval = setInterval(() => {
      setRealTimeData((prev) => ({
        ...prev,
        todayProgress: Math.min(prev.todayProgress + Math.random() * 2, 100),
        sessionTime: updateSessionTime(prev.sessionTime),
        liveUpdates: [
          {
            id: Date.now().toString(),
            type: "progress",
            message: "Completed lesson: Advanced TypeScript Generics",
            timestamp: new Date(),
          },
          ...prev.liveUpdates.slice(0, 4),
        ],
      }))
    }, 30000) // Update every 30 seconds

    return () => clearInterval(interval)
  }, [])

  const updateSessionTime = (currentTime: string) => {
    const [hours, minutes] = currentTime.split("h ").map((s) => Number.parseInt(s.replace("m", "")))
    const totalMinutes = hours * 60 + minutes + 1
    return `${Math.floor(totalMinutes / 60)}h ${totalMinutes % 60}m`
  }

  return (
    <div className="min-h-screen bg-background theme-dashboard">
      <DashboardNav />
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-theme-gradient mb-2">Real-Time Progress Tracking</h1>
              <p className="text-muted-foreground text-lg">
                Live monitoring of your skill development and learning journey
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <Badge className="bg-green-100 text-green-700 border-green-200 animate-pulse">
                <Activity className="h-3 w-3 mr-1" />
                Live Session Active
              </Badge>
              <Button variant="outline" size="sm" className="relative bg-transparent">
                <Bell className="h-4 w-4" />
                {notifications.filter((n) => !n.read).length > 0 && (
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-pulse" />
                )}
              </Button>
            </div>
          </div>
        </div>

        <div className="space-y-8">
          {/* Real-Time Overview Stats */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-5">
            <Card className="glass-card border-theme-primary/20 hover-lift">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Live Session</CardTitle>
                <Activity className="h-4 w-4 text-green-500 animate-pulse" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">{realTimeData.sessionTime}</div>
                <p className="text-xs text-muted-foreground">Active learning time today</p>
              </CardContent>
            </Card>

            <Card className="glass-card border-theme-secondary/20 hover-lift">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Today's Progress</CardTitle>
                <TrendingUp className="h-4 w-4 text-theme-secondary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-theme-secondary">{Math.round(realTimeData.todayProgress)}%</div>
                <p className="text-xs text-muted-foreground">Daily learning goal</p>
              </CardContent>
            </Card>

            <Card className="glass-card border-orange-500/20 hover-lift">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Learning Streak</CardTitle>
                <Zap className="h-4 w-4 text-orange-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-orange-600">{realTimeData.currentStreak}</div>
                <p className="text-xs text-muted-foreground">Consecutive days</p>
              </CardContent>
            </Card>

            <Card className="glass-card border-blue-500/20 hover-lift">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Courses Completed</CardTitle>
                <BookOpen className="h-4 w-4 text-blue-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-600">1</div>
                <p className="text-xs text-muted-foreground">3 in progress</p>
              </CardContent>
            </Card>

            <Card className="glass-card border-purple-500/20 hover-lift">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Achievements</CardTitle>
                <Trophy className="h-4 w-4 text-purple-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-purple-600">3</div>
                <p className="text-xs text-muted-foreground">2 available</p>
              </CardContent>
            </Card>
          </div>

          {/* Real-Time Tracker */}
          <RealTimeTracker
            sessionData={realTimeData}
            notifications={notifications}
            onNotificationRead={(id) => {
              setNotifications((prev) => prev.map((n) => (n.id === id ? { ...n, read: true } : n)))
            }}
          />

          {/* Enhanced Tabs with Real-Time Features */}
          <Tabs defaultValue="live" className="space-y-6">
            <TabsList className="glass-nav grid w-full grid-cols-5">
              <TabsTrigger value="live" className="flex items-center space-x-2">
                <Activity className="h-4 w-4" />
                <span>Live Tracking</span>
              </TabsTrigger>
              <TabsTrigger value="skills" className="flex items-center space-x-2">
                <Target className="h-4 w-4" />
                <span>Skills</span>
              </TabsTrigger>
              <TabsTrigger value="courses" className="flex items-center space-x-2">
                <BookOpen className="h-4 w-4" />
                <span>Courses</span>
              </TabsTrigger>
              <TabsTrigger value="achievements" className="flex items-center space-x-2">
                <Trophy className="h-4 w-4" />
                <span>Achievements</span>
              </TabsTrigger>
              <TabsTrigger value="analytics" className="flex items-center space-x-2">
                <TrendingUp className="h-4 w-4" />
                <span>Analytics</span>
              </TabsTrigger>
            </TabsList>

            <TabsContent value="live" className="space-y-6">
              <div className="grid lg:grid-cols-2 gap-8">
                <LiveProgressFeed updates={realTimeData.liveUpdates} />
                <ProgressAnalytics />
              </div>
            </TabsContent>

            <TabsContent value="skills" className="space-y-6">
              <ProgressChart skillProgress={skillProgressData} timelineData={timelineData} />
            </TabsContent>

            <TabsContent value="courses" className="space-y-6">
              <CourseProgress courses={courseProgressData} />
            </TabsContent>

            <TabsContent value="achievements" className="space-y-6">
              <Achievements achievements={achievementsData} />
            </TabsContent>

            <TabsContent value="analytics" className="space-y-6">
              <ProgressAnalytics detailed={true} />
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
