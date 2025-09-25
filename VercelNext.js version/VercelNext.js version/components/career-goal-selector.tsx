"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Search, Plus, X } from "lucide-react"
import { cn } from "@/lib/utils"

const popularRoles = [
  "Senior Full Stack Developer",
  "Data Scientist",
  "DevOps Engineer",
  "Product Manager",
  "Machine Learning Engineer",
  "Frontend Developer",
  "Backend Developer",
  "Cloud Architect",
  "UI/UX Designer",
  "Software Engineering Manager",
]

interface CareerGoalSelectorProps {
  selectedGoals: string[]
  onGoalsChange: (goals: string[]) => void
}

export function CareerGoalSelector({ selectedGoals, onGoalsChange }: CareerGoalSelectorProps) {
  const [searchTerm, setSearchTerm] = useState("")
  const [customRole, setCustomRole] = useState("")

  const filteredRoles = popularRoles.filter((role) => role.toLowerCase().includes(searchTerm.toLowerCase()))

  const addGoal = (role: string) => {
    if (!selectedGoals.includes(role)) {
      onGoalsChange([...selectedGoals, role])
    }
  }

  const removeGoal = (role: string) => {
    onGoalsChange(selectedGoals.filter((goal) => goal !== role))
  }

  const addCustomRole = () => {
    if (customRole.trim() && !selectedGoals.includes(customRole.trim())) {
      onGoalsChange([...selectedGoals, customRole.trim()])
      setCustomRole("")
    }
  }

  return (
    <Card className="border-border">
      <CardHeader>
        <CardTitle>Set Your Career Goals</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Selected Goals */}
        {selectedGoals.length > 0 && (
          <div>
            <Label className="text-sm font-medium mb-2 block">Selected Goals</Label>
            <div className="flex flex-wrap gap-2">
              {selectedGoals.map((goal) => (
                <Badge key={goal} variant="default" className="flex items-center space-x-1">
                  <span>{goal}</span>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-auto p-0 ml-1 hover:bg-transparent"
                    onClick={() => removeGoal(goal)}
                  >
                    <X className="h-3 w-3" />
                  </Button>
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Search */}
        <div className="space-y-2">
          <Label htmlFor="search">Search Job Roles</Label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              id="search"
              placeholder="Search for job roles..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-input border-border"
            />
          </div>
        </div>

        {/* Popular Roles */}
        <div>
          <Label className="text-sm font-medium mb-2 block">Popular Roles</Label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {filteredRoles.map((role) => (
              <Button
                key={role}
                variant="outline"
                className={cn(
                  "justify-start h-auto p-3 text-left bg-transparent",
                  selectedGoals.includes(role) && "border-primary bg-primary/5",
                )}
                onClick={() => addGoal(role)}
                disabled={selectedGoals.includes(role)}
              >
                {role}
              </Button>
            ))}
          </div>
        </div>

        {/* Custom Role */}
        <div className="space-y-2">
          <Label htmlFor="custom">Add Custom Role</Label>
          <div className="flex space-x-2">
            <Input
              id="custom"
              placeholder="Enter a custom job role..."
              value={customRole}
              onChange={(e) => setCustomRole(e.target.value)}
              className="bg-input border-border"
              onKeyPress={(e) => e.key === "Enter" && addCustomRole()}
            />
            <Button onClick={addCustomRole} disabled={!customRole.trim()}>
              <Plus className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
