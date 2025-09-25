import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Star, Clock, Users, ExternalLink, BookOpen } from "lucide-react"

interface Course {
  id: string
  title: string
  provider: string
  description: string
  duration: string
  level: "Beginner" | "Intermediate" | "Advanced"
  rating: number
  students: number
  price: number
  skills: string[]
  matchScore: number
  priority: "Critical" | "High" | "Medium" | "Low"
  url: string
  image?: string
}

interface CourseCardProps {
  course: Course
}

export function CourseCard({ course }: CourseCardProps) {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "Critical":
        return "bg-red-500"
      case "High":
        return "bg-orange-500"
      case "Medium":
        return "bg-yellow-500"
      default:
        return "bg-green-500"
    }
  }

  const getLevelColor = (level: string) => {
    switch (level) {
      case "Beginner":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
      case "Intermediate":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
      case "Advanced":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
    }
  }

  return (
    <Card className="border-border hover:shadow-lg transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <div className={`w-2 h-2 rounded-full ${getPriorityColor(course.priority)}`} />
              <Badge variant="secondary" className="text-xs">
                {course.priority} Priority
              </Badge>
              <Badge className={`text-xs ${getLevelColor(course.level)}`}>{course.level}</Badge>
            </div>
            <h3 className="font-semibold text-lg leading-tight mb-1">{course.title}</h3>
            <p className="text-sm text-muted-foreground">{course.provider}</p>
          </div>
          <div className="text-right">
            <div className="text-lg font-bold text-primary">{course.matchScore}%</div>
            <div className="text-xs text-muted-foreground">Match</div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-muted-foreground line-clamp-3">{course.description}</p>

        <div className="flex items-center space-x-4 text-sm text-muted-foreground">
          <div className="flex items-center space-x-1">
            <Clock className="h-4 w-4" />
            <span>{course.duration}</span>
          </div>
          <div className="flex items-center space-x-1">
            <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
            <span>{course.rating}</span>
          </div>
          <div className="flex items-center space-x-1">
            <Users className="h-4 w-4" />
            <span>{course.students.toLocaleString()}</span>
          </div>
        </div>

        <div className="space-y-2">
          <div className="text-sm font-medium">Skills you'll learn:</div>
          <div className="flex flex-wrap gap-1">
            {course.skills.slice(0, 4).map((skill) => (
              <Badge key={skill} variant="outline" className="text-xs">
                {skill}
              </Badge>
            ))}
            {course.skills.length > 4 && (
              <Badge variant="outline" className="text-xs">
                +{course.skills.length - 4} more
              </Badge>
            )}
          </div>
        </div>

        <div className="flex items-center justify-between pt-2">
          <div className="text-lg font-bold">{course.price === 0 ? "Free" : `$${course.price}`}</div>
          <div className="flex space-x-2">
            <Button variant="outline" size="sm" className="bg-transparent">
              <BookOpen className="h-4 w-4 mr-1" />
              Details
            </Button>
            <Button size="sm">
              <ExternalLink className="h-4 w-4 mr-1" />
              Enroll
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
