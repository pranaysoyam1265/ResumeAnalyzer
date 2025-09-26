"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Activity, Clock, Target, Bell, CheckCircle, TrendingUp } from "lucide-react"

interface RealTimeTrackerProps {
  sessionData: any
  notifications: any[]
  onNotificationRead: (id: string) => void
}

export function RealTimeTracker({ sessionData, notifications, onNotificationRead }: RealTimeTrackerProps) {
  const [currentGoal, setCurrentGoal] = useState({
    type: "daily",
    target: 120, // minutes
    current: 135, // minutes
    description: "Daily learning goal",
  })

  const [liveMetrics, setLiveMetrics] = useState({
    focusScore: 85,
    learningVelocity: 12.5,
    retentionRate: 78,
    engagementLevel: "High",
  })

  useEffect(() => {
    const interval = setInterval(() => {
      setLiveMetrics((prev) => ({
        ...prev,
        focusScore: Math.max(70, Math.min(100, prev.focusScore + (Math.random() - 0.5) * 5)),
        learningVelocity: Math.max(8, Math.min(20, prev.learningVelocity + (Math.random() - 0.5) * 2)),
        retentionRate: Math.max(60, Math.min(95, prev.retentionRate + (Math.random() - 0.5) * 3)),
      }))
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-6">
      {/* Live Session Dashboard */}
      <Card className="glass-card border-theme-primary/20 hover-lift">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="h-6 w-6 text-theme-primary animate-pulse" />
            <span>Live Learning Session</span>
            <Badge className="bg-green-100 text-green-700 border-green-200">Active</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Current Goal Progress */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Target className="h-4 w-4 text-theme-secondary" />
                <span className="font-medium">{currentGoal.description}</span>
              </div>
              <div className="text-sm text-muted-foreground">
                {currentGoal.current}m / {currentGoal.target}m
              </div>
            </div>
            <Progress value={(currentGoal.current / currentGoal.target) * 100} className="h-3" />
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span>Goal exceeded by {currentGoal.current - currentGoal.target} minutes!</span>
              <CheckCircle className="h-4 w-4 text-green-500" />
            </div>
          </div>

          {/* Live Metrics Grid */}
          <div className="grid md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-theme-primary/5 rounded-lg">
              <div className="text-2xl font-bold text-theme-primary">{liveMetrics.focusScore}%</div>
              <div className="text-xs text-muted-foreground">Focus Score</div>
              <div className="text-xs text-green-600 flex items-center justify-center mt-1">
                <TrendingUp className="h-3 w-3 mr-1" />
                +2.5%
              </div>
            </div>
            <div className="text-center p-3 bg-theme-secondary/5 rounded-lg">
              <div className="text-2xl font-bold text-theme-secondary">{liveMetrics.learningVelocity}</div>
              <div className="text-xs text-muted-foreground">Learning Velocity</div>
              <div className="text-xs text-blue-600">concepts/hour</div>
            </div>
            <div className="text-center p-3 bg-purple-500/5 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{liveMetrics.retentionRate}%</div>
              <div className="text-xs text-muted-foreground">Retention Rate</div>
              <div className="text-xs text-green-600 flex items-center justify-center mt-1">
                <TrendingUp className="h-3 w-3 mr-1" />
                +1.2%
              </div>
            </div>
            <div className="text-center p-3 bg-orange-500/5 rounded-lg">
              <div className="text-lg font-bold text-orange-600">{liveMetrics.engagementLevel}</div>
              <div className="text-xs text-muted-foreground">Engagement</div>
              <div className="text-xs text-orange-600">Real-time</div>
            </div>
          </div>

          {/* Session Controls */}
          <div className="flex items-center justify-between pt-4 border-t border-border">
            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">Session started 2h 15m ago</span>
            </div>
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm">
                Take Break
              </Button>
              <Button size="sm" className="bg-theme-gradient hover:opacity-90">
                End Session
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Real-Time Notifications */}
      <Card className="glass-card border-theme-accent/20 hover-lift">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Bell className="h-5 w-5 text-theme-accent" />
            <span>Live Notifications</span>
            {notifications.filter((n) => !n.read).length > 0 && (
              <Badge className="bg-red-100 text-red-700 border-red-200">
                {notifications.filter((n) => !n.read).length} new
              </Badge>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {notifications.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <Bell className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No new notifications</p>
            </div>
          ) : (
            notifications.map((notification) => (
              <div
                key={notification.id}
                className={`flex items-start space-x-3 p-3 rounded-lg transition-all hover-lift ${
                  notification.read ? "bg-muted/30" : "bg-theme-primary/5 border border-theme-primary/20"
                }`}
              >
                <div
                  className={`w-2 h-2 rounded-full mt-2 ${
                    notification.type === "milestone"
                      ? "bg-green-500"
                      : notification.type === "streak"
                        ? "bg-orange-500"
                        : "bg-blue-500"
                  }`}
                />
                <div className="flex-1">
                  <p className={`text-sm ${notification.read ? "text-muted-foreground" : "font-medium"}`}>
                    {notification.message}
                  </p>
                  <p className="text-xs text-muted-foreground">{notification.timestamp.toLocaleTimeString()}</p>
                </div>
                {!notification.read && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => onNotificationRead(notification.id)}
                    className="text-xs"
                  >
                    Mark Read
                  </Button>
                )}
              </div>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  )
}
