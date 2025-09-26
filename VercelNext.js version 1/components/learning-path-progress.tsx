import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { BookOpen, Clock, Award, TrendingUp, CheckCircle } from "lucide-react"

const learningPaths = [
  {
    title: "Full-Stack AI Developer",
    progress: 68,
    totalCourses: 12,
    completedCourses: 8,
    estimatedTime: "6 weeks",
    difficulty: "Advanced",
    skills: ["Python", "TensorFlow", "React", "Node.js"],
    nextMilestone: "Deploy ML Model to Production",
    status: "active" as const,
  },
  {
    title: "Cloud Architecture Specialist",
    progress: 35,
    totalCourses: 8,
    completedCourses: 3,
    estimatedTime: "4 weeks",
    difficulty: "Intermediate",
    skills: ["AWS", "Kubernetes", "Docker", "Terraform"],
    nextMilestone: "AWS Solutions Architect Certification",
    status: "active" as const,
  },
  {
    title: "Data Science Fundamentals",
    progress: 100,
    totalCourses: 6,
    completedCourses: 6,
    estimatedTime: "Completed",
    difficulty: "Beginner",
    skills: ["Python", "Pandas", "Matplotlib", "Statistics"],
    nextMilestone: "Certificate Earned",
    status: "completed" as const,
  },
]

export function LearningPathProgress() {
  return (
    <Card className="glass-card border-theme-accent/20 hover-lift">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <BookOpen className="h-5 w-5 text-theme-accent" />
          <span>Personalized Learning Paths</span>
        </CardTitle>
        <p className="text-muted-foreground text-sm">
          AI-curated learning journeys tailored to your career goals and skill gaps
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {learningPaths.map((path, index) => (
          <div
            key={path.title}
            className="glass p-5 rounded-xl hover-lift fade-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="space-y-4">
              <div className="flex items-start justify-between">
                <div className="space-y-2">
                  <div className="flex items-center space-x-3">
                    <h3 className="font-semibold text-lg">{path.title}</h3>
                    {path.status === "completed" ? (
                      <Badge className="bg-green-100 text-green-700 border-green-200">
                        <CheckCircle className="h-3 w-3 mr-1" />
                        Completed
                      </Badge>
                    ) : (
                      <Badge className="bg-blue-100 text-blue-700 border-blue-200">
                        <TrendingUp className="h-3 w-3 mr-1" />
                        In Progress
                      </Badge>
                    )}
                  </div>
                  <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                    <div className="flex items-center space-x-1">
                      <BookOpen className="h-4 w-4" />
                      <span>
                        {path.completedCourses}/{path.totalCourses} courses
                      </span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Clock className="h-4 w-4" />
                      <span>{path.estimatedTime}</span>
                    </div>
                    <Badge variant="outline" className="text-xs">
                      {path.difficulty}
                    </Badge>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-theme-primary">{path.progress}%</div>
                  <div className="text-xs text-muted-foreground">Complete</div>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Progress</span>
                  <span className="font-medium">{path.progress}%</span>
                </div>
                <Progress value={path.progress} className="h-3" />
              </div>

              <div className="space-y-3">
                <div>
                  <div className="text-sm font-medium mb-2">Key Skills</div>
                  <div className="flex flex-wrap gap-2">
                    {path.skills.map((skill) => (
                      <Badge key={skill} variant="secondary" className="text-xs">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium">Next Milestone</div>
                    <div className="text-sm text-muted-foreground">{path.nextMilestone}</div>
                  </div>
                  {path.status === "active" && (
                    <Button size="sm" className="bg-theme-gradient hover:opacity-90">
                      Continue Learning
                    </Button>
                  )}
                  {path.status === "completed" && (
                    <Button size="sm" variant="outline" className="border-green-200 text-green-700 bg-transparent">
                      <Award className="h-4 w-4 mr-1" />
                      View Certificate
                    </Button>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
