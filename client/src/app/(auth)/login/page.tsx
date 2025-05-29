"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft } from "lucide-react"
import axios from "axios"
import { useAuthStore } from "@/zustand/store"
import { UserProps } from "@/zustand/store"
import { useRouter } from "next/navigation"

export default function LoginPage() {
    const [isLoading, setIsLoading] = useState(false)

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const setUser = useAuthStore((state) => state.setUser)

    const router = useRouter()

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        setIsLoading(true)

        try {
            const response = await axios.post("http://localhost:8000/api/v1/auth/login", {email, password})
            if(!response.data) {
                throw new Error("Something went wrong")
            }

            const user: UserProps = {
                name: response.data.name,
                email: response.data.email,
                token: response.data.token
            }
            setUser(user)
            localStorage.setItem("user", JSON.stringify(user))

            router.push("/dashboard")
        } catch (error) {
            console.log(error)
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
            <div className="w-full max-w-md">
                <Link href="/" className="flex items-center gap-2 text-purple-600 mb-6 hover:underline">
                    <ArrowLeft size={16} />
                    Back to home
                </Link>

                <Card>
                    <CardHeader>
                        <CardTitle className="text-2xl">Welcome back</CardTitle>
                        <CardDescription>Log in to your account to continue</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="email">Email</Label>
                                <Input 
                                    id="email" 
                                    type="email" 
                                    placeholder="you@example.com" 
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required 
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="password">Password</Label>
                                <Input 
                                    id="password" 
                                    type="password" 
                                    placeholder="••••••••" 
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required 
                                />
                            </div>
                            <Button type="submit" className="w-full bg-purple-600 hover:bg-purple-700 cursor-pointer" disabled={isLoading}>
                                {isLoading ? "Logging in..." : "Log in"}
                            </Button>
                        </form>
                    </CardContent>
                    <CardFooter className="flex justify-center">
                        <p className="text-sm text-gray-600">
                            Don't have an account?{" "}
                            <Link href="/register" className="text-purple-600 hover:underline">
                                Register
                            </Link>
                        </p>
                    </CardFooter>
                </Card>
            </div>
        </div>
    )
}
