import { User2 } from "lucide-react";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "./ui/dropdown-menu";
import Link from "next/link";

const tabs = [
    {
        label: "Pricing",
        href: "/pricing",
    },
]

export default function Navbar() {
    return (
        <header className="w-full h-18 sticky flex items-center justify-between border-b border-gray-200 bg-white/60 px-6 py-2">
            <Link href="/">
                <h3 className="text-2xl font-bold">AskPDF</h3>
            </Link>

            <div>
                {
                    tabs.map((tab) => (
                        <div key={tab.href}>
                            <Link href={tab.href} className="text-blue-600">
                                {tab.label}
                            </Link>
                        </div>
                    ))
                }
            </div>

            <div>
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <User2 className="rounded-full w-8 h-8 bg-gray-300 p-2 cursor-pointer" />
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                        <DropdownMenuItem>
                            <p>Logout</p>
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
        </header>
    )
}