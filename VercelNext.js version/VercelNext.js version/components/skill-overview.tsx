import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"

const skills = [
  { name: "JavaScript", level: 85, category: "Programming" },
  { name: "React", level: 78, category: "Frontend" },
  { name: "Node.js", level: 72, category: "Backend" },
  { name: "Python", level: 65, category: "Programming" },
  { name: "Machine Learning", level: 45, category: "AI/ML" },
  { name: "Docker", level: 38, category: "DevOps" },
]

const skillGaps = [
  { name: "Kubernetes", importance: "High", category: "DevOps" },
  { name: "TypeScript", importance: "High", category: "Programming" },
  { name: "AWS", importance: "Medium", category: "Cloud" },
  { name: "GraphQL", importance: "Medium", category: "Backend" },
]

export function SkillOverview() {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card className="border-border">
        <CardHeader>
          <CardTitle>Current Skills</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {skills.map((skill) => (
            <div key={skill.name} className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="font-medium">{skill.name}</span>
                  <Badge variant="secondary" className="text-xs">
                    {skill.category}
                  </Badge>
                </div>
                <span className="text-sm text-muted-foreground">{skill.level}%</span>
              </div>
              <Progress value={skill.level} className="h-2" />
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="border-border">
        <CardHeader>
          <CardTitle>Identified Skill Gaps</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {skillGaps.map((gap) => (
            <div key={gap.name} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
              <div className="flex items-center space-x-2">
                <span className="font-medium">{gap.name}</span>
                <Badge variant="secondary" className="text-xs">
                  {gap.category}
                </Badge>
              </div>
              <Badge variant={gap.importance === "High" ? "destructive" : "default"} className="text-xs">
                {gap.importance}
              </Badge>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
