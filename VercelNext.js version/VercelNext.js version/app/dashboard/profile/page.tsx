"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { createBrowserClient } from "@supabase/ssr"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import {
  User,
  Bell,
  Shield,
  Briefcase,
  Upload,
  Save,
  Edit3,
  MapPin,
  Globe,
  Github,
  Linkedin,
  Twitter,
} from "lucide-react"
import { toast } from "@/hooks/use-toast"

interface UserProfile {
  id: string
  full_name: string
  email: string
  bio: string
  location: string
  website: string
  github_url: string
  linkedin_url: string
  twitter_url: string
  avatar_url: string
  phone: string
  job_title: string
  company: string
  experience_level: string
  career_goals: string[]
  skills: string[]
  interests: string[]
  timezone: string
  preferred_language: string
  created_at: string
  updated_at: string
}

interface NotificationSettings {
  email_notifications: boolean
  push_notifications: boolean
  course_reminders: boolean
  progress_updates: boolean
  skill_recommendations: boolean
  market_insights: boolean
  weekly_digest: boolean
}

interface PrivacySettings {
  profile_visibility: "public" | "private" | "connections"
  show_progress: boolean
  show_skills: boolean
  show_achievements: boolean
  allow_contact: boolean
}

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null)
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [notifications, setNotifications] = useState<NotificationSettings>({
    email_notifications: true,
    push_notifications: false,
    course_reminders: true,
    progress_updates: true,
    skill_recommendations: true,
    market_insights: false,
    weekly_digest: true,
  })
  const [privacy, setPrivacy] = useState<PrivacySettings>({
    profile_visibility: "public",
    show_progress: true,
    show_skills: true,
    show_achievements: true,
    allow_contact: true,
  })
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)

  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  )

  useEffect(() => {
    fetchUserProfile()
  }, [])

  const fetchUserProfile = async () => {
    try {
      const {
        data: { user },
      } = await supabase.auth.getUser()
      if (user) {
        setUser(user)
        // Initialize profile with user data
        setProfile({
          id: user.id,
          full_name: user.user_metadata?.full_name || "",
          email: user.email || "",
          bio: "",
          location: "",
          website: "",
          github_url: "",
          linkedin_url: "",
          twitter_url: "",
          avatar_url: user.user_metadata?.avatar_url || "",
          phone: "",
          job_title: "",
          company: "",
          experience_level: "intermediate",
          career_goals: [],
          skills: [],
          interests: [],
          timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
          preferred_language: "en",
          created_at: user.created_at,
          updated_at: new Date().toISOString(),
        })
      }
    } catch (error) {
      console.error("Error fetching profile:", error)
      toast({
        title: "Error",
        description: "Failed to load profile data",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleSaveProfile = async () => {
    if (!profile) return

    setIsSaving(true)
    try {
      // In a real app, you would save to Supabase
      await new Promise((resolve) => setTimeout(resolve, 1000)) // Simulate API call

      toast({
        title: "Profile Updated",
        description: "Your profile has been successfully updated.",
      })
      setIsEditing(false)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update profile",
        variant: "destructive",
      })
    } finally {
      setIsSaving(false)
    }
  }

  const handleAvatarUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    // In a real app, you would upload to Supabase Storage
    const reader = new FileReader()
    reader.onload = (e) => {
      if (profile) {
        setProfile({
          ...profile,
          avatar_url: e.target?.result as string,
        })
      }
    }
    reader.readAsDataURL(file)
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
        <div className="container mx-auto px-4 py-8">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-slate-200 dark:bg-slate-800 rounded w-1/4"></div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="h-96 bg-slate-200 dark:bg-slate-800 rounded-lg"></div>
              <div className="lg:col-span-2 h-96 bg-slate-200 dark:bg-slate-800 rounded-lg"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!profile) return null

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Profile Settings</h1>
            <p className="text-slate-600 dark:text-slate-400 mt-2">Manage your account and preferences</p>
          </div>
          <Button
            onClick={() => (isEditing ? handleSaveProfile() : setIsEditing(true))}
            disabled={isSaving}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
          >
            {isSaving ? (
              <>
                <Save className="w-4 h-4 mr-2 animate-spin" />
                Saving...
              </>
            ) : isEditing ? (
              <>
                <Save className="w-4 h-4 mr-2" />
                Save Changes
              </>
            ) : (
              <>
                <Edit3 className="w-4 h-4 mr-2" />
                Edit Profile
              </>
            )}
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Profile Overview Card */}
          <Card className="lg:col-span-1 backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
            <CardHeader className="text-center">
              <div className="relative mx-auto mb-4">
                <Avatar className="w-24 h-24 mx-auto border-4 border-white dark:border-slate-800 shadow-lg">
                  <AvatarImage src={profile.avatar_url || "/placeholder.svg"} alt={profile.full_name} />
                  <AvatarFallback className="text-2xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white">
                    {profile.full_name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")
                      .toUpperCase() || "U"}
                  </AvatarFallback>
                </Avatar>
                {isEditing && (
                  <label className="absolute bottom-0 right-0 bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full cursor-pointer shadow-lg transition-colors">
                    <Upload className="w-4 h-4" />
                    <input type="file" accept="image/*" onChange={handleAvatarUpload} className="hidden" />
                  </label>
                )}
              </div>
              <CardTitle className="text-xl">{profile.full_name || "Your Name"}</CardTitle>
              <CardDescription className="text-sm">
                {profile.job_title && profile.company ? `${profile.job_title} at ${profile.company}` : profile.email}
              </CardDescription>
              {profile.location && (
                <div className="flex items-center justify-center text-sm text-slate-600 dark:text-slate-400 mt-2">
                  <MapPin className="w-4 h-4 mr-1" />
                  {profile.location}
                </div>
              )}
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <Label className="text-sm font-medium text-slate-700 dark:text-slate-300">Experience Level</Label>
                  <Badge variant="secondary" className="mt-1 capitalize">
                    {profile.experience_level}
                  </Badge>
                </div>
                <div>
                  <Label className="text-sm font-medium text-slate-700 dark:text-slate-300">Member Since</Label>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                    {new Date(profile.created_at).toLocaleDateString("en-US", {
                      year: "numeric",
                      month: "long",
                    })}
                  </p>
                </div>
                {profile.skills.length > 0 && (
                  <div>
                    <Label className="text-sm font-medium text-slate-700 dark:text-slate-300">Top Skills</Label>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {profile.skills.slice(0, 3).map((skill, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Main Content */}
          <div className="lg:col-span-2">
            <Tabs defaultValue="personal" className="space-y-6">
              <TabsList className="grid w-full grid-cols-4 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
                <TabsTrigger value="personal" className="flex items-center gap-2">
                  <User className="w-4 h-4" />
                  Personal
                </TabsTrigger>
                <TabsTrigger value="career" className="flex items-center gap-2">
                  <Briefcase className="w-4 h-4" />
                  Career
                </TabsTrigger>
                <TabsTrigger value="notifications" className="flex items-center gap-2">
                  <Bell className="w-4 h-4" />
                  Notifications
                </TabsTrigger>
                <TabsTrigger value="privacy" className="flex items-center gap-2">
                  <Shield className="w-4 h-4" />
                  Privacy
                </TabsTrigger>
              </TabsList>

              {/* Personal Information Tab */}
              <TabsContent value="personal">
                <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                  <CardHeader>
                    <CardTitle>Personal Information</CardTitle>
                    <CardDescription>Update your personal details and contact information</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="fullName">Full Name</Label>
                        <Input
                          id="fullName"
                          value={profile.full_name}
                          onChange={(e) => setProfile({ ...profile, full_name: e.target.value })}
                          disabled={!isEditing}
                          className="mt-1"
                        />
                      </div>
                      <div>
                        <Label htmlFor="email">Email</Label>
                        <Input
                          id="email"
                          type="email"
                          value={profile.email}
                          disabled
                          className="mt-1 bg-slate-50 dark:bg-slate-800"
                        />
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="bio">Bio</Label>
                      <Textarea
                        id="bio"
                        value={profile.bio}
                        onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                        disabled={!isEditing}
                        placeholder="Tell us about yourself..."
                        className="mt-1 min-h-[100px]"
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="location">Location</Label>
                        <Input
                          id="location"
                          value={profile.location}
                          onChange={(e) => setProfile({ ...profile, location: e.target.value })}
                          disabled={!isEditing}
                          placeholder="City, Country"
                          className="mt-1"
                        />
                      </div>
                      <div>
                        <Label htmlFor="phone">Phone</Label>
                        <Input
                          id="phone"
                          value={profile.phone}
                          onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                          disabled={!isEditing}
                          placeholder="+1 (555) 123-4567"
                          className="mt-1"
                        />
                      </div>
                    </div>

                    <Separator />

                    <div>
                      <Label className="text-base font-medium">Social Links</Label>
                      <div className="space-y-4 mt-4">
                        <div className="flex items-center space-x-3">
                          <Globe className="w-5 h-5 text-slate-500" />
                          <Input
                            value={profile.website}
                            onChange={(e) => setProfile({ ...profile, website: e.target.value })}
                            disabled={!isEditing}
                            placeholder="https://yourwebsite.com"
                            className="flex-1"
                          />
                        </div>
                        <div className="flex items-center space-x-3">
                          <Github className="w-5 h-5 text-slate-500" />
                          <Input
                            value={profile.github_url}
                            onChange={(e) => setProfile({ ...profile, github_url: e.target.value })}
                            disabled={!isEditing}
                            placeholder="https://github.com/username"
                            className="flex-1"
                          />
                        </div>
                        <div className="flex items-center space-x-3">
                          <Linkedin className="w-5 h-5 text-slate-500" />
                          <Input
                            value={profile.linkedin_url}
                            onChange={(e) => setProfile({ ...profile, linkedin_url: e.target.value })}
                            disabled={!isEditing}
                            placeholder="https://linkedin.com/in/username"
                            className="flex-1"
                          />
                        </div>
                        <div className="flex items-center space-x-3">
                          <Twitter className="w-5 h-5 text-slate-500" />
                          <Input
                            value={profile.twitter_url}
                            onChange={(e) => setProfile({ ...profile, twitter_url: e.target.value })}
                            disabled={!isEditing}
                            placeholder="https://twitter.com/username"
                            className="flex-1"
                          />
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Career Information Tab */}
              <TabsContent value="career">
                <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                  <CardHeader>
                    <CardTitle>Career Information</CardTitle>
                    <CardDescription>Manage your professional details and career goals</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="jobTitle">Job Title</Label>
                        <Input
                          id="jobTitle"
                          value={profile.job_title}
                          onChange={(e) => setProfile({ ...profile, job_title: e.target.value })}
                          disabled={!isEditing}
                          placeholder="Software Engineer"
                          className="mt-1"
                        />
                      </div>
                      <div>
                        <Label htmlFor="company">Company</Label>
                        <Input
                          id="company"
                          value={profile.company}
                          onChange={(e) => setProfile({ ...profile, company: e.target.value })}
                          disabled={!isEditing}
                          placeholder="Tech Corp"
                          className="mt-1"
                        />
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="experienceLevel">Experience Level</Label>
                      <Select
                        value={profile.experience_level}
                        onValueChange={(value) => setProfile({ ...profile, experience_level: value })}
                        disabled={!isEditing}
                      >
                        <SelectTrigger className="mt-1">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="entry">Entry Level (0-2 years)</SelectItem>
                          <SelectItem value="intermediate">Intermediate (2-5 years)</SelectItem>
                          <SelectItem value="senior">Senior (5-10 years)</SelectItem>
                          <SelectItem value="expert">Expert (10+ years)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="careerGoals">Career Goals</Label>
                      <Textarea
                        id="careerGoals"
                        value={profile.career_goals.join("\n")}
                        onChange={(e) =>
                          setProfile({ ...profile, career_goals: e.target.value.split("\n").filter((g) => g.trim()) })
                        }
                        disabled={!isEditing}
                        placeholder="Enter your career goals (one per line)..."
                        className="mt-1 min-h-[100px]"
                      />
                    </div>

                    <div>
                      <Label>Current Skills</Label>
                      <div className="flex flex-wrap gap-2 mt-2 p-3 border rounded-lg bg-slate-50 dark:bg-slate-800/50 min-h-[60px]">
                        {profile.skills.length > 0 ? (
                          profile.skills.map((skill, index) => (
                            <Badge key={index} variant="secondary" className="text-sm">
                              {skill}
                            </Badge>
                          ))
                        ) : (
                          <p className="text-sm text-slate-500 dark:text-slate-400">
                            Upload a resume to automatically extract your skills
                          </p>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Notifications Tab */}
              <TabsContent value="notifications">
                <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                  <CardHeader>
                    <CardTitle>Notification Preferences</CardTitle>
                    <CardDescription>Choose how you want to be notified about updates</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Email Notifications</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">Receive notifications via email</p>
                        </div>
                        <Switch
                          checked={notifications.email_notifications}
                          onCheckedChange={(checked) =>
                            setNotifications({ ...notifications, email_notifications: checked })
                          }
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Push Notifications</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            Receive push notifications in your browser
                          </p>
                        </div>
                        <Switch
                          checked={notifications.push_notifications}
                          onCheckedChange={(checked) =>
                            setNotifications({ ...notifications, push_notifications: checked })
                          }
                        />
                      </div>

                      <Separator />

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Course Reminders</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            Reminders about your enrolled courses
                          </p>
                        </div>
                        <Switch
                          checked={notifications.course_reminders}
                          onCheckedChange={(checked) =>
                            setNotifications({ ...notifications, course_reminders: checked })
                          }
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Progress Updates</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            Updates about your learning progress
                          </p>
                        </div>
                        <Switch
                          checked={notifications.progress_updates}
                          onCheckedChange={(checked) =>
                            setNotifications({ ...notifications, progress_updates: checked })
                          }
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Skill Recommendations</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            New course recommendations based on your skills
                          </p>
                        </div>
                        <Switch
                          checked={notifications.skill_recommendations}
                          onCheckedChange={(checked) =>
                            setNotifications({ ...notifications, skill_recommendations: checked })
                          }
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Market Insights</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            Industry trends and market updates
                          </p>
                        </div>
                        <Switch
                          checked={notifications.market_insights}
                          onCheckedChange={(checked) =>
                            setNotifications({ ...notifications, market_insights: checked })
                          }
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Weekly Digest</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            Weekly summary of your activity and recommendations
                          </p>
                        </div>
                        <Switch
                          checked={notifications.weekly_digest}
                          onCheckedChange={(checked) => setNotifications({ ...notifications, weekly_digest: checked })}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Privacy Tab */}
              <TabsContent value="privacy">
                <Card className="backdrop-blur-sm bg-white/70 dark:bg-slate-900/70 border-white/20 dark:border-slate-800/20">
                  <CardHeader>
                    <CardTitle>Privacy Settings</CardTitle>
                    <CardDescription>Control who can see your information and activity</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div>
                      <Label htmlFor="profileVisibility">Profile Visibility</Label>
                      <Select
                        value={privacy.profile_visibility}
                        onValueChange={(value: "public" | "private" | "connections") =>
                          setPrivacy({ ...privacy, profile_visibility: value })
                        }
                      >
                        <SelectTrigger className="mt-1">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="public">Public - Anyone can view</SelectItem>
                          <SelectItem value="connections">Connections Only</SelectItem>
                          <SelectItem value="private">Private - Only you</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <Separator />

                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Show Progress</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            Display your learning progress publicly
                          </p>
                        </div>
                        <Switch
                          checked={privacy.show_progress}
                          onCheckedChange={(checked) => setPrivacy({ ...privacy, show_progress: checked })}
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Show Skills</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            Display your skills on your profile
                          </p>
                        </div>
                        <Switch
                          checked={privacy.show_skills}
                          onCheckedChange={(checked) => setPrivacy({ ...privacy, show_skills: checked })}
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Show Achievements</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            Display your achievements and certificates
                          </p>
                        </div>
                        <Switch
                          checked={privacy.show_achievements}
                          onCheckedChange={(checked) => setPrivacy({ ...privacy, show_achievements: checked })}
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-base">Allow Contact</Label>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            Allow others to contact you through the platform
                          </p>
                        </div>
                        <Switch
                          checked={privacy.allow_contact}
                          onCheckedChange={(checked) => setPrivacy({ ...privacy, allow_contact: checked })}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  )
}
