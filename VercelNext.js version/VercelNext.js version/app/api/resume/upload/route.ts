import { createServerClient } from "@supabase/ssr"
import { cookies } from "next/headers"
import { NextResponse } from "next/server"

export async function POST(request: Request) {
  const cookieStore = cookies()
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!, // Using service role key for server-side operations
    {
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
    },
  )

  try {
    const formData = await request.formData()
    const resumeFile = formData.get("resume") as File

    if (!resumeFile) {
      return NextResponse.json({ error: "No resume file provided" }, { status: 400 })
    }

    const fileExtension = resumeFile.name.split(".").pop()
    const fileName = `${Date.now()}-${Math.random().toString(36).substring(2, 15)}.${fileExtension}`
    const filePath = `resumes/${fileName}`

    const { data, error } = await supabase.storage
      .from("resumes") // Assuming a 'resumes' bucket in Supabase Storage
      .upload(filePath, resumeFile, {
        cacheControl: "3600",
        upsert: false,
      })

    if (error) {
      console.error("[v0] Supabase upload error:", error)
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    // Return the public URL or path to the uploaded file
    const { data: publicUrlData } = supabase.storage.from("resumes").getPublicUrl(filePath)

    return NextResponse.json({ filePath: data.path, publicUrl: publicUrlData.publicUrl }, { status: 200 })
  } catch (error: any) {
    console.error("[v0] Error uploading resume:", error)
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}
