"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CheckCircle, Circle, User, Briefcase, Target, Settings } from "lucide-react"
import Link from "next/link"

interface ProfileCompletionItem {
  id: string
  title: string
  description: string
  completed: boolean
  icon: React.ReactNode
  href: string
}

export function ProfileCompletionWidget() {
  const [completionItems, setCompletionItems] = useState<ProfileCompletionItem[]>([
    {
      id: "basic-info",
      title: "Basic Information",
      description: "Add your name, bio, and contact details",
      completed: false,
      icon: <User className="w-4 h-4" />,
      href: "/dashboard/profile?tab=personal",
    },
    {
      id: "career-info",
      title: "Career Details",
      description: "Add your job title, company, and experience level",
      completed: false,
      icon: <Briefcase className="w-4 h-4" />,
      href: "/dashboard/profile?tab=career",
    },
    {
      id: "skills-upload",
      title: "Upload Resume",
      description: "Upload your resume to extract skills automatically",
      completed: false,
      icon: <Target className="w-4 h-4" />,
      href: "/dashboard/resume",
    },
    {
      id: "preferences",
      title: "Set Preferences",
      description: "Configure notifications and privacy settings",
      completed: false,
      icon: <Settings className="w-4 h-4" />,
      href: "/dashboard/profile?tab=notifications",
    },
  ])

  const completedCount = completionItems.filter((item) => item.completed).length
  const completionPercentage = (completedCount / completionItems.length) * 100

  return (
    <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Profile Completion</CardTitle>
          <Badge variant={completionPercentage === 100 ? "default" : "secondary"} className="text-xs">
            {Math.round(completionPercentage)}%
          </Badge>
        </div>
        <Progress value={completionPercentage} className="mt-2" />
      </CardHeader>
      <CardContent className="space-y-3">
        {completionItems.map((item) => (
          <div
            key={item.id}
            className="flex items-center justify-between p-3 rounded-lg bg-slate-50/50 dark:bg-slate-800/50"
          >
            <div className="flex items-center space-x-3">
              {item.completed ? (
                <CheckCircle className="w-5 h-5 text-green-600" />
              ) : (
                <Circle className="w-5 h-5 text-slate-400" />
              )}
              <div className="flex items-center space-x-2">
                {item.icon}
                <div>
                  <p className="text-sm font-medium text-slate-900 dark:text-slate-100">{item.title}</p>
                  <p className="text-xs text-slate-600 dark:text-slate-400">{item.description}</p>
                </div>
              </div>
            </div>
            {!item.completed && (
              <Button asChild size="sm" variant="ghost" className="text-xs">
                <Link href={item.href}>Complete</Link>
              </Button>
            )}
          </div>
        ))}

        {completionPercentage === 100 && (
          <div className="text-center p-4 bg-green-50 dark:bg-green-950/20 rounded-lg border border-green-200 dark:border-green-800">
            <CheckCircle className="w-8 h-8 text-green-600 mx-auto mb-2" />
            <p className="text-sm font-medium text-green-800 dark:text-green-200">Profile Complete!</p>
            <p className="text-xs text-green-600 dark:text-green-400 mt-1">
              You're all set to get personalized recommendations
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
