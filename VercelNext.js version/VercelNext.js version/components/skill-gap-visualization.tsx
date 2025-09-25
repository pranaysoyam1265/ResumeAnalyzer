import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { TrendingUp, AlertTriangle, CheckCircle, Target, Clock, DollarSign, BarChart3 } from "lucide-react"

interface SkillGap {
  skill: string
  category: string
  currentLevel: number
  requiredLevel: number
  importance: "Critical" | "High" | "Medium" | "Low"
  gap: number
  skillType?: "Essential" | "Competitive"
  marketTrend?: "Growing" | "Stable" | "Declining"
  timeToAcquire?: string
  learningPath?: string
  jobPostingFrequency?: number
  salaryImpact?: string
  armaForecast?: string
}

interface SkillGapVisualizationProps {
  gaps: SkillGap[]
  targetRole: string
}

export function SkillGapVisualization({ gaps, targetRole }: SkillGapVisualizationProps) {
  const essentialGaps = gaps.filter((gap) => gap.skillType === "Essential" && gap.gap > 0)
  const competitiveGaps = gaps.filter((gap) => gap.skillType === "Competitive" && gap.gap > 0)
  const criticalGaps = gaps.filter((gap) => gap.importance === "Critical" && gap.gap > 0)
  const strengths = gaps.filter((gap) => gap.gap <= 0)
  const growingSkills = gaps.filter((gap) => gap.marketTrend === "Growing")

  const getGapColor = (importance: string) => {
    switch (importance) {
      case "Critical":
        return "text-red-500"
      case "High":
        return "text-orange-500"
      case "Medium":
        return "text-yellow-500"
      default:
        return "text-green-500"
    }
  }

  const getGapIcon = (importance: string) => {
    switch (importance) {
      case "Critical":
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      case "High":
        return <TrendingUp className="h-4 w-4 text-orange-500" />
      case "Medium":
        return <Target className="h-4 w-4 text-yellow-500" />
      default:
        return <CheckCircle className="h-4 w-4 text-green-500" />
    }
  }

  const getSkillTypeColor = (skillType: string) => {
    return skillType === "Essential" ? "bg-blue-100 text-blue-800" : "bg-purple-100 text-purple-800"
  }

  return (
    <div className="space-y-6">
      {/* Enhanced Summary with Two-Tier Analysis */}
      <Card className="border-border">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Target className="h-5 w-5 text-primary" />
            <span>AI-Powered Gap Analysis for {targetRole}</span>
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            Using ARIMA forecasting and time series analysis for strategic skill prioritization
          </p>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-red-500">{criticalGaps.length}</div>
              <div className="text-sm text-muted-foreground">Critical Gaps</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{essentialGaps.length}</div>
              <div className="text-sm text-muted-foreground">Essential Skills</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{competitiveGaps.length}</div>
              <div className="text-sm text-muted-foreground">Competitive Edge</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-500">{growingSkills.length}</div>
              <div className="text-sm text-muted-foreground">Growing Trends</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-500">{strengths.length}</div>
              <div className="text-sm text-muted-foreground">Strengths</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Strategic Priority Alert */}
      {criticalGaps.length > 0 && (
        <Alert className="border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-950/20">
          <AlertTriangle className="h-4 w-4 text-red-500" />
          <AlertDescription className="text-red-700 dark:text-red-300">
            <strong>Strategic Priority:</strong> You have {criticalGaps.length} critical foundational skills that are
            essential for the {targetRole} role. These should be your immediate focus as they represent barriers to job
            entry.
          </AlertDescription>
        </Alert>
      )}

      {/* Two-Tier Analysis Cards */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card className="border-border">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="h-5 w-5 text-blue-500" />
              <span>Foundational Skills (Essential for Job Entry)</span>
            </CardTitle>
            <p className="text-sm text-muted-foreground">Core competencies required to meet minimum job requirements</p>
          </CardHeader>
          <CardContent className="space-y-4">
            {essentialGaps.slice(0, 4).map((gap) => (
              <div key={gap.skill} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium">{gap.skill}</span>
                    <Badge className={getSkillTypeColor(gap.skillType || "Essential")} variant="secondary">
                      Essential
                    </Badge>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Clock className="h-3 w-3 text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">{gap.timeToAcquire}</span>
                  </div>
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span>Current: {gap.currentLevel}%</span>
                    <span>Required: {gap.requiredLevel}%</span>
                  </div>
                  <Progress value={gap.currentLevel} className="h-2" />
                  <div className="text-xs text-muted-foreground">
                    Gap: {gap.gap}% • {gap.armaForecast}
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="border-border">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-purple-500" />
              <span>Trending Skills (Competitive Advantage)</span>
            </CardTitle>
            <p className="text-sm text-muted-foreground">
              Emerging skills that provide market differentiation and career acceleration
            </p>
          </CardHeader>
          <CardContent className="space-y-4">
            {competitiveGaps.slice(0, 4).map((gap) => (
              <div key={gap.skill} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium">{gap.skill}</span>
                    <Badge className={getSkillTypeColor(gap.skillType || "Competitive")} variant="secondary">
                      Competitive
                    </Badge>
                  </div>
                  <div className="flex items-center space-x-2">
                    <DollarSign className="h-3 w-3 text-green-500" />
                    <span className="text-xs text-green-600">{gap.salaryImpact}</span>
                  </div>
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span>Current: {gap.currentLevel}%</span>
                    <span>Required: {gap.requiredLevel}%</span>
                  </div>
                  <Progress value={gap.currentLevel} className="h-2" />
                  <div className="text-xs text-muted-foreground">
                    Gap: {gap.gap}% • {gap.armaForecast}
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Detailed Market Intelligence Analysis */}
      <Card className="border-border">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <BarChart3 className="h-5 w-5 text-primary" />
            <span>Market Intelligence & Learning Pathways</span>
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            Time series analysis with ARIMA forecasting and personalized learning recommendations
          </p>
        </CardHeader>
        <CardContent className="space-y-6">
          {gaps
            .filter((gap) => gap.gap > 0)
            .map((gap) => (
              <div key={gap.skill} className="space-y-4 p-4 bg-muted/30 rounded-lg">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {getGapIcon(gap.importance)}
                    <div>
                      <span className="font-medium text-lg">{gap.skill}</span>
                      <div className="flex items-center space-x-2 mt-1">
                        <Badge variant="secondary" className="text-xs">
                          {gap.category}
                        </Badge>
                        <Badge className={getSkillTypeColor(gap.skillType || "Essential")} variant="secondary">
                          {gap.skillType}
                        </Badge>
                        <Badge variant={gap.importance === "Critical" ? "destructive" : "default"} className="text-xs">
                          {gap.importance}
                        </Badge>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-medium text-red-500">Gap: {gap.gap}%</div>
                    <div className="text-xs text-muted-foreground">{gap.timeToAcquire}</div>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Current Level</span>
                      <span>{gap.currentLevel}%</span>
                    </div>
                    <Progress value={gap.currentLevel} className="h-3" />

                    <div className="flex justify-between text-sm">
                      <span>Required Level</span>
                      <span>{gap.requiredLevel}%</span>
                    </div>
                    <Progress value={gap.requiredLevel} className="h-3 opacity-50" />
                  </div>

                  <div className="space-y-2 text-sm">
                    <div className="flex items-center justify-between">
                      <span className="text-muted-foreground">Market Demand:</span>
                      <span className="font-medium">{gap.jobPostingFrequency?.toLocaleString()} jobs</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-muted-foreground">Salary Impact:</span>
                      <span className="font-medium text-green-600">{gap.salaryImpact}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-muted-foreground">ARIMA Forecast:</span>
                      <span className="font-medium text-blue-600">{gap.armaForecast}</span>
                    </div>
                  </div>
                </div>

                {gap.learningPath && (
                  <div className="mt-3 p-3 bg-background rounded border">
                    <div className="text-sm font-medium mb-1">Recommended Learning Path:</div>
                    <div className="text-sm text-muted-foreground">{gap.learningPath}</div>
                  </div>
                )}
              </div>
            ))}
        </CardContent>
      </Card>

      {/* Strengths Section */}
      {strengths.length > 0 && (
        <Card className="border-border">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-green-500" />
              <span>Your Competitive Strengths</span>
            </CardTitle>
            <p className="text-sm text-muted-foreground">Skills where you exceed the required level for {targetRole}</p>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              {strengths.map((strength) => (
                <div
                  key={strength.skill}
                  className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-950/20 rounded-lg"
                >
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span className="font-medium">{strength.skill}</span>
                    <Badge variant="secondary" className="text-xs">
                      {strength.category}
                    </Badge>
                  </div>
                  <div className="text-sm text-green-600">+{Math.abs(strength.gap)}% above required</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
