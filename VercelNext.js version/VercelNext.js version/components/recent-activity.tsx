import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Clock, FileText, Target, BookOpen } from "lucide-react"

const activities = [
  {
    id: 1,
    type: "resume",
    title: "Resume analyzed",
    description: "24 skills identified from your latest resume",
    time: "2 hours ago",
    icon: FileText,
  },
  {
    id: 2,
    type: "goal",
    title: "New career goal set",
    description: "Senior Full Stack Developer position added",
    time: "1 day ago",
    icon: Target,
  },
  {
    id: 3,
    type: "course",
    title: "Course recommendation",
    description: "Advanced React Patterns course suggested",
    time: "2 days ago",
    icon: BookOpen,
  },
  {
    id: 4,
    type: "analysis",
    title: "Skill gap analysis completed",
    description: "7 skill gaps identified for your target role",
    time: "3 days ago",
    icon: Target,
  },
]

export function RecentActivity() {
  return (
    <Card className="border-border">
      <CardHeader>
        <CardTitle>Recent Activity</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {activities.map((activity) => {
          const Icon = activity.icon
          return (
            <div
              key={activity.id}
              className="flex items-start space-x-3 p-3 rounded-lg hover:bg-muted/50 transition-colors"
            >
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
                  <Icon className="h-4 w-4 text-primary" />
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-sm">{activity.title}</p>
                <p className="text-sm text-muted-foreground">{activity.description}</p>
                <div className="flex items-center mt-1 text-xs text-muted-foreground">
                  <Clock className="h-3 w-3 mr-1" />
                  {activity.time}
                </div>
              </div>
            </div>
          )
        })}
      </CardContent>
    </Card>
  )
}
