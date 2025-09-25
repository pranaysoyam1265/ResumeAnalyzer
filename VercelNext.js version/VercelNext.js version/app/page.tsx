import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"
import { ArrowRight, Brain, Target, TrendingUp, Users, Zap, CheckCircle, Lightbulb, FileText } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary">SkillGap AI</h1>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <Link href="#features" className="text-muted-foreground hover:text-foreground transition-colors">
                Features
              </Link>
              <Link href="#how-it-works" className="text-muted-foreground hover:text-foreground transition-colors">
                How it works
              </Link>
              <Link href="/advanced-analysis" className="text-muted-foreground hover:text-foreground transition-colors">
                Advanced Analysis
              </Link>
              <Link href="/analysis-wizard" className="text-muted-foreground hover:text-foreground transition-colors">
                Start Analysis
              </Link>
              <Link href="#pricing" className="text-muted-foreground hover:text-foreground transition-colors">
                Pricing
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

      {/* Hero Section */}
      <section className="relative py-20 lg:py-32">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-4xl mx-auto">
            <Badge variant="secondary" className="mb-6 bg-primary/10 text-primary border-primary/20">
              AI-Powered Career Development
            </Badge>
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-balance mb-6">
              Bridge your{" "}
              <span className="bg-gradient-to-r from-primary via-chart-1 to-primary bg-clip-text text-transparent">
                skill gaps
              </span>{" "}
              with AI precision
            </h1>
            <p className="text-xl text-muted-foreground text-balance mb-8 max-w-2xl mx-auto leading-relaxed">
              Upload your resume, set career goals, and get personalized course recommendations powered by advanced NLP
              and knowledge graphs. Transform your career trajectory with data-driven insights.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild className="text-lg px-8">
                <Link href="/auth/signup">
                  Start your journey <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" className="text-lg px-8 bg-transparent" asChild>
                <Link href="/analysis-wizard">
                  Start Analysis <Zap className="ml-2 h-5 w-5" />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-muted/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Powered by cutting-edge AI</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Our platform combines custom NER models, knowledge graphs, and semantic analysis to deliver precise career
              insights
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <Brain className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Smart Resume Analysis</h3>
                <p className="text-muted-foreground">
                  Advanced NLP extracts skills, experience, and qualifications from your resume with 95% accuracy
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <Target className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Precision Gap Analysis</h3>
                <p className="text-muted-foreground">
                  Compare your skills against job requirements using semantic similarity and knowledge graphs
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <TrendingUp className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Personalized Recommendations</h3>
                <p className="text-muted-foreground">
                  Get curated course suggestions that directly address your skill gaps and career goals
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <Lightbulb className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Advanced Gap Analysis</h3>
                <p className="text-muted-foreground">
                  Distinguish missing skills from proficiency gaps with priority-based scoring and detailed rationale.
                </p>
                <Link href="/advanced-analysis" className="text-primary hover:underline mt-4 block">
                  Learn more <ArrowRight className="ml-1 inline-block h-4 w-4" />
                </Link>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <Zap className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Real-time Insights</h3>
                <p className="text-muted-foreground">
                  Track your progress and get updated recommendations as you complete courses and gain new skills
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <Users className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Industry Standards</h3>
                <p className="text-muted-foreground">
                  Built on O*NET and ESCO taxonomies, ensuring alignment with industry skill requirements
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <CheckCircle className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Proven Results</h3>
                <p className="text-muted-foreground">
                  15% improvement in recommendation accuracy compared to traditional keyword-based systems
                </p>
              </CardContent>
            </Card>
            <Card className="border-border bg-card/50 backdrop-blur">
              <CardContent className="p-6">
                <FileText className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">Multi-Step Analysis Wizard</h3>
                <p className="text-muted-foreground">
                  Guided process to upload resume, enter job description, validate skills, and view analysis.
                </p>
                <Link href="/analysis-wizard" className="text-primary hover:underline mt-4 block">
                  Start Wizard <ArrowRight className="ml-1 inline-block h-4 w-4" />
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section id="how-it-works" className="py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">How it works</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Three simple steps to unlock your career potential with AI-powered insights
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Upload Resume</h3>
              <p className="text-muted-foreground">
                Upload your resume and our AI extracts your skills, experience, and qualifications automatically
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Set Goals</h3>
              <p className="text-muted-foreground">
                Define your target job roles and career objectives to get personalized analysis
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Get Recommendations</h3>
              <p className="text-muted-foreground">
                Receive curated course recommendations that bridge your skill gaps and advance your career
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary/5">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to accelerate your career?</h2>
            <p className="text-xl text-muted-foreground mb-8">
              Join thousands of professionals who are already using AI to identify and bridge their skill gaps
            </p>
            <Button size="lg" asChild className="text-lg px-8">
              <Link href="/auth/signup">
                Get started for free <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
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
