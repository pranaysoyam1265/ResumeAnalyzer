import { redirect } from "next/navigation"
import { createClient } from "@/lib/supabase/server"
import { DashboardNav } from "@/components/dashboard-nav"
import { DashboardStats } from "@/components/dashboard-stats"
import { SkillOverview } from "@/components/skill-overview"
import { RecentActivity } from "@/components/recent-activity"
import { SkillRadarChart } from "@/components/skill-radar-chart"
import { MarketTrendsChart } from "@/components/market-trends-chart"
import { LearningPathProgress } from "@/components/learning-path-progress"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Upload, Target, BookOpen, TrendingUp, Brain, Zap } from "lucide-react"
import Link from "next/link"

export default async function DashboardPage() {
  const supabase = await createClient()

  const {
    data: { user },
    error,
  } = await supabase.auth.getUser()
  if (error || !user) {
    redirect("/auth/login")
  }

  return (
    <div className="min-h-screen bg-background theme-dashboard">
      <DashboardNav />
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-theme-gradient mb-2">
            Welcome back, {user.user_metadata?.full_name || user.email?.split("@")[0] || "there"}!
          </h1>
          <p className="text-muted-foreground text-lg">
            Your AI-powered career development dashboard with real-time market insights
          </p>
        </div>

        <div className="space-y-8">
          {/* Enhanced Stats Overview */}
          <DashboardStats />

          <Card className="glass-card border-theme-primary/20 hover-lift">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="h-5 w-5 text-theme-primary" />
                <span>AI-Powered Quick Actions</span>
              </CardTitle>
              <p className="text-muted-foreground text-sm">
                Intelligent recommendations based on your career profile and market trends
              </p>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-3">
                <Button
                  asChild
                  variant="outline"
                  className="glass-nav h-auto p-6 flex flex-col items-center space-y-3 bg-transparent border-theme-primary/30 hover:bg-theme-primary/10 hover-lift focus-theme"
                >
                  <Link href="/dashboard/resume">
                    <div className="w-12 h-12 bg-theme-gradient rounded-full flex items-center justify-center mb-2">
                      <Upload className="h-6 w-6 text-white" />
                    </div>
                    <span className="font-semibold">Analyze Resume</span>
                    <span className="text-xs text-muted-foreground text-center">
                      Advanced NLP skill extraction with market intelligence
                    </span>
                    <div className="text-xs text-theme-primary font-medium">Last analysis: 2 days ago</div>
                  </Link>
                </Button>
                <Button
                  asChild
                  variant="outline"
                  className="glass-nav h-auto p-6 flex flex-col items-center space-y-3 bg-transparent border-theme-secondary/30 hover:bg-theme-secondary/10 hover-lift focus-theme"
                >
                  <Link href="/dashboard/goals">
                    <div className="w-12 h-12 bg-theme-gradient rounded-full flex items-center justify-center mb-2">
                      <Target className="h-6 w-6 text-white" />
                    </div>
                    <span className="font-semibold">Career Goals</span>
                    <span className="text-xs text-muted-foreground text-center">
                      Strategic skill gap analysis and goal setting
                    </span>
                    <div className="text-xs text-theme-secondary font-medium">7 active goals</div>
                  </Link>
                </Button>
                <Button
                  asChild
                  variant="outline"
                  className="glass-nav h-auto p-6 flex flex-col items-center space-y-3 bg-transparent border-theme-accent/30 hover:bg-theme-accent/10 hover-lift focus-theme"
                >
                  <Link href="/dashboard/recommendations">
                    <div className="w-12 h-12 bg-theme-gradient rounded-full flex items-center justify-center mb-2">
                      <BookOpen className="h-6 w-6 text-white" />
                    </div>
                    <span className="font-semibold">Smart Courses</span>
                    <span className="text-xs text-muted-foreground text-center">
                      Personalized learning paths with AI recommendations
                    </span>
                    <div className="text-xs text-theme-accent font-medium">12 new recommendations</div>
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>

          <div className="grid gap-8 lg:grid-cols-2">
            <Card className="glass-card border-theme-primary/20 hover-lift">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-theme-primary" />
                  <span>Skill Proficiency Radar</span>
                </CardTitle>
                <p className="text-muted-foreground text-sm">
                  Interactive visualization of your skill portfolio across key domains
                </p>
              </CardHeader>
              <CardContent>
                <SkillRadarChart />
              </CardContent>
            </Card>

            <Card className="glass-card border-theme-secondary/20 hover-lift">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <TrendingUp className="h-5 w-5 text-theme-secondary" />
                  <span>Market Trends Analysis</span>
                </CardTitle>
                <p className="text-muted-foreground text-sm">Real-time skill demand trends and growth predictions</p>
              </CardHeader>
              <CardContent>
                <MarketTrendsChart />
              </CardContent>
            </Card>
          </div>

          {/* Enhanced Skills Overview */}
          <SkillOverview />

          <LearningPathProgress />

          {/* Recent Activity */}
          <RecentActivity />
        </div>
      </div>
    </div>
  )
}
