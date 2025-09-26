"use client"

import { useState } from "react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { X, Plus, CheckCircle2, AlertCircle } from "lucide-react"

interface SkillValidationProps {
  skills: string[]
  onSkillsChange: (skills: string[]) => void
}

export function SkillValidation({ skills: initialSkills, onSkillsChange }: SkillValidationProps) {
  const [skills, setSkills] = useState(initialSkills)
  const [newSkill, setNewSkill] = useState("")
  const [editingSkill, setEditingSkill] = useState<string | null>(null)
  const [editedSkillValue, setEditedSkillValue] = useState("")

  const updateSkills = (newSkills: string[]) => {
    setSkills(newSkills)
    onSkillsChange(newSkills)
  }

  const handleAddSkill = () => {
    if (newSkill.trim() !== "" && !skills.includes(newSkill.trim())) {
      updateSkills([...skills, newSkill.trim()])
      setNewSkill("")
    }
  }

  const handleRemoveSkill = (skillToRemove: string) => {
    updateSkills(skills.filter((skill) => skill !== skillToRemove))
  }

  const handleEditSkill = (skill: string) => {
    setEditingSkill(skill)
    setEditedSkillValue(skill)
  }

  const handleSaveEditedSkill = (originalSkill: string) => {
    if (editedSkillValue.trim() !== "" && editedSkillValue.trim() !== originalSkill) {
      updateSkills(skills.map((skill) => (skill === originalSkill ? editedSkillValue.trim() : skill)))
    }
    setEditingSkill(null)
    setEditedSkillValue("")
  }

  const handleCancelEdit = () => {
    setEditingSkill(null)
    setEditedSkillValue("")
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-semibold mb-4">Extracted Skills</h3>
        <div className="flex flex-wrap gap-3">
          {skills.length > 0 ? (
            skills.map((skill) => (
              <div key={skill} className="flex items-center gap-2">
                {editingSkill === skill ? (
                  <div className="flex items-center gap-2">
                    <Input
                      value={editedSkillValue}
                      onChange={(e) => setEditedSkillValue(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") handleSaveEditedSkill(skill)
                        if (e.key === "Escape") handleCancelEdit()
                      }}
                      className="h-8"
                    />
                    <Button variant="ghost" size="icon" onClick={() => handleSaveEditedSkill(skill)}>
                      <CheckCircle2 className="h-4 w-4 text-primary" />
                    </Button>
                    <Button variant="ghost" size="icon" onClick={handleCancelEdit}>
                      <X className="h-4 w-4 text-muted-foreground" />
                    </Button>
                  </div>
                ) : (
                  <Badge
                    variant="secondary"
                    className="px-3 py-1 text-base cursor-pointer hover:bg-secondary/80 transition-colors"
                    onClick={() => handleEditSkill(skill)}
                  >
                    {skill}
                    <X
                      className="ml-2 h-4 w-4 cursor-pointer text-muted-foreground hover:text-foreground"
                      onClick={(e) => {
                        e.stopPropagation() // Prevent triggering edit when removing
                        handleRemoveSkill(skill)
                      }}
                    />
                  </Badge>
                )}
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No skills extracted yet. Add some below!</p>
          )}
        </div>
      </div>

      <div className="flex gap-2">
        <Input
          placeholder="Add a new skill"
          value={newSkill}
          onChange={(e) => setNewSkill(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAddSkill()}
          className="flex-1"
        />
        <Button onClick={handleAddSkill} disabled={newSkill.trim() === ""}>
          <Plus className="h-4 w-4 mr-2" /> Add Skill
        </Button>
      </div>

      <div className="border-t border-border pt-6 mt-6 space-y-4">
        <h3 className="text-xl font-semibold">Interactive Highlighting & Confidence Scores</h3>
        <div className="bg-muted/30 p-4 rounded-md text-muted-foreground italic">
          <p>{"// ... Resume text will be displayed here with interactive highlighting ..."}</p>
          <p className="mt-2">
            {'// Example: "Proficient in '}
            <span className="font-bold text-primary">React</span>
            {' (Confidence: 98%)"'}
          </p>
          <p>
            {'// Example: "Developed applications using '}
            <span className="font-bold text-primary">Next.js</span>
            {' (Confidence: 95%)"'}
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <AlertCircle className="h-4 w-4" />
          {
            "Click on extracted skills above to edit them. This section will show where skills were found in your resume."
          }
        </div>
      </div>
    </div>
  )
}
