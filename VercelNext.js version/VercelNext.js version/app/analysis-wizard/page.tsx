"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { CheckCircle2, UploadCloud, FileText, Lightbulb, BarChart, Loader2 } from "lucide-react"
import { SkillValidation } from "@/components/skill-validation"
import useSWRMutation from "swr/mutation"

const fetcher = (url: string) => fetch(url).then((res) => res.json())
const postFetcher = async (url: string, { arg }: { arg: any }) => {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(arg),
  })
  if (!res.ok) {
    const error = new Error("An error occurred while fetching the data.") as any
    error.info = await res.json()
    error.status = res.status
    throw error
  }
  return res.json()
}

export default function AnalysisWizardPage() {
  const [step, setStep] = useState(1)
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState("")
  const [extractedSkills, setExtractedSkills] = useState<string[]>([])
  const [validatedSkills, setValidatedSkills] = useState<string[]>([])
  const [resumeFilePath, setResumeFilePath] = useState<string | null>(null)
  const [analysisId, setAnalysisId] = useState<string | null>(null)
  const [analysisReport, setAnalysisReport] = useState<any>(null)

  const { trigger: uploadResumeTrigger, isMutating: isUploadingResume } = useSWRMutation(
    "/api/resume/upload",
    async (url, { arg }: { arg: FormData }) => {
      const res = await fetch(url, {
        method: "POST",
        body: arg,
      })
      if (!res.ok) {
        const error = new Error("An error occurred while uploading the resume.") as any
        error.info = await res.json()
        error.status = res.status
        throw error
      }
      return res.json()
    },
  )

  const { trigger: extractSkillsTrigger, isMutating: isExtractingSkills } = useSWRMutation(
    "/api/skills/extract",
    postFetcher,
  )

  const { trigger: generateAnalysisTrigger, isMutating: isGeneratingAnalysis } = useSWRMutation(
    "/api/analysis/generate",
    postFetcher,
  )

  const handleNext = () => {
    setStep(step + 1)
  }

  const handleBack = () => {
    setStep(step - 1)
  }

  const handleResumeUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setResumeFile(event.target.files[0])
    }
  }

  const handleJobDescriptionChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setJobDescription(event.target.value)
  }

  const uploadResume = async () => {
    if (!resumeFile) return

    const formData = new FormData()
    formData.append("resume", resumeFile)

    try {
      const data = await uploadResumeTrigger(formData)
      setResumeFilePath(data.filePath)
      handleNext()
    } catch (error) {
      console.error("[v0] Failed to upload resume:", error)
      // TODO: Display error message to user
    }
  }

  const performSkillExtraction = async () => {
    if (!resumeFilePath || !jobDescription) return

    try {
      const data = await extractSkillsTrigger({ resumeFilePath, jobDescription })
      setExtractedSkills(data.extractedSkills)
      setValidatedSkills(data.extractedSkills) // Initialize validated skills with extracted skills
      setAnalysisId(data.analysisId)
      handleNext()
    } catch (error) {
      console.error("[v0] Failed to extract skills:", error)
      // TODO: Display error message to user
    }
  }

  const generateAnalysis = async () => {
    if (!analysisId || !validatedSkills) return

    try {
      const data = await generateAnalysisTrigger({ analysisId, validatedSkills })
      setAnalysisReport(data.analysisReport)
      handleNext()
    } catch (error) {
      console.error("[v0] Failed to generate analysis:", error)
      // TODO: Display error message to user
    }
  }

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <Card className="w-full max-w-2xl mx-auto glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <UploadCloud className="h-6 w-6" /> {"1. Upload Your Resume"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid w-full items-center gap-4">
                <Label htmlFor="resume" className="text-lg">
                  Upload your resume (PDF, DOCX)
                </Label>
                <Input
                  id="resume"
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleResumeUpload}
                  className="file:text-primary file:font-semibold file:bg-primary/10 file:border-primary/20 file:rounded-md file:px-4 file:py-2 file:mr-4 hover:file:bg-primary/20"
                />
                {resumeFile && (
                  <p className="text-sm text-muted-foreground mt-2">
                    File selected: <span className="font-medium text-foreground">{resumeFile.name}</span>
                  </p>
                )}
              </div>
              <div className="flex justify-end mt-6">
                <Button onClick={uploadResume} disabled={!resumeFile || isUploadingResume}>
                  {isUploadingResume && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                  Next
                </Button>
              </div>
            </CardContent>
          </Card>
        )
      case 2:
        return (
          <Card className="w-full max-w-2xl mx-auto glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-6 w-6" /> {"2. Enter Job Description"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid w-full items-center gap-4">
                <Label htmlFor="job-description" className="text-lg">
                  Paste the job description
                </Label>
                <Textarea
                  id="job-description"
                  placeholder="Paste the job description here..."
                  value={jobDescription}
                  onChange={handleJobDescriptionChange}
                  rows={10}
                  className="min-h-[150px]"
                />
              </div>
              <div className="flex justify-between mt-6">
                <Button variant="outline" onClick={handleBack}>
                  Back
                </Button>
                <Button onClick={performSkillExtraction} disabled={!jobDescription || isExtractingSkills}>
                  {isExtractingSkills && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                  Extract Skills
                </Button>
              </div>
            </CardContent>
          </Card>
        )
      case 3:
        return (
          <Card className="w-full max-w-4xl mx-auto glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Lightbulb className="h-6 w-6" /> {"3. Validate Skills"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <SkillValidation skills={extractedSkills} onSkillsChange={setValidatedSkills} />
              <div className="flex justify-between mt-6">
                <Button variant="outline" onClick={handleBack}>
                  Back
                </Button>
                <Button onClick={generateAnalysis} disabled={isGeneratingAnalysis}>
                  {isGeneratingAnalysis && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                  View Analysis
                </Button>
              </div>
            </CardContent>
          </Card>
        )
      case 4:
        return (
          <Card className="w-full max-w-4xl mx-auto glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart className="h-6 w-6" /> {"4. View Analysis"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {analysisReport ? (
                <div className="py-10">
                  <CheckCircle2 className="h-16 w-16 text-primary mx-auto mb-4" />
                  <h3 className="text-2xl font-semibold mb-2">Analysis Complete!</h3>
                  <p className="text-muted-foreground mb-6">
                    Your personalized skill gap analysis and recommendations are ready.
                  </p>
                  <div className="space-y-4 text-left">
                    <h4 className="text-xl font-semibold">Summary:</h4>
                    <p>{analysisReport.summary}</p>

                    <h4 className="text-xl font-semibold mt-6">Skill Gap Analysis:</h4>
                    <ul className="list-disc list-inside space-y-2">
                      {analysisReport.gapAnalysis.map((item: any, index: number) => (
                        <li key={index}>
                          <span className="font-medium">{item.skill}:</span> {item.status} (Score: {item.score}%)
                          {item.recommendation && (
                            <p className="text-sm text-muted-foreground ml-4">{item.recommendation}</p>
                          )}
                        </li>
                      ))}
                    </ul>

                    <h4 className="text-xl font-semibold mt-6">Recommendations:</h4>
                    <ul className="list-disc list-inside space-y-2">
                      {analysisReport.recommendations.map((rec: string, index: number) => (
                        <li key={index}>{rec}</li>
                      ))}
                    </ul>

                    {analysisReport.xaiFeatures && (
                      <>
                        <h4 className="text-xl font-semibold mt-6">Explainable AI Features:</h4>
                        <p>{analysisReport.xaiFeatures.evidenceSnippets}</p>
                        <p>{analysisReport.xaiFeatures.confidenceScores}</p>
                      </>
                    )}
                  </div>
                  <Button className="mt-6">Download Report</Button>
                </div>
              ) : (
                <div className="text-center py-10">
                  <Loader2 className="h-16 w-16 text-primary mx-auto mb-4 animate-spin" />
                  <h3 className="text-2xl font-semibold mb-2">Generating Analysis...</h3>
                  <p className="text-muted-foreground">Please wait while we process your data.</p>
                </div>
              )}
              <div className="flex justify-start mt-6">
                <Button variant="outline" onClick={handleBack}>
                  Back
                </Button>
              </div>
            </CardContent>
          </Card>
        )
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-background py-12 px-4 sm:px-6 lg:px-8 flex flex-col items-center">
      <h1 className="text-4xl md:text-5xl font-bold text-center text-balance mb-12">AI-Powered Skill Gap Analysis</h1>
      <div className="w-full max-w-5xl">
        <div className="flex justify-center gap-4 mb-12">
          <div className={`flex flex-col items-center ${step >= 1 ? "text-primary" : "text-muted-foreground"}`}>
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center border-2 ${step >= 1 ? "border-primary bg-primary/10" : "border-muted-foreground bg-muted/10"}`}
            >
              <span className="font-bold">{step > 1 ? <CheckCircle2 className="h-5 w-5" /> : "1"}</span>
            </div>
            <p className="text-sm mt-2">Upload Resume</p>
          </div>
          <div className="flex-1 border-t-2 border-dashed border-muted-foreground mt-5 mx-2" />
          <div className={`flex flex-col items-center ${step >= 2 ? "text-primary" : "text-muted-foreground"}`}>
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center border-2 ${step >= 2 ? "border-primary bg-primary/10" : "border-muted-foreground bg-muted/10"}`}
            >
              <span className="font-bold">{step > 2 ? <CheckCircle2 className="h-5 w-5" /> : "2"}</span>
            </div>
            <p className="text-sm mt-2">Job Description</p>
          </div>
          <div className="flex-1 border-t-2 border-dashed border-muted-foreground mt-5 mx-2" />
          <div className={`flex flex-col items-center ${step >= 3 ? "text-primary" : "text-muted-foreground"}`}>
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center border-2 ${step >= 3 ? "border-primary bg-primary/10" : "border-muted-foreground bg-muted/10"}`}
            >
              <span className="font-bold">{step > 3 ? <CheckCircle2 className="h-5 w-5" /> : "3"}</span>
            </div>
            <p className="text-sm mt-2">Validate Skills</p>
          </div>
          <div className="flex-1 border-t-2 border-dashed border-muted-foreground mt-5 mx-2" />
          <div className={`flex flex-col items-center ${step >= 4 ? "text-primary" : "text-muted-foreground"}`}>
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center border-2 ${step >= 4 ? "border-primary bg-primary/10" : "border-muted-foreground bg-muted/10"}`}
            >
              <span className="font-bold">4</span>
            </div>
            <p className="text-sm mt-2">View Analysis</p>
          </div>
        </div>
        {renderStep()}
      </div>
    </div>
  )
}
