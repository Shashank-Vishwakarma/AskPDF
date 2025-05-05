"use client"

import Navbar from "@/components/navbar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { FileText, Plus, Trash2, Upload } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

const filteredPdfs = [
    { id: 1, name: "Business Proposal.pdf", date: "2023-04-15", pages: 12 },
    { id: 2, name: "Financial Report Q1.pdf", date: "2023-03-30", pages: 24 },
    { id: 3, name: "Product Manual.pdf", date: "2023-02-18", pages: 45 },
    { id: 4, name: "Research Paper.pdf", date: "2023-01-22", pages: 18 },
    { id: 5, name: "Meeting Notes.pdf", date: "2023-04-10", pages: 5 },
]

export default function Dashboard() {
    // const [filteredPdfs, setFilteredPdfs] = useState([]);
    const [isUploading, setIsUploading] = useState(false);
    
    return <div className="min-h-screen">
        <Navbar />

        <div className="flex items-center justify-between mb-8 px-6 py-8">
            <h1 className="text-3xl font-bold">Your PDFs</h1>

            <Dialog>
                <DialogTrigger asChild>
                    <Button className="bg-purple-600 hover:bg-purple-700">
                    <Plus className="mr-2 h-4 w-4" /> Upload PDF
                    </Button>
                </DialogTrigger>
                <DialogContent>
                    <DialogHeader>
                    <DialogTitle>Upload a new PDF</DialogTitle>
                    <DialogDescription>Upload a PDF file to start chatting with it</DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
                        <Upload className="mx-auto h-12 w-12 text-gray-400" />
                        <Input type="file" accept=".pdf" className="hidden" id="pdf-upload" />
                        <Button
                            variant="outline"
                            onClick={() => document.getElementById("pdf-upload")?.click()}
                            className="mt-4 cursor-pointer"
                        >
                            Select PDF
                        </Button>
                    </div>
                    </div>
                    <DialogFooter>
                    <Button disabled={isUploading} className="bg-purple-600 hover:bg-purple-700 cursor-pointer">
                        {isUploading ? "Uploading..." : "Upload"}
                    </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
                {filteredPdfs.map((pdf) => (
                    <Card key={pdf.id} className="overflow-hidden">
                        <div className="h-40 bg-gray-100 flex items-center justify-center">
                            <FileText className="h-16 w-16 text-gray-400" />
                        </div>
                        <CardContent className="p-4">
                            <h3 className="font-medium truncate" title={pdf.name}>
                                {pdf.name}
                            </h3>
                            <div className="flex justify-between text-sm text-gray-500 mt-1">
                            <span>{pdf.date}</span>
                            <span>{pdf.pages} pages</span>
                            </div>
                        </CardContent>
                        <CardFooter className="p-4 pt-0 flex justify-between">
                            <Button variant="outline" size="sm" asChild>
                            <Link href={`/chat/${pdf.id}`}>Chat</Link>
                            </Button>
                            <Button variant="destructive" className="hover:cursor-pointer">
                                {/* <Link href={`/chat/${pdf.id}`}>Chat</Link> */}
                                <Trash2 />
                            </Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>
    </div>;
}