import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Trophy, Star, Target, Zap, Award, BookOpen } from "lucide-react"

interface Achievement {
  id: string
  title: string
  description: string
  icon: string
  earned: boolean
  earnedDate?: string
  progress?: number
  maxProgress?: number
}

interface AchievementsProps {
  achievements: Achievement[]
}

export function Achievements({ achievements }: AchievementsProps) {
  const getIcon = (iconName: string) => {
    switch (iconName) {
      case "trophy":
        return <Trophy className="h-6 w-6" />
      case "star":
        return <Star className="h-6 w-6" />
      case "target":
        return <Target className="h-6 w-6" />
      case "zap":
        return <Zap className="h-6 w-6" />
      case "award":
        return <Award className="h-6 w-6" />
      default:
        return <BookOpen className="h-6 w-6" />
    }
  }

  const earnedAchievements = achievements.filter((a) => a.earned)
  const unlockedAchievements = achievements.filter((a) => !a.earned)

  return (
    <div className="space-y-6">
      {/* Summary */}
      <Card className="border-border">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Trophy className="h-5 w-5 text-primary" />
            <span>Achievements</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{earnedAchievements.length}</div>
              <div className="text-sm text-muted-foreground">Earned</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-muted-foreground">{unlockedAchievements.length}</div>
              <div className="text-sm text-muted-foreground">Available</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">
                {Math.round((earnedAchievements.length / achievements.length) * 100)}%
              </div>
              <div className="text-sm text-muted-foreground">Completion</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Earned Achievements */}
      {earnedAchievements.length > 0 && (
        <Card className="border-border">
          <CardHeader>
            <CardTitle>Earned Achievements</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              {earnedAchievements.map((achievement) => (
                <div
                  key={achievement.id}
                  className="flex items-start space-x-3 p-3 rounded-lg bg-primary/5 border border-primary/20"
                >
                  <div className="flex-shrink-0 text-primary">{getIcon(achievement.icon)}</div>
                  <div className="flex-1">
                    <h3 className="font-medium text-primary">{achievement.title}</h3>
                    <p className="text-sm text-muted-foreground">{achievement.description}</p>
                    {achievement.earnedDate && (
                      <p className="text-xs text-muted-foreground mt-1">Earned on {achievement.earnedDate}</p>
                    )}
                  </div>
                  <Badge variant="default" className="bg-primary/10 text-primary">
                    Earned
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Available Achievements */}
      {unlockedAchievements.length > 0 && (
        <Card className="border-border">
          <CardHeader>
            <CardTitle>Available Achievements</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              {unlockedAchievements.map((achievement) => (
                <div key={achievement.id} className="flex items-start space-x-3 p-3 rounded-lg bg-muted/30">
                  <div className="flex-shrink-0 text-muted-foreground">{getIcon(achievement.icon)}</div>
                  <div className="flex-1">
                    <h3 className="font-medium">{achievement.title}</h3>
                    <p className="text-sm text-muted-foreground">{achievement.description}</p>
                    {achievement.progress !== undefined && achievement.maxProgress && (
                      <div className="mt-2">
                        <div className="flex justify-between text-xs text-muted-foreground mb-1">
                          <span>
                            Progress: {achievement.progress}/{achievement.maxProgress}
                          </span>
                          <span>{Math.round((achievement.progress / achievement.maxProgress) * 100)}%</span>
                        </div>
                        <div className="w-full bg-muted rounded-full h-2">
                          <div
                            className="bg-primary h-2 rounded-full transition-all"
                            style={{ width: `${(achievement.progress / achievement.maxProgress) * 100}%` }}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                  <Badge variant="outline">Available</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
