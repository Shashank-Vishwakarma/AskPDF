"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ArrowLeft, Send } from "lucide-react"
import Link from "next/link"
import Navbar from "@/components/navbar"
import axios from "axios"
import { useParams } from "next/navigation"

// Mock PDF data
const mockPdf = {
  id: 1,
  name: "Business Proposal.pdf",
  url: "/placeholder.svg?height=800&width=600",
}

// Mock chat messages
const initialMessages = [
  { id: 1, role: "system", content: "Hello! I'm your PDF assistant. Ask me anything about this document." },
]

export default function ChatPage() {
  const [messages, setMessages] = useState(initialMessages)
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const params = useParams();

  useEffect(()=>{
    const fetchPdf = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/v1/documents/${params.fileId}`,
          {
            headers: {
              Authorization: `Bearer ${JSON.parse(localStorage.getItem("user")!)["token"]} `,
            }
          }
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchPdf()
  }, [])

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    // Add user message
    const userMessage = { id: Date.now(), role: "user", content: input }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      const aiMessage = {
        id: Date.now(),
        role: "assistant",
        content: `I've analyzed the document and found information related to "${input}". The business proposal contains details about project scope, timeline, and budget considerations. Would you like me to elaborate on any specific section?`,
      }
      setMessages((prev) => [...prev, aiMessage])
      setIsLoading(false)
    }, 1500)
  }

  return (
    <div className="flex flex-col h-[calc(100vh-20px)] bg-gray-50">
        <Navbar />
        
        <div className="flex gap-2 h-full">
          <div className="w-1/2 p-4 border-r">
            <div className="flex items-center gap-2 mb-4">
              <Link href="/dashboard">
                <Button variant="ghost" size="icon">
                  <ArrowLeft className="h-4 w-4" />
                </Button>
              </Link>
              <h2 className="font-semibold">{mockPdf.name}</h2>
            </div>
            <div className="bg-gray-100 rounded-lg h-[calc(100%-40px)] overflow-auto">
              {/* <iframe src={mockPdf.url} className="w-full h-full" title={mockPdf.name} /> */}
            </div>
          </div>

        {/* Chat Interface */}
        <div className="w-1/2 flex flex-col">
          <div className="flex-1 p-4 overflow-auto">
            <div className="space-y-4">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${
                      message.role === "user"
                        ? "bg-purple-600 text-white"
                        : message.role === "system"
                          ? "bg-gray-200 text-gray-800"
                          : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="max-w-[80%] rounded-lg p-3 bg-gray-100">
                    <div className="flex space-x-2">
                      <div
                        className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"
                        style={{ animationDelay: "0ms" }}
                      ></div>
                      <div
                        className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"
                        style={{ animationDelay: "150ms" }}
                      ></div>
                      <div
                        className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"
                        style={{ animationDelay: "300ms" }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>
          <div className="p-4 border-t">
            <form onSubmit={handleSubmit} className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question about this PDF..."
                disabled={isLoading}
              />
              <Button type="submit" disabled={isLoading || !input.trim()} className="bg-purple-600 hover:bg-purple-700">
                <Send className="h-4 w-4" />
              </Button>
            </form>
          </div>
        </div>
        </div>
      </div>
  )
}
