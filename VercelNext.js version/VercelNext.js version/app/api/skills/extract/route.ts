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
    const { resumeFilePath, jobDescription } = await request.json()

    if (!resumeFilePath || !jobDescription) {
      return NextResponse.json({ error: "Resume file path and job description are required" }, { status: 400 })
    }

    // In a real application, you would call an external AI service or a local model here
    // For now, we'll simulate some extracted skills based on the job description
    const mockSkills = [
      "React",
      "Next.js",
      "TypeScript",
      "Tailwind CSS",
      "Node.js",
      "Express.js",
      "MongoDB",
      "RESTful APIs",
      "Git",
      "Agile Methodologies",
      "Problem Solving",
      "Communication",
    ].filter((skill) => jobDescription.toLowerCase().includes(skill.toLowerCase().split(" ")[0]))

    // Store extracted skills in Supabase (e.g., in a 'extracted_skills' table)
    const { data, error } = await supabase
      .from("extracted_skills")
      .insert({
        resume_file_path: resumeFilePath,
        job_description: jobDescription,
        skills: mockSkills,
        created_at: new Date().toISOString(),
      })
      .select()

    if (error) {
      console.error("[v0] Supabase insert error (extracted_skills):", error)
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    return NextResponse.json({ extractedSkills: mockSkills, analysisId: data[0].id }, { status: 200 })
  } catch (error: any) {
    console.error("[v0] Error extracting skills:", error)
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}
