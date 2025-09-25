import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import {
  TrendingUp,
  TrendingDown,
  Minus,
  Star,
  AlertTriangle,
  CheckCircle,
  FileText,
  Award,
  Calendar,
} from "lucide-react"

interface Skill {
  name: string
  category: string
  confidence: number
  experience?: string
  marketDemand: "High" | "Medium" | "Low"
  skillType: "Essential" | "Competitive"
  trend: "Growing" | "Stable" | "Declining"
  proficiencyLevel?: string
  contextMentions?: number
  normalizedSkill?: string
  synonyms?: string[]
  marketGrowthRate?: string
  jobPostingFrequency?: number
  salaryImpact?: string
  originalContext?: string[]
  verificationStatus?: "verified" | "inferred" | "uncertain"
  skillSource?: "work_experience" | "education" | "projects" | "certifications"
  lastUsed?: string
  certifications?: string[]
}

interface SkillExtractionResultsProps {
  skills: Skill[]
  isLoading?: boolean
}

const skillCategories = [
  { name: "Programming Languages", color: "bg-blue-500", icon: "💻" },
  { name: "AI & ML", color: "bg-purple-500", icon: "🤖" },
  { name: "Frontend Technologies", color: "bg-green-500", icon: "🎨" },
  { name: "Backend Technologies", color: "bg-orange-500", icon: "⚙️" },
  { name: "Data Science", color: "bg-pink-500", icon: "📊" },
  { name: "Cloud & DevOps", color: "bg-cyan-500", icon: "☁️" },
  { name: "Databases", color: "bg-red-500", icon: "🗄️" },
  { name: "Mobile Development", color: "bg-indigo-500", icon: "📱" },
  { name: "Soft Skills", color: "bg-gray-500", icon: "🤝" },
]

export function SkillExtractionResults({ skills, isLoading = false }: SkillExtractionResultsProps) {
  if (isLoading) {
    return (
      <Card className="glass-card border-theme-primary/20">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <div className="w-6 h-6 bg-theme-primary/20 rounded animate-pulse" />
            <span>Processing with Advanced NLP Pipeline...</span>
          </CardTitle>
          <p className="text-muted-foreground">Extracting skills with context understanding and market intelligence</p>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="space-y-3 fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
                <div className="flex items-center space-x-3">
                  <div className="h-4 w-24 bg-muted rounded animate-pulse" />
                  <div className="h-4 w-16 bg-muted/70 rounded animate-pulse" />
                  <div className="h-4 w-20 bg-muted/50 rounded animate-pulse" />
                </div>
                <div className="h-2 bg-muted/30 rounded animate-pulse" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  const groupedSkills = skills.reduce(
    (acc, skill) => {
      if (!acc[skill.category]) {
        acc[skill.category] = []
      }
      acc[skill.category].push(skill)
      return acc
    },
    {} as Record<string, Skill[]>,
  )

  const essentialSkills = skills.filter((s) => s.skillType === "Essential")
  const competitiveSkills = skills.filter((s) => s.skillType === "Competitive")
  const highDemandSkills = skills.filter((s) => s.marketDemand === "High")
  const growingSkills = skills.filter((s) => s.trend === "Growing")
  const verifiedSkills = skills.filter((s) => s.verificationStatus === "verified")

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "Growing":
        return <TrendingUp className="h-3 w-3 text-green-500" />
      case "Declining":
        return <TrendingDown className="h-3 w-3 text-red-500" />
      default:
        return <Minus className="h-3 w-3 text-gray-500" />
    }
  }

  const getDemandColor = (demand: string) => {
    switch (demand) {
      case "High":
        return "text-green-700 bg-green-100 border-green-200"
      case "Medium":
        return "text-yellow-700 bg-yellow-100 border-yellow-200"
      case "Low":
        return "text-red-700 bg-red-100 border-red-200"
      default:
        return "text-gray-700 bg-gray-100 border-gray-200"
    }
  }

  const getVerificationIcon = (status?: string) => {
    switch (status) {
      case "verified":
        return <CheckCircle className="h-3 w-3 text-green-500" />
      case "inferred":
        return <AlertTriangle className="h-3 w-3 text-yellow-500" />
      default:
        return <AlertTriangle className="h-3 w-3 text-gray-400" />
    }
  }

  return (
    <div className="space-y-6">
      <Card className="glass-card border-theme-primary/20 hover-lift">
        <CardHeader>
          <CardTitle className="text-theme-gradient">AI-Powered Market Analysis Summary</CardTitle>
          <p className="text-muted-foreground">
            Comprehensive skill extraction using transformer models with real-time job market intelligence
          </p>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="text-center p-4 glass rounded-xl">
              <div className="text-3xl font-bold text-theme-primary mb-1">{skills.length}</div>
              <div className="text-sm text-muted-foreground">Skills Identified</div>
            </div>
            <div className="text-center p-4 glass rounded-xl">
              <div className="text-3xl font-bold text-green-600 mb-1">{essentialSkills.length}</div>
              <div className="text-sm text-muted-foreground">Essential Skills</div>
            </div>
            <div className="text-center p-4 glass rounded-xl">
              <div className="text-3xl font-bold text-blue-600 mb-1">{competitiveSkills.length}</div>
              <div className="text-sm text-muted-foreground">Competitive Edge</div>
            </div>
            <div className="text-center p-4 glass rounded-xl">
              <div className="text-3xl font-bold text-purple-600 mb-1">{verifiedSkills.length}</div>
              <div className="text-sm text-muted-foreground">Verified Skills</div>
            </div>
            <div className="text-center p-4 glass rounded-xl">
              <div className="text-3xl font-bold text-orange-600 mb-1">{growingSkills.length}</div>
              <div className="text-sm text-muted-foreground">Growing Trends</div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="glass-card border-theme-secondary/20 hover-lift">
        <CardHeader>
          <CardTitle className="text-theme-gradient">Strategic Skill Categorization</CardTitle>
          <p className="text-muted-foreground">
            Two-tier analysis distinguishing foundational skills from competitive advantages
          </p>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center">
                  <Star className="h-5 w-5 text-yellow-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Foundational Skills</h3>
                  <p className="text-sm text-muted-foreground">Essential for job entry and basic competency</p>
                </div>
              </div>
              <div className="space-y-3">
                {essentialSkills.slice(0, 6).map((skill) => (
                  <div key={skill.name} className="glass p-4 rounded-xl hover-lift">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold">{skill.name}</span>
                        {getVerificationIcon(skill.verificationStatus)}
                      </div>
                      <div className="flex items-center space-x-2">
                        {getTrendIcon(skill.trend)}
                        <Badge className={getDemandColor(skill.marketDemand)} variant="secondary">
                          {skill.marketDemand}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>{skill.jobPostingFrequency?.toLocaleString()} job postings</span>
                      <span>{skill.marketGrowthRate} growth</span>
                    </div>
                    <Progress value={skill.confidence} className="h-2 mt-2" />
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center">
                  <AlertTriangle className="h-5 w-5 text-orange-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Competitive Skills</h3>
                  <p className="text-sm text-muted-foreground">Advanced skills that provide market advantage</p>
                </div>
              </div>
              <div className="space-y-3">
                {competitiveSkills.slice(0, 6).map((skill) => (
                  <div key={skill.name} className="glass p-4 rounded-xl hover-lift">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold">{skill.name}</span>
                        {getVerificationIcon(skill.verificationStatus)}
                      </div>
                      <div className="flex items-center space-x-2">
                        {getTrendIcon(skill.trend)}
                        <Badge className={getDemandColor(skill.marketDemand)} variant="secondary">
                          {skill.marketDemand}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>{skill.jobPostingFrequency?.toLocaleString()} job postings</span>
                      <span>{skill.marketGrowthRate} growth</span>
                    </div>
                    <Progress value={skill.confidence} className="h-2 mt-2" />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="glass-card border-theme-accent/20 hover-lift">
        <CardHeader>
          <CardTitle className="text-theme-gradient">Detailed Context Analysis</CardTitle>
          <p className="text-muted-foreground">
            Skills extracted with original context, verification status, and market positioning
          </p>
        </CardHeader>
        <CardContent className="space-y-8">
          {Object.entries(groupedSkills).map(([category, categorySkills]) => {
            const categoryInfo = skillCategories.find((c) => c.name === category) || {
              name: category,
              color: "bg-gray-500",
              icon: "🔧",
            }
            return (
              <div key={category} className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className={cn("w-4 h-4 rounded-full", categoryInfo.color)} />
                  <span className="text-2xl">{categoryInfo.icon}</span>
                  <h3 className="font-semibold text-lg">{category}</h3>
                  <Badge variant="secondary" className="text-xs">
                    {categorySkills.length} skills
                  </Badge>
                </div>

                <div className="grid gap-4">
                  {categorySkills.map((skill) => (
                    <div key={skill.name} className="glass p-5 rounded-xl hover-lift">
                      <div className="space-y-4">
                        {/* Skill Header */}
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <span className="font-semibold text-lg">{skill.name}</span>
                            {getVerificationIcon(skill.verificationStatus)}
                            {skill.experience && (
                              <Badge variant="outline" className="text-xs">
                                <Calendar className="h-3 w-3 mr-1" />
                                {skill.experience}
                              </Badge>
                            )}
                            {skill.certifications && skill.certifications.length > 0 && (
                              <Badge variant="outline" className="text-xs">
                                <Award className="h-3 w-3 mr-1" />
                                Certified
                              </Badge>
                            )}
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge
                              variant={skill.skillType === "Essential" ? "default" : "secondary"}
                              className="text-xs"
                            >
                              {skill.skillType}
                            </Badge>
                            <span className="text-sm font-medium text-theme-primary">
                              {skill.confidence}% confidence
                            </span>
                          </div>
                        </div>

                        {/* Market Metrics */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                          <div className="flex items-center space-x-2">
                            {getTrendIcon(skill.trend)}
                            <span className="text-muted-foreground">
                              {skill.trend} ({skill.marketGrowthRate})
                            </span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge className={getDemandColor(skill.marketDemand)} variant="secondary">
                              {skill.marketDemand} Demand
                            </Badge>
                          </div>
                          <div className="text-muted-foreground">
                            {skill.jobPostingFrequency?.toLocaleString()} job postings
                          </div>
                          <div className="text-muted-foreground">Salary impact: {skill.salaryImpact}</div>
                        </div>

                        {/* Original Context */}
                        {skill.originalContext && skill.originalContext.length > 0 && (
                          <div className="space-y-2">
                            <div className="flex items-center space-x-2">
                              <FileText className="h-4 w-4 text-muted-foreground" />
                              <span className="text-sm font-medium">Original Context</span>
                              <Badge variant="outline" className="text-xs">
                                {skill.contextMentions} mentions
                              </Badge>
                            </div>
                            <div className="space-y-1">
                              {skill.originalContext.slice(0, 2).map((context, index) => (
                                <div
                                  key={index}
                                  className="text-sm text-muted-foreground bg-muted/30 p-2 rounded italic"
                                >
                                  "{context}"
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Skill Normalization */}
                        <div className="flex items-center justify-between text-xs text-muted-foreground">
                          <div>Normalized: {skill.normalizedSkill}</div>
                          <div>
                            Source: {skill.skillSource?.replace("_", " ")} • Last used: {skill.lastUsed}
                          </div>
                        </div>

                        <Progress value={skill.confidence} className="h-2" />
                      </div>
                    </div>
                  ))}
                </div>

                {Object.keys(groupedSkills).indexOf(category) < Object.keys(groupedSkills).length - 1 && (
                  <Separator className="mt-8" />
                )}
              </div>
            )
          })}
        </CardContent>
      </Card>
    </div>
  )
}
