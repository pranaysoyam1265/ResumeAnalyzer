import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Target, BookOpen, TrendingUp, Brain } from "lucide-react"

export function DashboardStats() {
  const stats = [
    {
      title: "Skills Identified",
      value: "24",
      change: "+3 this week",
      changeType: "positive" as const,
      icon: Brain,
      description: "From AI-powered resume analysis",
      progress: 85,
      color: "text-slate-600",
      bgColor: "bg-slate-100",
    },
    {
      title: "Skill Gaps",
      value: "7",
      change: "-2 closed",
      changeType: "positive" as const,
      icon: Target,
      description: "High-priority areas for growth",
      progress: 65,
      color: "text-orange-600",
      bgColor: "bg-orange-100",
    },
    {
      title: "Learning Progress",
      value: "68%",
      change: "+12% this month",
      changeType: "positive" as const,
      icon: TrendingUp,
      description: "Towards career objectives",
      progress: 68,
      color: "text-green-600",
      bgColor: "bg-green-100",
    },
    {
      title: "Course Recommendations",
      value: "12",
      change: "4 new matches",
      changeType: "neutral" as const,
      icon: BookOpen,
      description: "AI-curated for your goals",
      progress: 90,
      color: "text-blue-600",
      bgColor: "bg-blue-100",
    },
  ]

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat, index) => {
        const Icon = stat.icon
        return (
          <Card
            key={stat.title}
            className="glass-card border-slate-200 hover-lift scale-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
              <div className="space-y-1">
                <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
                <div className="flex items-center space-x-2">
                  <div className="text-3xl font-bold">{stat.value}</div>
                  <Badge
                    variant="secondary"
                    className={`text-xs ${
                      stat.changeType === "positive"
                        ? "bg-green-100 text-green-700"
                        : stat.changeType === "negative"
                          ? "bg-red-100 text-red-700"
                          : "bg-gray-100 text-gray-700"
                    }`}
                  >
                    {stat.change}
                  </Badge>
                </div>
              </div>
              <div className={`w-12 h-12 ${stat.bgColor} rounded-full flex items-center justify-center`}>
                <Icon className={`h-6 w-6 ${stat.color}`} />
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-xs text-muted-foreground">{stat.description}</p>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-muted-foreground">Progress</span>
                  <span className="font-medium">{stat.progress}%</span>
                </div>
                <Progress value={stat.progress} className="h-2" />
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
