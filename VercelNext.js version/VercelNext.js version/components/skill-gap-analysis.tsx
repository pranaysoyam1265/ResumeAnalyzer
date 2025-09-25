"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { TrendingUp, AlertTriangle, Target, Zap, BookOpen } from "lucide-react"

interface SkillGapAnalysisProps {
  courses: any[]
}

export function SkillGapAnalysis({ courses }: SkillGapAnalysisProps) {
  const skillGaps = [
    {
      skill: "Kubernetes",
      currentLevel: 20,
      targetLevel: 80,
      marketDemand: 95,
      priority: "Critical",
      gap: 60,
      timeToClose: "3-4 months",
      recommendedCourses: courses.filter((c) => c.skills.includes("Kubernetes")),
      salaryImpact: "+$18,000",
      jobOpportunities: 1240,
    },
    {
      skill: "TypeScript",
      currentLevel: 45,
      targetLevel: 85,
      marketDemand: 89,
      priority: "High",
      gap: 40,
      timeToClose: "2-3 months",
      recommendedCourses: courses.filter((c) => c.skills.includes("TypeScript")),
      salaryImpact: "+$12,000",
      jobOpportunities: 2100,
    },
    {
      skill: "AWS",
      currentLevel: 30,
      targetLevel: 75,
      marketDemand: 92,
      priority: "High",
      gap: 45,
      timeToClose: "4-5 months",
      recommendedCourses: courses.filter((c) => c.skills.includes("AWS")),
      salaryImpact: "+$15,000",
      jobOpportunities: 1850,
    },
    {
      skill: "Machine Learning",
      currentLevel: 25,
      targetLevel: 70,
      marketDemand: 88,
      priority: "Medium",
      gap: 45,
      timeToClose: "6-8 months",
      recommendedCourses: courses.filter((c) => c.skills.includes("Machine Learning")),
      salaryImpact: "+$22,000",
      jobOpportunities: 980,
    },
  ]

  return (
    <div className="space-y-8">
      {/* Analysis Overview */}
      <Card className="glass-card border-theme-accent/20 hover-lift">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="h-6 w-6 text-theme-accent" />
            <span>AI-Powered Skill Gap Analysis</span>
          </CardTitle>
          <p className="text-muted-foreground">
            Advanced analysis of your skill portfolio against market demands and career objectives
          </p>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-red-500 mb-1">4</div>
              <div className="text-sm text-muted-foreground">Critical Gaps</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-500 mb-1">$67K</div>
              <div className="text-sm text-muted-foreground">Potential Salary Boost</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-500 mb-1">6,170</div>
              <div className="text-sm text-muted-foreground">Job Opportunities</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-500 mb-1">3-8</div>
              <div className="text-sm text-muted-foreground">Months to Close</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Detailed Gap Analysis */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold flex items-center space-x-2">
          <Target className="h-6 w-6 text-theme-accent" />
          <span>Priority Skill Gaps</span>
        </h2>

        {skillGaps.map((gap, index) => (
          <Card
            key={gap.skill}
            className="glass-card border-theme-primary/20 hover-lift scale-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <CardContent className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div
                    className={`w-3 h-3 rounded-full ${
                      gap.priority === "Critical"
                        ? "bg-red-500"
                        : gap.priority === "High"
                          ? "bg-orange-500"
                          : "bg-yellow-500"
                    }`}
                  />
                  <div>
                    <h3 className="text-xl font-semibold">{gap.skill}</h3>
                    <p className="text-muted-foreground text-sm">
                      {gap.gap}% skill gap • {gap.timeToClose} to close
                    </p>
                  </div>
                </div>
                <Badge
                  variant={
                    gap.priority === "Critical" ? "destructive" : gap.priority === "High" ? "default" : "secondary"
                  }
                >
                  {gap.priority} Priority
                </Badge>
              </div>

              {/* Skill Level Visualization */}
              <div className="space-y-4 mb-6">
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Current Level</span>
                    <span className="font-medium">{gap.currentLevel}%</span>
                  </div>
                  <Progress value={gap.currentLevel} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Target Level</span>
                    <span className="font-medium">{gap.targetLevel}%</span>
                  </div>
                  <Progress value={gap.targetLevel} className="h-2" />
                </div>
              </div>

              {/* Market Intelligence */}
              <div className="grid md:grid-cols-4 gap-4 mb-6">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4 text-green-600" />
                  <div>
                    <div className="text-sm font-medium">Market Demand</div>
                    <div className="text-xs text-muted-foreground">{gap.marketDemand}%</div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Zap className="h-4 w-4 text-blue-600" />
                  <div>
                    <div className="text-sm font-medium">Salary Impact</div>
                    <div className="text-xs text-muted-foreground">{gap.salaryImpact}</div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Target className="h-4 w-4 text-purple-600" />
                  <div>
                    <div className="text-sm font-medium">Job Openings</div>
                    <div className="text-xs text-muted-foreground">{gap.jobOpportunities.toLocaleString()}</div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <BookOpen className="h-4 w-4 text-orange-600" />
                  <div>
                    <div className="text-sm font-medium">Courses Available</div>
                    <div className="text-xs text-muted-foreground">{gap.recommendedCourses.length}</div>
                  </div>
                </div>
              </div>

              {/* Recommended Actions */}
              <div className="bg-theme-primary/5 rounded-lg p-4">
                <div className="flex items-start space-x-2 mb-3">
                  <AlertTriangle className="h-4 w-4 text-theme-primary mt-0.5" />
                  <div>
                    <div className="text-sm font-medium text-theme-primary">AI Recommendation</div>
                    <div className="text-sm text-muted-foreground">
                      Focus on {gap.skill} to unlock {gap.jobOpportunities.toLocaleString()} job opportunities and
                      increase your salary by {gap.salaryImpact}.
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div className="text-xs text-muted-foreground">
                    {gap.recommendedCourses.length} relevant courses found
                  </div>
                  <Button size="sm" className="bg-theme-gradient hover:opacity-90">
                    View Courses
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
