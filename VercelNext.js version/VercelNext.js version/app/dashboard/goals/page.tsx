"use client"

import { useState } from "react"
import { DashboardNav } from "@/components/dashboard-nav"
import { CareerGoalSelector } from "@/components/career-goal-selector"
import { SkillGapVisualization } from "@/components/skill-gap-visualization"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Brain, Target, TrendingUp } from "lucide-react"

const mockSkillGaps = [
  // Critical Essential Skills (Foundational)
  {
    skill: "Kubernetes",
    category: "Cloud & DevOps",
    currentLevel: 20,
    requiredLevel: 85,
    importance: "Critical" as const,
    gap: 65,
    skillType: "Essential",
    marketTrend: "Growing",
    timeToAcquire: "6-8 months",
    learningPath: "Beginner → Intermediate → Advanced",
    jobPostingFrequency: 18000,
    salaryImpact: "Very High (+$15k-25k)",
    armaForecast: "+50% demand growth",
  },
  {
    skill: "System Design",
    category: "Architecture",
    currentLevel: 30,
    requiredLevel: 80,
    importance: "Critical" as const,
    gap: 50,
    skillType: "Essential",
    marketTrend: "Growing",
    timeToAcquire: "4-6 months",
    learningPath: "Fundamentals → Scalability → Distributed Systems",
    jobPostingFrequency: 25000,
    salaryImpact: "Very High (+$20k-30k)",
    armaForecast: "+25% demand growth",
  },

  // High Priority Competitive Skills (Trending)
  {
    skill: "TypeScript",
    category: "Programming",
    currentLevel: 45,
    requiredLevel: 90,
    importance: "High" as const,
    gap: 45,
    skillType: "Competitive",
    marketTrend: "Growing",
    timeToAcquire: "3-4 months",
    learningPath: "Basics → Advanced Types → Enterprise Patterns",
    jobPostingFrequency: 28000,
    salaryImpact: "High (+$10k-15k)",
    armaForecast: "+25% demand growth",
  },
  {
    skill: "AWS",
    category: "Cloud",
    currentLevel: 40,
    requiredLevel: 75,
    importance: "High" as const,
    gap: 35,
    skillType: "Essential",
    marketTrend: "Growing",
    timeToAcquire: "4-5 months",
    learningPath: "Core Services → Architecture → Certification",
    jobPostingFrequency: 32000,
    salaryImpact: "High (+$12k-18k)",
    armaForecast: "+22% demand growth",
  },

  // Medium Priority Skills
  {
    skill: "GraphQL",
    category: "Backend",
    currentLevel: 25,
    requiredLevel: 60,
    importance: "Medium" as const,
    gap: 35,
    skillType: "Competitive",
    marketTrend: "Growing",
    timeToAcquire: "2-3 months",
    learningPath: "Query Language → Schema Design → Performance",
    jobPostingFrequency: 8500,
    salaryImpact: "Medium (+$5k-10k)",
    armaForecast: "+30% demand growth",
  },

  // Skills Above Required Level (Strengths)
  {
    skill: "React",
    category: "Frontend",
    currentLevel: 88,
    requiredLevel: 85,
    importance: "High" as const,
    gap: -3,
    skillType: "Essential",
    marketTrend: "Stable",
    timeToAcquire: "Maintain current level",
    learningPath: "Stay updated with latest features",
    jobPostingFrequency: 42000,
    salaryImpact: "High (Maintained)",
    armaForecast: "+5% demand growth",
  },
  {
    skill: "JavaScript",
    category: "Programming",
    currentLevel: 92,
    requiredLevel: 85,
    importance: "Critical" as const,
    gap: -7,
    skillType: "Essential",
    marketTrend: "Stable",
    timeToAcquire: "Maintain expertise",
    learningPath: "Keep up with ES updates",
    jobPostingFrequency: 52000,
    salaryImpact: "High (Maintained)",
    armaForecast: "+8% demand growth",
  },
]

export default function SkillGoalsPage() {
  const [selectedGoals, setSelectedGoals] = useState<string[]>([])
  const [analysisComplete, setAnalysisComplete] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleAnalyzeGaps = async () => {
    if (selectedGoals.length === 0) return

    setIsAnalyzing(true)
    // Simulate analysis
    setTimeout(() => {
      setAnalysisComplete(true)
      setIsAnalyzing(false)
    }, 2000)
  }

  const handleReset = () => {
    setAnalysisComplete(false)
    setSelectedGoals([])
  }

  return (
    <div className="min-h-screen bg-background">
      <DashboardNav />
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground">Skill Gap Analysis</h1>
          <p className="text-muted-foreground mt-2">
            Set your career goals and discover the skills you need to develop
          </p>
        </div>

        <div className="space-y-8">
          {/* Enhanced How it Works */}
          <Card className="border-border">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5 text-primary" />
                <span>AI-Powered Two-Tier Gap Analysis</span>
              </CardTitle>
              <p className="text-sm text-muted-foreground">
                Using ARIMA models, time series analysis, and O*NET knowledge graphs
              </p>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
                    <Target className="h-4 w-4 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-medium mb-1">Foundational vs Trending</h3>
                    <p className="text-sm text-muted-foreground">
                      Distinguishes essential skills for job entry from competitive advantage skills
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
                    <Brain className="h-4 w-4 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-medium mb-1">Time Series Analysis</h3>
                    <p className="text-sm text-muted-foreground">
                      ARIMA models predict skill demand trends and growth rates
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
                    <TrendingUp className="h-4 w-4 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-medium mb-1">Market Intelligence</h3>
                    <p className="text-sm text-muted-foreground">
                      Real-time data from LinkedIn, Indeed, Glassdoor for accurate insights
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Goal Selection */}
          {!analysisComplete && (
            <>
              <CareerGoalSelector selectedGoals={selectedGoals} onGoalsChange={setSelectedGoals} />

              {selectedGoals.length > 0 && (
                <Card className="border-border">
                  <CardContent className="p-6">
                    <div className="text-center space-y-4">
                      <p className="text-muted-foreground">
                        Ready to analyze skill gaps for {selectedGoals.length} career goal
                        {selectedGoals.length > 1 ? "s" : ""}?
                      </p>
                      <Button onClick={handleAnalyzeGaps} disabled={isAnalyzing} size="lg">
                        {isAnalyzing ? "Analyzing..." : "Analyze Skill Gaps"}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              )}
            </>
          )}

          {/* Analysis in Progress */}
          {isAnalyzing && (
            <Alert className="border-primary/20 bg-primary/5">
              <Brain className="h-4 w-4 text-primary" />
              <AlertDescription className="text-primary">
                Analyzing skill requirements and comparing with your profile...
              </AlertDescription>
            </Alert>
          )}

          {/* Results */}
          {analysisComplete && selectedGoals.length > 0 && (
            <>
              <SkillGapVisualization gaps={mockSkillGaps} targetRole={selectedGoals[0]} />

              <Card className="border-border">
                <CardContent className="p-6">
                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Button onClick={handleReset} variant="outline" className="bg-transparent">
                      Analyze Different Goals
                    </Button>
                    <Button asChild>
                      <a href="/dashboard/recommendations">View Course Recommendations</a>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
