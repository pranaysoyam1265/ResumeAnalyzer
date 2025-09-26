import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"
import {
  Brain,
  Target,
  TrendingUp,
  BookOpen,
  Lightbulb,
  LayoutDashboard,
  FileText,
  Goal,
  Award,
  User,
} from "lucide-react"
import { Progress } from "@/components/ui/progress"

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground">
      <header className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center gap-2">
          <Lightbulb className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold">SkillGap AI</span>
        </div>
        <nav className="hidden md:flex items-center space-x-6">
          <Link href="#" className="flex items-center gap-2 text-sm font-medium hover:text-primary transition-colors">
            <LayoutDashboard className="h-4 w-4" />
            Dashboard
          </Link>
          <Link
            href="/analysis-wizard"
            className="flex items-center gap-2 text-sm font-medium hover:text-primary transition-colors"
          >
            <FileText className="h-4 w-4" />
            Resume Analysis
          </Link>
          <Link href="#" className="flex items-center gap-2 text-sm font-medium hover:text-primary transition-colors">
            <Goal className="h-4 w-4" />
            Skill Goals
          </Link>
          <Link href="#" className="flex items-center gap-2 text-sm font-medium hover:text-primary transition-colors">
            <Award className="h-4 w-4" />
            Recommendations
          </Link>
          <Link href="#" className="flex items-center gap-2 text-sm font-medium hover:text-primary transition-colors">
            <TrendingUp className="h-4 w-4" />
            Progress
          </Link>
        </nav>
        <div className="flex items-center gap-4">
          <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-semibold">
            <User className="h-5 w-5" />
          </div>
        </div>
      </header>

      <main className="flex-1 p-8">
        <section className="mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-2">Welcome back, Pranay Soyam!</h1>
          <p className="text-lg text-muted-foreground">
            Your AI-powered career development dashboard with real-time market insights
          </p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <Card className="bg-card text-card-foreground shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Skills Identified</CardTitle>
              <Brain className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-foreground">24</div>
              <p className="text-xs text-green-500">+3 this week</p>
              <p className="text-sm text-muted-foreground mt-4">From AI-powered resume analysis</p>
              <Progress value={85} className="h-2 mt-2" />
              <p className="text-xs text-muted-foreground mt-1">Progress 85%</p>
            </CardContent>
          </Card>

          <Card className="bg-card text-card-foreground shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Skill Gaps</CardTitle>
              <Target className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-foreground">7</div>
              <p className="text-xs text-red-500">-2 closed</p>
              <p className="text-sm text-muted-foreground mt-4">High-priority areas for growth</p>
              <Progress value={65} className="h-2 mt-2" />
              <p className="text-xs text-muted-foreground mt-1">Progress 65%</p>
            </CardContent>
          </Card>

          <Card className="bg-card text-card-foreground shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Learning Progress</CardTitle>
              <TrendingUp className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-foreground">68%</div>
              <p className="text-xs text-green-500">+12% this month</p>
              <p className="text-sm text-muted-foreground mt-4">Towards career objectives</p>
              <Progress value={68} className="h-2 mt-2" />
              <p className="text-xs text-muted-foreground mt-1">Progress 68%</p>
            </CardContent>
          </Card>

          <Card className="bg-card text-card-foreground shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Course Recommendations</CardTitle>
              <BookOpen className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-foreground">12</div>
              <p className="text-xs text-blue-500">4 new matches</p>
              <p className="text-sm text-muted-foreground mt-4">AI-curated for your goals</p>
              <Progress value={90} className="h-2 mt-2" />
              <p className="text-xs text-muted-foreground mt-1">Progress 90%</p>
            </CardContent>
          </Card>
        </section>
      </main>

      <footer className="border-t border-border py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold text-foreground mb-4">SkillGap AI</h3>
            <p className="text-muted-foreground mb-4">Your AI-powered career development platform</p>
            <div className="flex justify-center space-x-6 text-sm text-muted-foreground">
              <Link href="#" className="hover:text-primary transition-colors">
                Privacy Policy
              </Link>
              <Link href="#" className="hover:text-primary transition-colors">
                Terms of Service
              </Link>
              <Link href="#" className="hover:text-primary transition-colors">
                Contact
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
