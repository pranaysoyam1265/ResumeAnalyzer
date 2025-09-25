"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Target, Clock, Award, ArrowRight, CheckCircle } from "lucide-react"

interface LearningPathBuilderProps {
  courses: any[]
  userGoals: string[]
}

export function LearningPathBuilder({ courses, userGoals }: LearningPathBuilderProps) {
  const [selectedPath, setSelectedPath] = useState("full-stack")

  const learningPaths = {
    "full-stack": {
      title: "Full-Stack Developer Path",
      description: "Become a complete full-stack developer with modern technologies",
      duration: "6-8 months",
      difficulty: "Intermediate",
      courses: [
        { ...courses[1], order: 1, status: "completed" },
        { ...courses[0], order: 2, status: "in-progress" },
        { ...courses[3], order: 3, status: "locked" },
        { ...courses[4], order: 4, status: "locked" },
      ],
      skills: ["TypeScript", "React", "Node.js", "Kubernetes", "AWS"],
      outcomes: ["Build scalable web applications", "Deploy to cloud platforms", "Implement CI/CD pipelines"],
    },
    "ai-ml": {
      title: "AI/ML Engineer Path",
      description: "Master artificial intelligence and machine learning technologies",
      duration: "8-10 months",
      difficulty: "Advanced",
      courses: [
        { ...courses[1], order: 1, status: "completed" },
        { ...courses[2], order: 2, status: "in-progress" },
        { ...courses[0], order: 3, status: "locked" },
      ],
      skills: ["Python", "TensorFlow", "PyTorch", "MLOps", "Data Science"],
      outcomes: ["Build ML models", "Deploy AI systems", "Implement MLOps pipelines"],
    },
  }

  const currentPath = learningPaths[selectedPath as keyof typeof learningPaths]
  const completedCourses = currentPath.courses.filter((c) => c.status === "completed").length
  const progressPercentage = (completedCourses / currentPath.courses.length) * 100

  return (
    <div className="space-y-8">
      {/* Path Selection */}
      <Card className="glass-card border-theme-secondary/20 hover-lift">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Target className="h-6 w-6 text-theme-secondary" />
            <span>AI-Generated Learning Paths</span>
          </CardTitle>
          <p className="text-muted-foreground">
            Structured learning journeys optimized for your career goals and current skill level
          </p>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-4">
            {Object.entries(learningPaths).map(([key, path]) => (
              <Card
                key={key}
                className={`cursor-pointer transition-all hover-lift ${
                  selectedPath === key
                    ? "border-theme-secondary bg-theme-secondary/5"
                    : "border-border hover:border-theme-secondary/50"
                }`}
                onClick={() => setSelectedPath(key)}
              >
                <CardContent className="p-4">
                  <h3 className="font-semibold mb-2">{path.title}</h3>
                  <p className="text-sm text-muted-foreground mb-3">{path.description}</p>
                  <div className="flex items-center justify-between text-xs">
                    <Badge variant="outline">{path.difficulty}</Badge>
                    <span className="text-muted-foreground">{path.duration}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Selected Path Details */}
      <Card className="glass-card border-theme-accent/20 hover-lift">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl">{currentPath.title}</CardTitle>
              <p className="text-muted-foreground mt-1">{currentPath.description}</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-theme-accent">{Math.round(progressPercentage)}%</div>
              <div className="text-sm text-muted-foreground">Complete</div>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Progress Overview */}
          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span>Overall Progress</span>
              <span>
                {completedCourses} of {currentPath.courses.length} courses
              </span>
            </div>
            <Progress value={progressPercentage} className="h-3" />
          </div>

          {/* Path Metadata */}
          <div className="grid md:grid-cols-3 gap-4">
            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4 text-muted-foreground" />
              <div>
                <div className="text-sm font-medium">Duration</div>
                <div className="text-xs text-muted-foreground">{currentPath.duration}</div>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Target className="h-4 w-4 text-muted-foreground" />
              <div>
                <div className="text-sm font-medium">Difficulty</div>
                <div className="text-xs text-muted-foreground">{currentPath.difficulty}</div>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Award className="h-4 w-4 text-muted-foreground" />
              <div>
                <div className="text-sm font-medium">Courses</div>
                <div className="text-xs text-muted-foreground">{currentPath.courses.length} total</div>
              </div>
            </div>
          </div>

          {/* Course Sequence */}
          <div className="space-y-4">
            <h3 className="font-semibold">Learning Sequence</h3>
            {currentPath.courses.map((course, index) => (
              <div key={course.id} className="flex items-center space-x-4">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                    course.status === "completed"
                      ? "bg-green-100 text-green-700"
                      : course.status === "in-progress"
                        ? "bg-blue-100 text-blue-700"
                        : "bg-gray-100 text-gray-500"
                  }`}
                >
                  {course.status === "completed" ? <CheckCircle className="h-4 w-4" /> : course.order}
                </div>

                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium">{course.title}</h4>
                      <p className="text-sm text-muted-foreground">
                        {course.provider} • {course.duration}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge
                        variant={
                          course.status === "completed"
                            ? "default"
                            : course.status === "in-progress"
                              ? "secondary"
                              : "outline"
                        }
                        className="text-xs"
                      >
                        {course.status === "completed"
                          ? "Completed"
                          : course.status === "in-progress"
                            ? "In Progress"
                            : "Locked"}
                      </Badge>
                      {course.status !== "locked" && (
                        <Button size="sm" variant="outline">
                          {course.status === "completed" ? "Review" : "Continue"}
                        </Button>
                      )}
                    </div>
                  </div>
                </div>

                {index < currentPath.courses.length - 1 && <ArrowRight className="h-4 w-4 text-muted-foreground" />}
              </div>
            ))}
          </div>

          {/* Expected Outcomes */}
          <div className="space-y-3">
            <h3 className="font-semibold">What You'll Achieve</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium mb-2">Skills You'll Master</h4>
                <div className="flex flex-wrap gap-2">
                  {currentPath.skills.map((skill) => (
                    <Badge key={skill} variant="secondary" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="text-sm font-medium mb-2">Career Outcomes</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  {currentPath.outcomes.map((outcome, index) => (
                    <li key={index} className="flex items-center space-x-2">
                      <CheckCircle className="h-3 w-3 text-green-600" />
                      <span>{outcome}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
