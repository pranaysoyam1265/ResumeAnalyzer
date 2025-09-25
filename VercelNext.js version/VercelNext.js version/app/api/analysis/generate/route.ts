import { createServerClient } from "@supabase/ssr"
import { cookies } from "next/headers"
import { NextResponse } from "next/server"

export async function POST(request: Request) {
  const cookieStore = cookies()
  const supabase = createServerClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!, {
    cookies: {
      get(name: string) {
        return cookieStore.get(name)?.value
      },
      set(name: string, value: string, options: any) {
        cookieStore.set({ name, value, ...options })
      },
      remove(name: string, options: any) {
        cookieStore.set({ name, value: "", ...options })
      },
    },
  })

  try {
    const { analysisId, validatedSkills } = await request.json()

    if (!analysisId || !validatedSkills) {
      return NextResponse.json({ error: "Analysis ID and validated skills are required" }, { status: 400 })
    }

    // In a real application, you would use the validatedSkills to perform a detailed analysis
    // For now, we'll simulate a basic analysis report
    const mockAnalysisReport = {
      summary: "Based on your validated skills and the job description, here's a preliminary analysis.",
      gapAnalysis: [
        { skill: "React", status: "proficient", score: 90 },
        { skill: "Next.js", status: "proficient", score: 85 },
        {
          skill: "TypeScript",
          status: "needs improvement",
          score: 60,
          recommendation: "Focus on advanced TypeScript concepts like generics and utility types.",
        },
        { skill: "Node.js", status: "proficient", score: 75 },
        {
          skill: "Express.js",
          status: "needs improvement",
          score: 50,
          recommendation: "Gain more experience with Express.js middleware and routing.",
        },
        {
          skill: "MongoDB",
          status: "gap",
          score: 30,
          recommendation: "Learn MongoDB CRUD operations and schema design.",
        },
      ],
      recommendations: [
        "Consider taking an online course on advanced TypeScript.",
        "Build a small project using Express.js and MongoDB to solidify your backend skills.",
        "Practice coding challenges related to data structures and algorithms.",
      ],
      xaiFeatures: {
        evidenceSnippets: "Snippets from your resume and job description highlighting skill matches.",
        confidenceScores: "Confidence scores for each skill extraction.",
      },
    }

    // Update the 'extracted_skills' table with the final analysis report
    const { data, error } = await supabase
      .from("extracted_skills")
      .update({
        validated_skills: validatedSkills,
        analysis_report: mockAnalysisReport,
        updated_at: new Date().toISOString(),
      })
      .eq("id", analysisId)
      .select()

    if (error) {
      console.error("[v0] Supabase update error (analysis_report):", error)
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    return NextResponse.json({ analysisReport: mockAnalysisReport }, { status: 200 })
  } catch (error: any) {
    console.error("[v0] Error generating analysis:", error)
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}
