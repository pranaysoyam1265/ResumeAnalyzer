import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CheckCircle, Clock, PlayCircle, ExternalLink } from "lucide-react"

interface CourseProgressItem {
  id: string
  title: string
  provider: string
  status: "completed" | "in-progress" | "not-started"
  progress: number
  completedLessons: number
  totalLessons: number
  timeSpent: string
  estimatedTimeRemaining: string
  skills: string[]
  priority: "Critical" | "High" | "Medium" | "Low"
}

interface CourseProgressProps {
  courses: CourseProgressItem[]
}

export function CourseProgress({ courses }: CourseProgressProps) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case "in-progress":
        return <PlayCircle className="h-4 w-4 text-blue-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
      case "in-progress":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
    }
  }

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

  const completedCourses = courses.filter((course) => course.status === "completed")
  const inProgressCourses = courses.filter((course) => course.status === "in-progress")
  const notStartedCourses = courses.filter((course) => course.status === "not-started")

  return (
    <div className="space-y-6">
      {/* Summary */}
      <Card className="border-border">
        <CardHeader>
          <CardTitle>Course Progress Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-500">{completedCourses.length}</div>
              <div className="text-sm text-muted-foreground">Completed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-500">{inProgressCourses.length}</div>
              <div className="text-sm text-muted-foreground">In Progress</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-500">{notStartedCourses.length}</div>
              <div className="text-sm text-muted-foreground">Not Started</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">
                {Math.round((completedCourses.length / courses.length) * 100)}%
              </div>
              <div className="text-sm text-muted-foreground">Overall Progress</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Course List */}
      <Card className="border-border">
        <CardHeader>
          <CardTitle>Your Courses</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {courses.map((course) => (
            <div key={course.id} className="border border-border rounded-lg p-4 space-y-3">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <div className={`w-2 h-2 rounded-full ${getPriorityColor(course.priority)}`} />
                    {getStatusIcon(course.status)}
                    <Badge className={`text-xs ${getStatusColor(course.status)}`}>
                      {course.status.replace("-", " ")}
                    </Badge>
                  </div>
                  <h3 className="font-medium text-lg">{course.title}</h3>
                  <p className="text-sm text-muted-foreground">{course.provider}</p>
                </div>
                <Button variant="outline" size="sm" className="bg-transparent">
                  <ExternalLink className="h-4 w-4 mr-1" />
                  Continue
                </Button>
              </div>

              {course.status !== "not-started" && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>
                      {course.completedLessons} of {course.totalLessons} lessons completed
                    </span>
                    <span>{course.progress}%</span>
                  </div>
                  <Progress value={course.progress} className="h-2" />
                </div>
              )}

              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <div className="flex items-center space-x-4">
                  <span>Time spent: {course.timeSpent}</span>
                  {course.status === "in-progress" && <span>Est. remaining: {course.estimatedTimeRemaining}</span>}
                </div>
              </div>

              <div className="flex flex-wrap gap-1">
                {course.skills.slice(0, 3).map((skill) => (
                  <Badge key={skill} variant="outline" className="text-xs">
                    {skill}
                  </Badge>
                ))}
                {course.skills.length > 3 && (
                  <Badge variant="outline" className="text-xs">
                    +{course.skills.length - 3} more
                  </Badge>
                )}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
