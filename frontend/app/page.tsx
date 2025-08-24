import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  FileText, 
  Search, 
  Brain, 
  Zap, 
  Shield, 
  Users, 
  ArrowRight,
  CheckCircle,
  Star
} from 'lucide-react';

'use client';

import { useSession } from 'next-auth/react';
import { useEffect } from 'react';

export default function HomePage() {
  const { data: session, status } = useSession();
  
  // Analytics tracking
  useEffect(() => {
    // TODO: Implement analytics tracking for page views and user interactions
    // This would typically integrate with Google Analytics, Mixpanel, etc.
    console.log('Page view: Home');
  }, []);
  // Loading state
  if (status === 'loading') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-300">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <FileText className="h-8 w-8 text-primary-600" />
            <span className="text-xl font-bold text-gray-900 dark:text-white">
              DocIntel
            </span>
          </div>
          <div className="flex items-center space-x-4">
            {session ? (
              <>
                <Link href="/dashboard">
                  <Button variant="ghost">Dashboard</Button>
                </Link>
                <Link href="/profile">
                  <Button>Profile</Button>
                </Link>
              </>
            ) : (
              <>
                <Link href="/login">
                  <Button variant="ghost">Sign In</Button>
                </Link>
                <Link href="/register">
                  <Button>Get Started</Button>
                </Link>
              </>
            )}
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            Transform Documents into
            <span className="text-primary-600 block">Actionable Intelligence</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
            AI-powered document processing that extracts insights, automates workflows, 
            and builds intelligent knowledge bases for smarter decision-making.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="text-lg px-8 py-3">
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/demo">
              <Button variant="outline" size="lg" className="text-lg px-8 py-3">
                Watch Demo
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Powerful Features for Modern Teams
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Everything you need to process, analyze, and extract value from your documents
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="hover:shadow-medium transition-shadow duration-300">
            <CardHeader>
              <div className="w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-lg flex items-center justify-center mb-4">
                <FileText className="h-6 w-6 text-primary-600" />
              </div>
              <CardTitle>Intelligent Document Processing</CardTitle>
              <CardDescription>
                AI-powered OCR and NLP extract structured data from any document type
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-medium transition-shadow duration-300">
            <CardHeader>
              <div className="w-12 h-12 bg-success-100 dark:bg-success-900 rounded-lg flex items-center justify-center mb-4">
                <Search className="h-6 w-6 text-success-600" />
              </div>
              <CardTitle>Smart Knowledge Base</CardTitle>
              <CardDescription>
                Searchable, interconnected knowledge base with natural language queries
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-medium transition-shadow duration-300">
            <CardHeader>
              <div className="w-12 h-12 bg-warning-100 dark:bg-warning-900 rounded-lg flex items-center justify-center mb-4">
                <Brain className="h-6 w-6 text-warning-600" />
              </div>
              <CardTitle>AI-Powered Insights</CardTitle>
              <CardDescription>
                Advanced analytics and pattern recognition for deeper understanding
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-medium transition-shadow duration-300">
            <CardHeader>
              <div className="w-12 h-12 bg-error-100 dark:bg-error-900 rounded-lg flex items-center justify-center mb-4">
                <Zap className="h-6 w-6 text-error-600" />
              </div>
              <CardTitle>Automated Workflows</CardTitle>
              <CardDescription>
                Streamline processes with intelligent routing and validation
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-medium transition-shadow duration-300">
            <CardHeader>
              <div className="w-12 h-12 bg-secondary-100 dark:bg-secondary-900 rounded-lg flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-secondary-600" />
              </div>
              <CardTitle>Enterprise Security</CardTitle>
              <CardDescription>
                Bank-level security with encryption, access controls, and compliance
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-medium transition-shadow duration-300">
            <CardHeader>
              <div className="w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-lg flex items-center justify-center mb-4">
                <Users className="h-6 w-6 text-primary-600" />
              </div>
              <CardTitle>Team Collaboration</CardTitle>
              <CardDescription>
                Real-time collaboration with role-based access and permissions
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">99.9%</div>
            <div className="text-gray-600 dark:text-gray-300">Uptime</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">10M+</div>
            <div className="text-gray-600 dark:text-gray-300">Documents Processed</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">500+</div>
            <div className="text-gray-600 dark:text-gray-300">Enterprise Clients</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">24/7</div>
            <div className="text-gray-600 dark:text-gray-300">Support</div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <Card className="max-w-4xl mx-auto text-center">
          <CardHeader>
            <CardTitle className="text-3xl font-bold">
              Ready to Transform Your Document Workflow?
            </CardTitle>
            <CardDescription className="text-xl">
              Join thousands of organizations already using our platform
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/register">
                <Button size="lg" className="text-lg px-8 py-3">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/contact">
                <Button variant="outline" size="lg" className="text-lg px-8 py-3">
                  Contact Sales
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-12 border-t border-gray-200 dark:border-gray-700">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <FileText className="h-6 w-6 text-primary-600" />
              <span className="text-lg font-bold">DocIntel</span>
            </div>
            <p className="text-gray-600 dark:text-gray-300">
              Transforming documents into actionable intelligence with AI-powered processing.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-4">Product</h3>
            <ul className="space-y-2 text-gray-600 dark:text-gray-300">
              <li><Link href="/features">Features</Link></li>
              <li><Link href="/pricing">Pricing</Link></li>
              <li><Link href="/integrations">Integrations</Link></li>
              <li><Link href="/api">API</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-4">Company</h3>
            <ul className="space-y-2 text-gray-600 dark:text-gray-300">
              <li><Link href="/about">About</Link></li>
              <li><Link href="/blog">Blog</Link></li>
              <li><Link href="/careers">Careers</Link></li>
              <li><Link href="/contact">Contact</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-4">Support</h3>
            <ul className="space-y-2 text-gray-600 dark:text-gray-300">
              <li><Link href="/help">Help Center</Link></li>
              <li><Link href="/docs">Documentation</Link></li>
              <li><Link href="/status">Status</Link></li>
              <li><Link href="/security">Security</Link></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-200 dark:border-gray-700 mt-8 pt-8 text-center text-gray-600 dark:text-gray-300">
          <p>&copy; 2024 DocIntel. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
