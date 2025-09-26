"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Filter, X } from "lucide-react"

interface CourseFiltersProps {
  onFiltersChange: (filters: any) => void
}

export function CourseFilters({ onFiltersChange }: CourseFiltersProps) {
  const [filters, setFilters] = useState({
    providers: [] as string[],
    levels: [] as string[],
    duration: [0, 100] as number[],
    price: [0, 500] as number[],
    priority: [] as string[],
    sortBy: "match" as string,
  })

  const providers = ["Coursera", "Udemy", "edX", "Pluralsight", "LinkedIn Learning", "Udacity"]
  const levels = ["Beginner", "Intermediate", "Advanced"]
  const priorities = ["Critical", "High", "Medium", "Low"]

  const updateFilters = (key: string, value: any) => {
    const newFilters = { ...filters, [key]: value }
    setFilters(newFilters)
    onFiltersChange(newFilters)
  }

  const toggleArrayFilter = (key: string, value: string) => {
    const currentArray = filters[key as keyof typeof filters] as string[]
    const newArray = currentArray.includes(value)
      ? currentArray.filter((item) => item !== value)
      : [...currentArray, value]
    updateFilters(key, newArray)
  }

  const clearFilters = () => {
    const clearedFilters = {
      providers: [],
      levels: [],
      duration: [0, 100],
      price: [0, 500],
      priority: [],
      sortBy: "match",
    }
    setFilters(clearedFilters)
    onFiltersChange(clearedFilters)
  }

  const hasActiveFilters =
    filters.providers.length > 0 ||
    filters.levels.length > 0 ||
    filters.priority.length > 0 ||
    filters.duration[0] > 0 ||
    filters.duration[1] < 100 ||
    filters.price[0] > 0 ||
    filters.price[1] < 500

  return (
    <Card className="border-border">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Filter className="h-5 w-5" />
            <span>Filters</span>
          </CardTitle>
          {hasActiveFilters && (
            <Button variant="ghost" size="sm" onClick={clearFilters}>
              <X className="h-4 w-4 mr-1" />
              Clear
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Sort By */}
        <div className="space-y-2">
          <Label>Sort by</Label>
          <Select value={filters.sortBy} onValueChange={(value) => updateFilters("sortBy", value)}>
            <SelectTrigger className="bg-input border-border">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="match">Best Match</SelectItem>
              <SelectItem value="rating">Highest Rated</SelectItem>
              <SelectItem value="price-low">Price: Low to High</SelectItem>
              <SelectItem value="price-high">Price: High to Low</SelectItem>
              <SelectItem value="duration">Duration</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Priority */}
        <div className="space-y-3">
          <Label>Priority</Label>
          <div className="space-y-2">
            {priorities.map((priority) => (
              <div key={priority} className="flex items-center space-x-2">
                <Checkbox
                  id={`priority-${priority}`}
                  checked={filters.priority.includes(priority)}
                  onCheckedChange={() => toggleArrayFilter("priority", priority)}
                />
                <Label htmlFor={`priority-${priority}`} className="text-sm">
                  {priority}
                </Label>
              </div>
            ))}
          </div>
        </div>

        {/* Providers */}
        <div className="space-y-3">
          <Label>Providers</Label>
          <div className="space-y-2">
            {providers.map((provider) => (
              <div key={provider} className="flex items-center space-x-2">
                <Checkbox
                  id={`provider-${provider}`}
                  checked={filters.providers.includes(provider)}
                  onCheckedChange={() => toggleArrayFilter("providers", provider)}
                />
                <Label htmlFor={`provider-${provider}`} className="text-sm">
                  {provider}
                </Label>
              </div>
            ))}
          </div>
        </div>

        {/* Levels */}
        <div className="space-y-3">
          <Label>Level</Label>
          <div className="space-y-2">
            {levels.map((level) => (
              <div key={level} className="flex items-center space-x-2">
                <Checkbox
                  id={`level-${level}`}
                  checked={filters.levels.includes(level)}
                  onCheckedChange={() => toggleArrayFilter("levels", level)}
                />
                <Label htmlFor={`level-${level}`} className="text-sm">
                  {level}
                </Label>
              </div>
            ))}
          </div>
        </div>

        {/* Duration */}
        <div className="space-y-3">
          <Label>Duration (hours)</Label>
          <div className="px-2">
            <Slider
              value={filters.duration}
              onValueChange={(value) => updateFilters("duration", value)}
              max={100}
              step={5}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-muted-foreground mt-1">
              <span>{filters.duration[0]}h</span>
              <span>{filters.duration[1]}h+</span>
            </div>
          </div>
        </div>

        {/* Price */}
        <div className="space-y-3">
          <Label>Price ($)</Label>
          <div className="px-2">
            <Slider
              value={filters.price}
              onValueChange={(value) => updateFilters("price", value)}
              max={500}
              step={10}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-muted-foreground mt-1">
              <span>${filters.price[0]}</span>
              <span>{filters.price[1] >= 500 ? "$500+" : `$${filters.price[1]}`}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
