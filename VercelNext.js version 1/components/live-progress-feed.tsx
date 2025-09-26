"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Activity, CheckCircle, Target, BookOpen, Trophy, Clock } from "lucide-react"

interface LiveProgressFeedProps {
  updates: any[]
}

export function LiveProgressFeed({ updates }: LiveProgressFeedProps) {
  const getUpdateIcon = (type: string) => {
    switch (type) {
      case "progress":
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case "milestone":
        return <Target className="h-4 w-4 text-blue-500" />
      case "achievement":
        return <Trophy className="h-4 w-4 text-yellow-500" />
      case "course":
        return <BookOpen className="h-4 w-4 text-purple-500" />
      default:
        return <Activity className="h-4 w-4 text-gray-500" />
    }
  }

  const getUpdateColor = (type: string) => {
    switch (type) {
      case "progress":
        return "border-green-200 bg-green-50"
      case "milestone":
        return "border-blue-200 bg-blue-50"
      case "achievement":
        return "border-yellow-200 bg-yellow-50"
      case "course":
        return "border-purple-200 bg-purple-50"
      default:
        return "border-gray-200 bg-gray-50"
    }
  }

  return (
    <Card className="glass-card border-theme-accent/20 hover-lift">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Activity className="h-5 w-5 text-theme-accent animate-pulse" />
          <span>Live Progress Feed</span>
          <Badge className="bg-green-100 text-green-700 border-green-200">Real-time</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {updates.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p>No recent activity</p>
            <p className="text-xs">Start learning to see live updates here</p>
          </div>
        ) : (
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {updates.map((update, index) => (
              <div
                key={update.id}
                className={`flex items-start space-x-3 p-3 rounded-lg border transition-all hover-lift scale-in ${getUpdateColor(update.type)}`}
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex-shrink-0 mt-0.5">{getUpdateIcon(update.type)}</div>
                <div className="flex-1">
                  <p className="text-sm font-medium">{update.message}</p>
                  <div className="flex items-center space-x-2 mt-1">
                    <Clock className="h-3 w-3 text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">{update.timestamp.toLocaleTimeString()}</span>
                    <Badge variant="outline" className="text-xs">
                      {update.type}
                    </Badge>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Live Activity Indicator */}
        <div className="flex items-center justify-center pt-4 border-t border-border">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span>Monitoring your progress in real-time</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
