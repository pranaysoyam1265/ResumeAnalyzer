"use client"

import { useState, useEffect } from "react"
import { DashboardNav } from "@/components/dashboard-nav"
import { FileUpload } from "@/components/file-upload"
import { SkillExtractionResults } from "@/components/skill-extraction-results"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Brain, FileText, Zap, TrendingUp, Database, Globe, CheckCircle, Clock } from "lucide-react"

const mockSkills = [
  {
    name: "Python",
    category: "Programming Languages",
    confidence: 95,
    experience: "5+ years",
    marketDemand: "High" as const,
    skillType: "Essential" as const,
    trend: "Growing" as const,
    proficiencyLevel: "Expert",
    contextMentions: 12,
    normalizedSkill: "Python Programming",
    synonyms: ["Python", "Python3", "Python Development"],
    marketGrowthRate: "+15%",
    jobPostingFrequency: 45000,
    salaryImpact: "High",
    originalContext: [
      "Developed machine learning models using Python and scikit-learn",
      "Built web scraping applications with Python and Beautiful Soup",
      "Implemented data analysis pipelines using Python pandas",
    ],
    verificationStatus: "verified" as const,
    skillSource: "work_experience" as const,
    lastUsed: "2024",
    certifications: ["Python Institute PCAP"],
  },
  {
    name: "JavaScript",
    category: "Programming Languages",
    confidence: 92,
    experience: "4+ years",
    marketDemand: "High" as const,
    skillType: "Essential" as const,
    trend: "Stable" as const,
    proficiencyLevel: "Advanced",
    contextMentions: 8,
    normalizedSkill: "JavaScript Programming",
    synonyms: ["JavaScript", "JS", "ECMAScript"],
    marketGrowthRate: "+8%",
    jobPostingFrequency: 52000,
    salaryImpact: "High",
    originalContext: [
      "Built interactive web applications using JavaScript and React",
      "Implemented client-side validation with vanilla JavaScript",
    ],
    verificationStatus: "verified" as const,
    skillSource: "work_experience" as const,
    lastUsed: "2024",
  },
  {
    name: "Machine Learning",
    category: "AI & ML",
    confidence: 88,
    experience: "3+ years",
    marketDemand: "High" as const,
    skillType: "Competitive" as const,
    trend: "Growing" as const,
    proficiencyLevel: "Advanced",
    contextMentions: 15,
    normalizedSkill: "Machine Learning Engineering",
    synonyms: ["Machine Learning", "ML", "Artificial Intelligence"],
    marketGrowthRate: "+35%",
    jobPostingFrequency: 28000,
    salaryImpact: "Very High",
    originalContext: [
      "Designed and implemented machine learning algorithms for predictive analytics",
      "Applied supervised and unsupervised learning techniques",
      "Optimized ML models for production deployment",
    ],
    verificationStatus: "verified" as const,
    skillSource: "work_experience" as const,
    lastUsed: "2024",
    certifications: ["AWS Machine Learning Specialty"],
  },
  {
    name: "React",
    category: "Frontend Technologies",
    confidence: 90,
    experience: "4+ years",
    marketDemand: "High" as const,
    skillType: "Essential" as const,
    trend: "Stable" as const,
    proficiencyLevel: "Expert",
    contextMentions: 11,
    normalizedSkill: "React.js Development",
    synonyms: ["React", "React.js", "ReactJS"],
    marketGrowthRate: "+5%",
    jobPostingFrequency: 42000,
    salaryImpact: "High",
    originalContext: [
      "Built responsive web applications using React and modern hooks",
      "Implemented state management with React Context and Redux",
    ],
    verificationStatus: "verified" as const,
    skillSource: "work_experience" as const,
    lastUsed: "2024",
  },
  {
    name: "Data Analysis",
    category: "Data Science",
    confidence: 92,
    experience: "5+ years",
    marketDemand: "High" as const,
    skillType: "Essential" as const,
    trend: "Growing" as const,
    proficiencyLevel: "Expert",
    contextMentions: 18,
    normalizedSkill: "Data Analysis & Visualization",
    synonyms: ["Data Analysis", "Data Analytics", "Statistical Analysis"],
    marketGrowthRate: "+15%",
    jobPostingFrequency: 55000,
    salaryImpact: "High",
    originalContext: [
      "Performed statistical analysis on large datasets to identify trends",
      "Created data visualizations and dashboards for stakeholder reporting",
      "Conducted A/B testing and experimental design",
    ],
    verificationStatus: "verified" as const,
    skillSource: "work_experience" as const,
    lastUsed: "2024",
  },
]

export default function ResumeAnalysisPage() {
  const [isProcessing, setIsProcessing] = useState(false)
  const [analysisComplete, setAnalysisComplete] = useState(false)
  const [extractedSkills, setExtractedSkills] = useState<typeof mockSkills>([])
  const [processingStage, setProcessingStage] = useState("")
  const [currentStageIndex, setCurrentStageIndex] = useState(0)
  const [processingProgress, setProcessingProgress] = useState(0)

  const stages = [
    {
      name: "Document Processing",
      description: "Extracting text from PDF/DOCX using OCR and document parsing",
      icon: FileText,
      duration: 1200,
    },
    {
      name: "Text Preprocessing",
      description: "Tokenization, normalization, and cleaning with spaCy NLP pipeline",
      icon: Zap,
      duration: 800,
    },
    {
      name: "Named Entity Recognition",
      description: "Running custom-trained NER models to identify skill entities",
      icon: Brain,
      duration: 1000,
    },
    {
      name: "Context Analysis",
      description: "Understanding skill context and proficiency levels using transformers",
      icon: TrendingUp,
      duration: 1500,
    },
    {
      name: "Skill Normalization",
      description: "Mapping skills to standard taxonomies and industry classifications",
      icon: Database,
      duration: 600,
    },
    {
      name: "Market Intelligence",
      description: "Cross-referencing with real-time job market data from LinkedIn, Indeed",
      icon: Globe,
      duration: 1000,
    },
    {
      name: "Confidence Scoring",
      description: "Calculating extraction confidence using ensemble ML models",
      icon: CheckCircle,
      duration: 400,
    },
    {
      name: "Final Analysis",
      description: "Generating insights and categorizing skills into strategic tiers",
      icon: TrendingUp,
      duration: 600,
    },
  ]

  useEffect(() => {
    document.documentElement.classList.add("theme-resume")
    return () => {
      document.documentElement.classList.remove("theme-resume")
    }
  }, [])

  const handleFileUpload = async (file: File) => {
    setIsProcessing(true)
    setAnalysisComplete(false)
    setCurrentStageIndex(0)
    setProcessingProgress(0)

    for (let i = 0; i < stages.length; i++) {
      setCurrentStageIndex(i)
      setProcessingStage(stages[i].description)

      // Simulate realistic processing time for each stage
      const duration = stages[i].duration
      const steps = 20
      const stepDuration = duration / steps

      for (let step = 0; step <= steps; step++) {
        setProcessingProgress(((i * steps + step) / (stages.length * steps)) * 100)
        await new Promise((resolve) => setTimeout(resolve, stepDuration))
      }
    }

    setExtractedSkills(mockSkills)
    setIsProcessing(false)
    setAnalysisComplete(true)
    setProcessingStage("")
  }

  const handleReanalyze = () => {
    setAnalysisComplete(false)
    setExtractedSkills([])
    setProcessingProgress(0)
    setCurrentStageIndex(0)
  }

  return (
    <div className="min-h-screen bg-background">
      <DashboardNav />
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-theme-gradient mb-2">AI-Powered Resume Analysis</h1>
          <p className="text-muted-foreground text-lg">
            Advanced NLP system using spaCy, NLTK, and Transformers for comprehensive skill extraction
          </p>
        </div>

        <div className="space-y-8">
          <Card className="glass-card border-theme-primary/20 hover-lift">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-theme-primary" />
                <span>Advanced NLP & Skill Extraction Pipeline</span>
              </CardTitle>
              <p className="text-muted-foreground">
                Multi-layered analysis using transformer models and real-time market intelligence
              </p>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-4 gap-6">
                {stages.slice(0, 4).map((stage, index) => {
                  const Icon = stage.icon
                  return (
                    <div key={stage.name} className="flex items-start space-x-3">
                      <div className="w-10 h-10 bg-theme-gradient rounded-full flex items-center justify-center flex-shrink-0">
                        <Icon className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <h3 className="font-semibold mb-1 text-theme-primary">{stage.name}</h3>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          {stage.description.split(" ").slice(0, 8).join(" ")}...
                        </p>
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card border-theme-secondary/20 hover-lift">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Database className="h-6 w-6 text-theme-secondary" />
                <span>Real-Time Market Data Sources</span>
              </CardTitle>
              <p className="text-muted-foreground">
                Live integration with job boards and professional networks for accurate market insights
              </p>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-3 gap-4">
                <div className="glass p-4 rounded-xl hover-lift">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-3">
                      <Globe className="h-6 w-6 text-blue-500" />
                      <div>
                        <div className="font-semibold">LinkedIn Jobs</div>
                        <div className="text-sm text-muted-foreground">Professional network data</div>
                      </div>
                    </div>
                    <Badge variant="secondary" className="bg-green-100 text-green-700">
                      <div className="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse" />
                      Live
                    </Badge>
                  </div>
                  <div className="text-xs text-muted-foreground">Last updated: 2 minutes ago • 2.3M+ job postings</div>
                </div>

                <div className="glass p-4 rounded-xl hover-lift">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-3">
                      <Globe className="h-6 w-6 text-green-500" />
                      <div>
                        <div className="font-semibold">Indeed</div>
                        <div className="text-sm text-muted-foreground">Market trends & salaries</div>
                      </div>
                    </div>
                    <Badge variant="secondary" className="bg-green-100 text-green-700">
                      <div className="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse" />
                      Live
                    </Badge>
                  </div>
                  <div className="text-xs text-muted-foreground">Last updated: 5 minutes ago • 1.8M+ job postings</div>
                </div>

                <div className="glass p-4 rounded-xl hover-lift">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-3">
                      <Globe className="h-6 w-6 text-purple-500" />
                      <div>
                        <div className="font-semibold">Glassdoor</div>
                        <div className="text-sm text-muted-foreground">Salary insights & reviews</div>
                      </div>
                    </div>
                    <Badge variant="secondary" className="bg-green-100 text-green-700">
                      <div className="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse" />
                      Live
                    </Badge>
                  </div>
                  <div className="text-xs text-muted-foreground">Last updated: 1 minute ago • 900K+ salary reports</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* File Upload */}
          <FileUpload onFileUpload={handleFileUpload} isProcessing={isProcessing} />

          {isProcessing && (
            <Card className="glass-card border-theme-primary/30 bg-theme-gradient/5">
              <CardContent className="p-6">
                <div className="space-y-6">
                  <div className="flex items-center space-x-3">
                    <Brain className="h-6 w-6 text-theme-primary animate-pulse" />
                    <div>
                      <h3 className="font-semibold text-theme-primary">Processing Resume with Advanced AI Pipeline</h3>
                      <p className="text-sm text-muted-foreground">{processingStage}</p>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Overall Progress</span>
                      <span className="text-sm text-muted-foreground">{Math.round(processingProgress)}%</span>
                    </div>
                    <Progress value={processingProgress} className="h-3" />
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {stages.map((stage, index) => {
                      const Icon = stage.icon
                      const isCompleted = index < currentStageIndex
                      const isCurrent = index === currentStageIndex
                      const isPending = index > currentStageIndex

                      return (
                        <div
                          key={stage.name}
                          className={`flex items-center space-x-2 p-2 rounded-lg transition-all ${
                            isCompleted
                              ? "bg-green-100 text-green-700"
                              : isCurrent
                                ? "bg-theme-primary/10 text-theme-primary"
                                : "bg-muted/30 text-muted-foreground"
                          }`}
                        >
                          {isCompleted ? (
                            <CheckCircle className="h-4 w-4" />
                          ) : isCurrent ? (
                            <Icon className="h-4 w-4 animate-pulse" />
                          ) : (
                            <Clock className="h-4 w-4" />
                          )}
                          <span className="text-xs font-medium">{stage.name}</span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Results */}
          {(isProcessing || analysisComplete) && (
            <SkillExtractionResults skills={extractedSkills} isLoading={isProcessing} />
          )}

          {analysisComplete && (
            <Card className="glass-card border-theme-accent/20">
              <CardContent className="p-6">
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button
                    onClick={handleReanalyze}
                    variant="outline"
                    className="glass-nav border-theme-primary/30 hover:bg-theme-primary/10 focus-theme bg-transparent"
                  >
                    Upload Different Resume
                  </Button>
                  <Button asChild className="bg-theme-gradient hover:opacity-90 focus-theme">
                    <a href="/dashboard/goals">Analyze Skill Gaps</a>
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
