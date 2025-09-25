"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Brain, Target, TrendingUp, Zap, Star, Users, DollarSign } from "lucide-react"

interface RecommendationEngineProps {
  recommendations: any[]
  userPreferences: any
  onPreferencesChange: (preferences: any) => void
}

export function RecommendationEngine({
  recommendations,
  userPreferences,
  onPreferencesChange,
}: RecommendationEngineProps) {
  return (
    <div className="space-y-8">
      {/* AI Recommendation Header */}
      <Card className="glass-card border-theme-primary/20 hover-lift">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Brain className="h-6 w-6 text-theme-primary" />
            <span>AI-Powered Course Recommendations</span>
          </CardTitle>
          <p className="text-muted-foreground">
            Our machine learning algorithm analyzed 10,000+ courses, your skill profile, and current market trends to
            curate these personalized recommendations.
          </p>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-theme-primary/10 rounded-full flex items-center justify-center">
                <Target className="h-5 w-5 text-theme-primary" />
              </div>
              <div>
                <h3 className="font-semibold">Skill Gap Analysis</h3>
                <p className="text-sm text-muted-foreground">Identifies critical missing skills</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-theme-secondary/10 rounded-full flex items-center justify-center">
                <TrendingUp className="h-5 w-5 text-theme-secondary" />
              </div>
              <div>
                <h3 className="font-semibold">Market Intelligence</h3>
                <p className="text-sm text-muted-foreground">Real-time industry demand data</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-theme-accent/10 rounded-full flex items-center justify-center">
                <Zap className="h-5 w-5 text-theme-accent" />
              </div>
              <div>
                <h3 className="font-semibold">Career Impact</h3>
                <p className="text-sm text-muted-foreground">Predicts salary and job prospects</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Top AI Recommendations */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold flex items-center space-x-2">
          <Zap className="h-6 w-6 text-theme-primary" />
          <span>Top AI Picks for You</span>
        </h2>

        {recommendations.map((course, index) => (
          <Card
            key={course.id}
            className="glass-card border-theme-primary/20 hover-lift scale-in"
            style={{ animationDelay: `${index * 0.2}s` }}
          >
            <CardContent className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-theme-gradient rounded-full flex items-center justify-center text-white font-bold">
                    #{index + 1}
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-1">{course.title}</h3>
                    <p className="text-muted-foreground text-sm">{course.provider}</p>
                  </div>
                </div>
                <Badge className="bg-theme-primary/10 text-theme-primary border-theme-primary/20">
                  {course.matchScore}% Match
                </Badge>
              </div>

              <p className="text-muted-foreground mb-4">{course.description}</p>

              {/* AI Insights Grid */}
              <div className="grid md:grid-cols-4 gap-4 mb-4">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4 text-green-600" />
                  <div>
                    <div className="text-sm font-medium">Market Demand</div>
                    <div className="text-xs text-muted-foreground">{course.aiInsights.marketDemand}%</div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <DollarSign className="h-4 w-4 text-blue-600" />
                  <div>
                    <div className="text-sm font-medium">Salary Impact</div>
                    <div className="text-xs text-muted-foreground">{course.aiInsights.salaryImpact}</div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Users className="h-4 w-4 text-purple-600" />
                  <div>
                    <div className="text-sm font-medium">Success Rate</div>
                    <div className="text-xs text-muted-foreground">{course.aiInsights.completionRate}%</div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Star className="h-4 w-4 text-yellow-600" />
                  <div>
                    <div className="text-sm font-medium">Rating</div>
                    <div className="text-xs text-muted-foreground">{course.rating}/5.0</div>
                  </div>
                </div>
              </div>

              {/* AI Recommendation Reason */}
              <div className="bg-theme-primary/5 rounded-lg p-4 mb-4">
                <div className="flex items-start space-x-2">
                  <Brain className="h-4 w-4 text-theme-primary mt-0.5" />
                  <div>
                    <div className="text-sm font-medium text-theme-primary mb-1">Why AI recommends this:</div>
                    <div className="text-sm text-muted-foreground">{course.reason}</div>
                  </div>
                </div>
              </div>

              {/* Skills and Actions */}
              <div className="flex items-center justify-between">
                <div className="flex flex-wrap gap-2">
                  {course.skills.slice(0, 4).map((skill: string) => (
                    <Badge key={skill} variant="secondary" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                  {course.skills.length > 4 && (
                    <Badge variant="outline" className="text-xs">
                      +{course.skills.length - 4} more
                    </Badge>
                  )}
                </div>
                <div className="flex items-center space-x-2">
                  <Button variant="outline" size="sm">
                    Learn More
                  </Button>
                  <Button className="bg-theme-gradient hover:opacity-90" size="sm">
                    Start Learning
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
