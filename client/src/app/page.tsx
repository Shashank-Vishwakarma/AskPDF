import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, FileText, MessageSquare, Upload } from "lucide-react"
import Image from "next/image"
import Navbar from "@/components/navbar"

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
    
      {/* Hero Section */}
      <header className="bg-gradient-to-r from-purple-600 to-pink-600 text-white">
        <div className="container mx-auto px-4 py-20 max-w-6xl">
          <div className="flex flex-col md:flex-row items-center justify-between gap-12">
            <div className="flex-1 space-y-6">
              <h1 className="text-4xl md:text-6xl font-bold leading-tight">Chat with your PDFs using AI</h1>
              <p className="text-xl md:text-2xl opacity-90">
                Upload your documents and get instant answers from our advanced AI assistant. No more scrolling through
                pages to find what you need.
              </p>
            </div>
            <div className="flex-1">
              <div className="relative">
                <div className="absolute -top-6 -left-6 w-full h-full bg-purple-800 rounded-lg"></div>
                <div className="relative bg-white p-4 rounded-lg shadow-xl">
                  <Image
                    src={"/placeholder.svg?height=400&width=500"}
                    alt="PDF Chat Demo"
                    width={500}
                    height={400}
                    className="rounded border border-gray-200"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-100">
        <div className="container mx-auto px-4 max-w-6xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">How It Works</h2>

          <div className="grid md:grid-cols-3 gap-10">
            <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center">
              <div className="w-16 h-16 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <Upload size={28} />
              </div>
              <h3 className="text-xl font-semibold mb-3">Upload Your PDFs</h3>
              <p className="text-gray-600">
                Simply upload your PDF documents to our secure platform.
              </p>
            </div>

            <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center">
              <div className="w-16 h-16 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <FileText size={28} />
              </div>
              <h3 className="text-xl font-semibold mb-3">Instant Processing</h3>
              <p className="text-gray-600">Our AI quickly analyzes and understands the content of your documents.</p>
            </div>

            <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center">
              <div className="w-16 h-16 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <MessageSquare size={28} />
              </div>
              <h3 className="text-xl font-semibold mb-3">Chat & Get Answers</h3>
              <p className="text-gray-600">
                Ask questions about your document and receive accurate, contextual responses.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-purple-600 text-white">
        <div className="container mx-auto px-4 text-center max-w-3xl">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">Ready to chat with your PDFs?</h2>
          <p className="text-xl mb-10 opacity-90">
            Join thousands of professionals who save hours by using our AI-powered PDF chat.
          </p>
          <Button asChild size="lg" className="bg-white text-purple-600 hover:bg-gray-100 cursor-pointer">
            <Link href="/register" className="flex items-center gap-2">
              Get Started Now <ArrowRight size={16} />
            </Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-10 bg-gray-900 text-gray-400">
        <div className="container mx-auto px-4">
          <div className="mt-8 text-center text-sm">
            &copy; {new Date().getFullYear()} AskPDF. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}
