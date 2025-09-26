"use client"

import { useState, useMemo } from "react"
import { DashboardNav } from "@/components/dashboard-nav"
import { CourseCard } from "@/components/course-card"
import { CourseFilters } from "@/components/course-filters"
import { RecommendationEngine } from "@/components/recommendation-engine"
import { LearningPathBuilder } from "@/components/learning-path-builder"
import { SkillGapAnalysis } from "@/components/skill-gap-analysis"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Brain, BookOpen, Target, Zap, TrendingUp, Clock, Star } from "lucide-react"

// Enhanced mock course data with AI features
const mockCourses = [
  {
    id: "1",
    title: "Kubernetes for Developers",
    provider: "Pluralsight",
    description:
      "Master container orchestration with Kubernetes. Learn to deploy, scale, and manage containerized applications in production environments.",
    duration: "12 hours",
    level: "Intermediate" as const,
    rating: 4.8,
    students: 15420,
    price: 49,
    skills: ["Kubernetes", "Docker", "Container Orchestration", "DevOps", "YAML"],
    matchScore: 95,
    priority: "Critical" as const,
    url: "#",
    aiInsights: {
      marketDemand: 92,
      salaryImpact: "+$15,000",
      completionRate: 78,
      jobRelevance: 95,
      trendingScore: 88,
    },
    prerequisites: ["Docker Basics", "Linux Fundamentals"],
    outcomes: ["Deploy applications to Kubernetes", "Manage cluster resources", "Implement CI/CD pipelines"],
    difficulty: 7.5,
    tags: ["trending", "high-demand", "certification-prep"],
  },
  {
    id: "2",
    title: "TypeScript Complete Developer Guide",
    provider: "Udemy",
    description:
      "Learn TypeScript from scratch and build type-safe applications. Covers advanced types, generics, and integration with React.",
    duration: "24 hours",
    level: "Beginner" as const,
    rating: 4.7,
    students: 89340,
    price: 89,
    skills: ["TypeScript", "JavaScript", "Type Safety", "Generics", "React"],
    matchScore: 92,
    priority: "Critical" as const,
    url: "#",
    aiInsights: {
      marketDemand: 89,
      salaryImpact: "+$12,000",
      completionRate: 85,
      jobRelevance: 92,
      trendingScore: 95,
    },
    prerequisites: ["JavaScript ES6+"],
    outcomes: ["Write type-safe code", "Use advanced TypeScript features", "Integrate with React"],
    difficulty: 6.0,
    tags: ["essential", "trending", "beginner-friendly"],
  },
  {
    id: "3",
    title: "System Design Interview Preparation",
    provider: "Coursera",
    description:
      "Prepare for system design interviews with real-world examples. Learn to design scalable systems and handle high traffic.",
    duration: "16 hours",
    level: "Advanced" as const,
    rating: 4.9,
    students: 23450,
    price: 79,
    skills: ["System Design", "Scalability", "Architecture", "Microservices", "Load Balancing"],
    matchScore: 88,
    priority: "High" as const,
    url: "#",
    aiInsights: {
      marketDemand: 80,
      salaryImpact: "+$10,000",
      completionRate: 90,
      jobRelevance: 85,
      trendingScore: 80,
    },
    prerequisites: ["Data Structures", "Algorithms"],
    outcomes: ["Design scalable systems", "Handle high traffic", "Optimize performance"],
    difficulty: 8.0,
    tags: ["high-demand", "advanced"],
  },
  {
    id: "4",
    title: "AWS Solutions Architect",
    provider: "A Cloud Guru",
    description:
      "Become an AWS Solutions Architect. Learn to design and deploy scalable, highly available systems on AWS.",
    duration: "32 hours",
    level: "Intermediate" as const,
    rating: 4.6,
    students: 45670,
    price: 149,
    skills: ["AWS", "Cloud Architecture", "EC2", "S3", "Lambda", "VPC"],
    matchScore: 85,
    priority: "High" as const,
    url: "#",
    aiInsights: {
      marketDemand: 75,
      salaryImpact: "+$12,000",
      completionRate: 80,
      jobRelevance: 80,
      trendingScore: 75,
    },
    prerequisites: ["Cloud Computing Basics"],
    outcomes: ["Design AWS architectures", "Deploy scalable systems", "Manage cloud resources"],
    difficulty: 7.0,
    tags: ["certification-prep", "high-demand"],
  },
  {
    id: "5",
    title: "GraphQL with React and Node.js",
    provider: "Udemy",
    description:
      "Build modern APIs with GraphQL. Learn to create efficient, flexible APIs and integrate them with React applications.",
    duration: "18 hours",
    level: "Intermediate" as const,
    rating: 4.5,
    students: 12890,
    price: 69,
    skills: ["GraphQL", "React", "Node.js", "Apollo", "API Design"],
    matchScore: 78,
    priority: "Medium" as const,
    url: "#",
    aiInsights: {
      marketDemand: 70,
      salaryImpact: "+$8,000",
      completionRate: 85,
      jobRelevance: 75,
      trendingScore: 70,
    },
    prerequisites: ["JavaScript Basics", "React Fundamentals"],
    outcomes: ["Create GraphQL APIs", "Integrate with React", "Optimize API performance"],
    difficulty: 6.5,
    tags: ["trending", "beginner-friendly"],
  },
  {
    id: "6",
    title: "Advanced React Patterns",
    provider: "Frontend Masters",
    description:
      "Master advanced React patterns and techniques. Learn render props, higher-order components, and custom hooks.",
    duration: "8 hours",
    level: "Advanced" as const,
    rating: 4.9,
    students: 8920,
    price: 0,
    skills: ["React", "Hooks", "Patterns", "Performance", "State Management"],
    matchScore: 72,
    priority: "Low" as const,
    url: "#",
    aiInsights: {
      marketDemand: 60,
      salaryImpact: "+$5,000",
      completionRate: 95,
      jobRelevance: 70,
      trendingScore: 60,
    },
    prerequisites: ["React Intermediate"],
    outcomes: ["Implement advanced React patterns", "Optimize component performance", "Manage complex state"],
    difficulty: 9.0,
    tags: ["advanced", "essential"],
  },
]

export default function RecommendationsPage() {
  const [filters, setFilters] = useState<any>({
    providers: [],
    levels: [],
    duration: [0, 100],
    price: [0, 500],
    priority: [],
    sortBy: "ai-score",
    tags: [],
  })

  const [activeTab, setActiveTab] = useState("recommendations")
  const [userPreferences, setUserPreferences] = useState({
    learningStyle: "visual",
    timeCommitment: "moderate",
    careerGoals: ["full-stack", "ai-ml"],
    experienceLevel: "intermediate",
  })

  const filteredCourses = useMemo(() => {
    const filtered = mockCourses.filter((course) => {
      // Provider filter
      if (filters.providers.length > 0 && !filters.providers.includes(course.provider)) {
        return false
      }

      // Level filter
      if (filters.levels.length > 0 && !filters.levels.includes(course.level)) {
        return false
      }

      // Priority filter
      if (filters.priority.length > 0 && !filters.priority.includes(course.priority)) {
        return false
      }

      // Tag filter
      if (filters.tags.length > 0) {
        const hasMatchingTag = filters.tags.some((tag: string) => course.tags?.includes(tag))
        if (!hasMatchingTag) return false
      }

      // Duration filter (approximate)
      const courseDuration = Number.parseInt(course.duration)
      if (courseDuration < filters.duration[0] || courseDuration > filters.duration[1]) {
        return false
      }

      // Price filter
      if (course.price < filters.price[0] || course.price > filters.price[1]) {
        return false
      }

      return true
    })

    switch (filters.sortBy) {
      case "ai-score":
        filtered.sort((a, b) => {
          const aScore = a.matchScore * 0.4 + a.aiInsights.marketDemand * 0.3 + a.aiInsights.jobRelevance * 0.3
          const bScore = b.matchScore * 0.4 + b.aiInsights.marketDemand * 0.3 + b.aiInsights.jobRelevance * 0.3
          return bScore - aScore
        })
        break
      case "market-demand":
        filtered.sort((a, b) => b.aiInsights.marketDemand - a.aiInsights.marketDemand)
        break
      case "salary-impact":
        filtered.sort((a, b) => {
          const aSalary = Number.parseInt(a.aiInsights.salaryImpact.replace(/[^0-9]/g, ""))
          const bSalary = Number.parseInt(b.aiInsights.salaryImpact.replace(/[^0-9]/g, ""))
          return bSalary - aSalary
        })
        break
      case "trending":
        filtered.sort((a, b) => b.aiInsights.trendingScore - a.aiInsights.trendingScore)
        break
      case "rating":
        filtered.sort((a, b) => b.rating - a.rating)
        break
      case "price-low":
        filtered.sort((a, b) => a.price - b.price)
        break
      case "price-high":
        filtered.sort((a, b) => b.price - a.price)
        break
      case "duration":
        filtered.sort((a, b) => Number.parseInt(a.duration) - Number.parseInt(b.duration))
        break
    }

    return filtered
  }, [filters])

  function generateRecommendationReason(course: any, preferences: any) {
    const reasons = []
    if (course.aiInsights.marketDemand > 85) reasons.push("High market demand")
    if (course.matchScore > 90) reasons.push("Perfect skill match")
    if (course.tags?.includes("trending")) reasons.push("Trending technology")
    if (course.aiInsights.salaryImpact.includes("+")) reasons.push("Salary boost potential")
    return reasons.join(" • ")
  }

  const aiRecommendations = useMemo(() => {
    return filteredCourses.slice(0, 3).map((course) => ({
      ...course,
      reason: generateRecommendationReason(course, userPreferences),
    }))
  }, [filteredCourses, userPreferences])

  return (
    <div className="min-h-screen bg-background theme-dashboard">
      <DashboardNav />
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-theme-gradient mb-2">Smart Course Recommendations</h1>
          <p className="text-muted-foreground text-lg">
            AI-powered personalized learning paths based on market intelligence and your career goals
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-8">
          <TabsList className="glass-nav grid w-full grid-cols-4">
            <TabsTrigger value="recommendations" className="flex items-center space-x-2">
              <Brain className="h-4 w-4" />
              <span>AI Recommendations</span>
            </TabsTrigger>
            <TabsTrigger value="learning-paths" className="flex items-center space-x-2">
              <Target className="h-4 w-4" />
              <span>Learning Paths</span>
            </TabsTrigger>
            <TabsTrigger value="skill-gaps" className="flex items-center space-x-2">
              <TrendingUp className="h-4 w-4" />
              <span>Skill Analysis</span>
            </TabsTrigger>
            <TabsTrigger value="browse" className="flex items-center space-x-2">
              <BookOpen className="h-4 w-4" />
              <span>Browse All</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="recommendations" className="space-y-8">
            <RecommendationEngine
              recommendations={aiRecommendations}
              userPreferences={userPreferences}
              onPreferencesChange={setUserPreferences}
            />
          </TabsContent>

          <TabsContent value="learning-paths" className="space-y-8">
            <LearningPathBuilder courses={filteredCourses} userGoals={userPreferences.careerGoals} />
          </TabsContent>

          <TabsContent value="skill-gaps" className="space-y-8">
            <SkillGapAnalysis courses={filteredCourses} />
          </TabsContent>

          <TabsContent value="browse" className="space-y-8">
            {/* Enhanced AI Insights Dashboard */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              <Card className="glass-card border-theme-primary/20 hover-lift">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">AI Match Score</CardTitle>
                  <Brain className="h-4 w-4 text-theme-primary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-theme-primary">
                    {Math.round(filteredCourses.reduce((acc, c) => acc + c.matchScore, 0) / filteredCourses.length)}%
                  </div>
                  <p className="text-xs text-muted-foreground">Average relevance to your profile</p>
                </CardContent>
              </Card>

              <Card className="glass-card border-theme-secondary/20 hover-lift">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Market Demand</CardTitle>
                  <TrendingUp className="h-4 w-4 text-theme-secondary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-theme-secondary">
                    {Math.round(
                      filteredCourses.reduce((acc, c) => acc + c.aiInsights.marketDemand, 0) / filteredCourses.length,
                    )}
                    %
                  </div>
                  <p className="text-xs text-muted-foreground">Industry demand for these skills</p>
                </CardContent>
              </Card>

              <Card className="glass-card border-green-500/20 hover-lift">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Salary Impact</CardTitle>
                  <Zap className="h-4 w-4 text-green-600" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-600">+$13.5K</div>
                  <p className="text-xs text-muted-foreground">Average potential salary increase</p>
                </CardContent>
              </Card>

              <Card className="glass-card border-blue-500/20 hover-lift">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
                  <Star className="h-4 w-4 text-blue-600" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-blue-600">
                    {Math.round(
                      filteredCourses.reduce((acc, c) => acc + c.aiInsights.completionRate, 0) / filteredCourses.length,
                    )}
                    %
                  </div>
                  <p className="text-xs text-muted-foreground">Average completion rate</p>
                </CardContent>
              </Card>
            </div>

            {/* Smart Alerts */}
            <div className="space-y-4">
              <Alert className="glass border-theme-primary/30 bg-theme-primary/5">
                <Zap className="h-4 w-4 text-theme-primary" />
                <AlertDescription className="text-theme-primary">
                  <strong>AI Insight:</strong> Based on current market trends, focusing on Kubernetes and TypeScript
                  could increase your job prospects by 40% and potential salary by $15,000+.
                </AlertDescription>
              </Alert>

              <Alert className="glass border-orange-500/30 bg-orange-50">
                <Clock className="h-4 w-4 text-orange-600" />
                <AlertDescription className="text-orange-700">
                  <strong>Time-Sensitive:</strong> 3 courses in your recommendations have limited-time discounts ending
                  this week. Consider enrolling soon to save up to 60%.
                </AlertDescription>
              </Alert>
            </div>

            <div className="grid lg:grid-cols-4 gap-8">
              {/* Enhanced Filters */}
              <div className="lg:col-span-1">
                <CourseFilters onFiltersChange={setFilters} />
              </div>

              {/* Course List with AI Enhancements */}
              <div className="lg:col-span-3">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center space-x-2">
                    <h2 className="text-xl font-semibold">Smart Recommendations</h2>
                    <Badge variant="secondary" className="bg-theme-primary/10 text-theme-primary">
                      {filteredCourses.length} courses
                    </Badge>
                    <Badge variant="outline" className="text-xs">
                      AI-Powered
                    </Badge>
                  </div>
                </div>

                <div className="grid gap-6">
                  {filteredCourses.map((course, index) => (
                    <div key={course.id} className="fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                      <CourseCard course={course} showAIInsights={true} />
                    </div>
                  ))}
                </div>

                {filteredCourses.length === 0 && (
                  <Card className="glass-card border-theme-primary/20">
                    <CardContent className="p-8 text-center">
                      <Brain className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                      <h3 className="text-lg font-medium mb-2">No matching courses found</h3>
                      <p className="text-muted-foreground mb-4">
                        Try adjusting your filters or let our AI suggest alternatives.
                      </p>
                      <Button className="bg-theme-gradient hover:opacity-90">Get AI Suggestions</Button>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
