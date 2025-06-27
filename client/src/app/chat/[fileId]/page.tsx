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
import { cn } from "@/lib/utils"
import Markdown from "react-markdown"

type ROLE = "user" | "assistant"

interface Message {
  role: ROLE
  content: string
  created_at: string
}

interface PDFDoc {
  id: number
  name: string
  url: string
  insert_status: boolean
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [pdf, setPdf] = useState<PDFDoc | null>(null)
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
        setPdf(response.data)
      } catch (error) {
        console.error(error);
      }
    }

    fetchPdf()
  }, [])

  useEffect(()=>{
    const fetchConversation = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/v1/documents/${params.fileId}/user/pdf/chats`,
          {
            headers: {
              Authorization: `Bearer ${JSON.parse(localStorage.getItem("user")!)["token"]} `,
            }
          }
        );
        setMessages(response.data)
      } catch (error) {
        console.error(error);
      }
    }

    if(pdf?.insert_status) {
      fetchConversation()
    } else {
      setMessages([])
    }
  }, [pdf])

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    setIsLoading(true)
    try {
      setMessages(prev => [...prev, {
        role: "user",
        content: input,
        created_at: new Date(Date.now()).toISOString()
      }])
      setInput("")

      const response = await axios.post(
        `http://localhost:8000/api/v1/documents/${params.fileId}/chats`,
        { query: input },
        {
          headers: {
            Authorization: `Bearer ${JSON.parse(localStorage.getItem("user")!)["token"]} `,
          }
        }
      )

      setMessages(prev => [...prev, {
        role: "assistant",
        content: response.data.response,
        created_at: response.data.created_at
      }])
    } catch (error) {
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
        <Navbar />

        <div className="flex gap-2 h-full">
          <div className="w-2/5 p-4 border-r">
            <div className="flex items-center gap-2 mb-4">
              <Link href="/dashboard">
                <Button variant="ghost" size="icon">
                  <ArrowLeft className="h-4 w-4" />
                </Button>
              </Link>
              <h2 className="font-semibold">{pdf?.name}</h2>
            </div>
            <div className="bg-gray-100 rounded-lg h-[calc(100%-40px)] overflow-auto">
              <iframe src={pdf?.url} className="w-full h-full" title={pdf?.name} />
            </div>
          </div>

          <div className="w-3/5 flex flex-col">
            <div className="flex-1 p-4 overflow-auto">
              <div className={cn("space-y-4", messages?.length==0 ? "flex items-center justify-center h-full" : "")}>
                {pdf?.insert_status && messages?.length==0 && (
                  <div className="flex items-center justify-center h-full">
                      <p className="text-gray-500">Start a conversation by typing in the input box below.</p>
                    </div>
                )}

                {pdf?.insert_status && messages?.length>0 && messages?.map((message) => (
                    <div key={message.role+message.content+message.created_at} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                      <div
                        className={`max-w-[80%] rounded-lg p-3 ${
                          message.role === "user"
                            ? "bg-purple-600 text-white"
                            : message.role === "assistant"
                              ? "bg-gray-200 text-gray-800"
                              : "bg-gray-100 text-gray-800"
                        }`}
                      >
                        <Markdown>
                        {message.content}
                        </Markdown>
                      </div>
                    </div>
                  ))}

                {pdf?.insert_status == false && (
                  <div className="flex items-center justify-center h-full">
                    <p className="text-gray-500">We are processing the document, please wait. If it takes too long, try to upload the document again.</p>
                  </div>
                )}

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
