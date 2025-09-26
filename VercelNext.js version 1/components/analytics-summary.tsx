"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { TrendingUp, TrendingDown, Clock, Award, Zap } from "lucide-react"

interface AnalyticsSummaryProps {
  className?: string
}

export function AnalyticsSummary({ className }: AnalyticsSummaryProps) {
  const summaryData = {
    weeklyHours: 18.5,
    weeklyChange: 12.3,
    skillsProgress: 75,
    focusScore: 92,
    streakDays: 15,
    completionRate: 87,
  }

  return (
    <Card
      className={`backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20 ${className}`}
    >
      <CardHeader>
        <CardTitle className="text-lg">Weekly Summary</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-600 dark:text-slate-400">Hours Studied</span>
              <div className="flex items-center">
                {summaryData.weeklyChange > 0 ? (
                  <TrendingUp className="w-3 h-3 text-green-600 mr-1" />
                ) : (
                  <TrendingDown className="w-3 h-3 text-red-600 mr-1" />
                )}
                <span className="text-xs text-slate-500">+{summaryData.weeklyChange}%</span>
              </div>
            </div>
            <div className="flex items-center">
              <Clock className="w-4 h-4 text-blue-600 mr-2" />
              <span className="text-lg font-semibold">{summaryData.weeklyHours}h</span>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-600 dark:text-slate-400">Focus Score</span>
              <Badge variant="secondary" className="text-xs">
                Excellent
              </Badge>
            </div>
            <div className="flex items-center">
              <Zap className="w-4 h-4 text-orange-600 mr-2" />
              <span className="text-lg font-semibold">{summaryData.focusScore}%</span>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          <div>
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm text-slate-600 dark:text-slate-400">Skills Progress</span>
              <span className="text-sm font-medium">{summaryData.skillsProgress}%</span>
            </div>
            <Progress value={summaryData.skillsProgress} className="h-2" />
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm text-slate-600 dark:text-slate-400">Completion Rate</span>
              <span className="text-sm font-medium">{summaryData.completionRate}%</span>
            </div>
            <Progress value={summaryData.completionRate} className="h-2" />
          </div>
        </div>

        <div className="flex items-center justify-between pt-2 border-t border-slate-200 dark:border-slate-700">
          <div className="flex items-center">
            <Award className="w-4 h-4 text-yellow-600 mr-2" />
            <span className="text-sm text-slate-600 dark:text-slate-400">Learning Streak</span>
          </div>
          <Badge variant="outline" className="text-sm">
            {summaryData.streakDays} days
          </Badge>
        </div>
      </CardContent>
    </Card>
  )
}
