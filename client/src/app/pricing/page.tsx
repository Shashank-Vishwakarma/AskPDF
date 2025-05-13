import type React from "react"
import { Check } from "lucide-react"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import Navbar from "@/components/navbar"

export default function PricingPage() {
    return (
        <>
        <Navbar />

        <div className="container mx-auto py-16 px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
                <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">Simple, transparent pricing</h1>
                <p className="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
                Choose the plan that's right for you and start chatting with your PDF documents today.
                </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
                {/* Free Plan */}
                <Card className="flex flex-col border-2 shadow-lg">
                <CardHeader className="pb-8">
                    <CardTitle className="text-2xl font-bold">Free</CardTitle>
                    <CardDescription className="text-gray-600 mt-2">Perfect for getting started with PDF chat</CardDescription>
                    <div className="mt-4">
                        <span className="text-4xl font-bold">$0</span>
                        <span className="text-gray-600 ml-2">/ month</span>
                    </div>
                </CardHeader>
                <CardContent className="flex-grow">
                    <ul className="space-y-3">
                        <FeatureItem>Upload up to 3 PDF documents</FeatureItem>
                        <FeatureItem>Maximum 5 pages per PDF</FeatureItem>
                        <FeatureItem>Basic chat functionality</FeatureItem>
                        <FeatureItem>Standard response time</FeatureItem>
                    </ul>
                </CardContent>
                <CardFooter>
                    <Button asChild className="w-full" variant="outline">
                    <Link href="/register">Get Started</Link>
                    </Button>
                </CardFooter>
                </Card>

                {/* Pro Plan */}
                <Card className="flex flex-col border-2 border-purple-500 shadow-lg relative overflow-hidden">
                <div className="absolute top-0 right-0 bg-purple-500 text-white px-4 py-1 rounded-bl-lg text-sm font-medium">
                    Popular
                </div>
                <CardHeader className="pb-8">
                    <CardTitle className="text-2xl font-bold">Pro</CardTitle>
                    <CardDescription className="text-gray-600 mt-2">
                        For professionals who need advanced features
                    </CardDescription>
                    <div className="mt-4">
                        <span className="text-4xl font-bold">$15</span>
                        <span className="text-gray-600 ml-2">/ month</span>
                    </div>
                </CardHeader>
                <CardContent className="flex-grow">
                    <ul className="space-y-3">
                        <FeatureItem>Unlimited PDF uploads</FeatureItem>
                        <FeatureItem>Maximum 50 pages per PDF</FeatureItem>
                        <FeatureItem>Advanced AI chat capabilities</FeatureItem>
                        <FeatureItem>Priority response time</FeatureItem>
                    </ul>
                </CardContent>
                <CardFooter>
                    <Button asChild className="w-full bg-purple-600 hover:bg-purple-700">
                        <Link href="/register?plan=pro">Upgrade to Pro</Link>
                    </Button>
                </CardFooter>
                </Card>
            </div>
        </div>
        </>
    )
}

function FeatureItem({ children }: { children: React.ReactNode }) {
    return (
        <li className="flex items-start">
            <div className="flex-shrink-0">
                <Check className="h-5 w-5 text-green-500" />
            </div>
            <p className="ml-3 text-gray-600">{children}</p>
        </li>
    )
}
