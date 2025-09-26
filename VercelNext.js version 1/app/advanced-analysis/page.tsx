import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"
import { Brain, Target, TrendingUp, Lightbulb, Layers, ShieldCheck } from "lucide-react"

export default function AdvancedAnalysisPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation - Reusing existing navigation pattern */}
      <nav className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary">SkillGap AI</h1>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <Link href="/" className="text-muted-foreground hover:text-foreground transition-colors">
                Home
              </Link>
              <Link href="/advanced-analysis" className="text-primary hover:text-foreground transition-colors">
                Advanced Analysis
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" asChild>
                <Link href="/auth/login">Sign in</Link>
              </Button>
              <Button asChild>
                <Link href="/auth/signup">Get started</Link>
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section for Advanced Analysis */}
      <section className="relative py-20 lg:py-32 text-center">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <Badge variant="secondary" className="mb-6 bg-primary/10 text-primary border-primary/20">
            Phase 2: Advanced Intelligence
          </Badge>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-balance mb-6">
            Unlock Deeper{" "}
            <span className="bg-gradient-to-r from-primary via-chart-1 to-primary bg-clip-text text-transparent">
              Career Insights
            </span>{" "}
            with AI
          </h1>
          <p className="text-xl text-muted-foreground text-balance mb-8 max-w-2xl mx-auto leading-relaxed">
            Our advanced engine goes beyond basic matching, providing intelligent gap analysis, enhanced proficiency
            scoring, and transparent AI explanations.
          </p>
          <Button size="lg" asChild className="text-lg px-8">
            <Link href="/auth/signup">
              Explore Features <Lightbulb className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>
      </section>

      {/* Intelligent Gap Analysis Engine */}
      <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Intelligent Gap Analysis Engine</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Our AI distinguishes between missing skills and proficiency gaps, offering priority-based scoring and
              detailed improvement suggestions.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <Brain className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Skill vs. Proficiency Gaps</h3>
                <p className="text-muted-foreground">
                  Precisely identify if a skill is entirely missing or if there's a need for deeper proficiency.
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <Target className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Priority-Based Scoring</h3>
                <p className="text-muted-foreground">
                  Gaps are scored (Critical/High/Medium/Low) based on job role relevance and impact.
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <TrendingUp className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Detailed Improvement Suggestions</h3>
                <p className="text-muted-foreground">
                  Receive actionable advice and resources tailored to close each identified gap.
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <Layers className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Skill Clustering & Recommendations</h3>
                <p className="text-muted-foreground">
                  Discover related skills and comprehensive learning paths to maximize your development.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Enhanced Proficiency Scoring */}
      <section className="py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Enhanced Proficiency Scoring</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Our AI analyzes years of experience, project complexity, leadership roles, and technology recency to
              provide a holistic view of your expertise.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <h3 className="text-xl font-semibold mb-2">Experience Detection</h3>
                <p className="text-muted-foreground">Accurately identifies years of experience for each skill.</p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <h3 className="text-xl font-semibold mb-2">Project Complexity</h3>
                <p className="text-muted-foreground">Evaluates the complexity of projects you've worked on.</p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <h3 className="text-xl font-semibold mb-2">Leadership Roles</h3>
                <p className="text-muted-foreground">
                  Recognizes and scores leadership contributions in your experience.
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <h3 className="text-xl font-semibold mb-2">Technology Recency</h3>
                <p className="text-muted-foreground">
                  Awareness of technology versions and how recently they were used.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Explainable AI Features */}
      <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Explainable AI Features</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Understand exactly how our AI arrives at its conclusions with transparent evidence snippets and confidence
              scores.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-8">
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <ShieldCheck className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Evidence Snippets</h3>
                <p className="text-muted-foreground">
                  See the exact text from your resume that supports each extracted skill and proficiency level.
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <Lightbulb className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Interactive Skill Highlighting</h3>
                <p className="text-muted-foreground">
                  Visually identify where skills are mentioned in your resume for quick verification.
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <h3 className="text-xl font-semibold mb-2">Confidence Score Explanations</h3>
                <p className="text-muted-foreground">
                  Understand the AI's confidence in its assessments and why certain scores were given.
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <h3 className="text-xl font-semibold mb-2">Model Uncertainty Quantification</h3>
                <p className="text-muted-foreground">
                  Insights into areas where the model has higher uncertainty, guiding further review.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer - Reusing existing footer pattern */}
      <footer className="border-t border-border py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold text-primary mb-4">SkillGap AI</h3>
            <p className="text-muted-foreground mb-4">AI-powered career development platform</p>
            <div className="flex justify-center space-x-6 text-sm text-muted-foreground">
              <Link href="#" className="hover:text-foreground transition-colors">
                Privacy Policy
              </Link>
              <Link href="#" className="hover:text-foreground transition-colors">
                Terms of Service
              </Link>
              <Link href="#" className="hover:text-foreground transition-colors">
                Contact
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
