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
import { useAuthStore, UserProps } from "@/zustand/store"
import { useRouter } from "next/navigation"

export default function SignupPage() {
    const [isLoading, setIsLoading] = useState(false)

    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")

    const setUser = useAuthStore((state) => state.setUser)

    const router = useRouter()

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        setIsLoading(true)

        try {
            const response = await axios.post("http://localhost:8000/api/v1/auth/register", {name, email, password, confirm_password: confirmPassword})
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
                        <CardTitle className="text-2xl">Create an account</CardTitle>
                        <CardDescription>Sign up to start chatting with your PDFs</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="name">Name</Label>
                                <Input 
                                    id="name" 
                                    type="text" 
                                    placeholder="John Doe" 
                                    value={name}
                                    onChange={(e) => setName(e.target.value)} 
                                    required 
                                />
                            </div>
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
                            <div className="space-y-2">
                                <Label htmlFor="confirmPassword">Confirm Password</Label>
                                <Input 
                                    id="confirmPassword" 
                                    type="password" 
                                    placeholder="••••••••" 
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)} 
                                    required 
                                />
                            </div>
                            <Button type="submit" className="w-full bg-purple-600 hover:bg-purple-700 cursor-pointer" disabled={isLoading}>
                                {isLoading ? "Creating account..." : "Sign up"}
                            </Button>
                        </form>
                    </CardContent>
                    <CardFooter className="flex justify-center">
                        <p className="text-sm text-gray-600">
                            Already have an account?{" "}
                            <Link href="/login" className="text-purple-600 hover:underline">
                                Login
                            </Link>
                        </p>
                    </CardFooter>
                </Card>
            </div>
        </div>
    )
}
