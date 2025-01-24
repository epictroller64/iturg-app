import Link from "next/link";

export default function Footer() {
    return (
        <footer className="bg-gray-800 text-white py-8 mt-auto">
            <div className="container mx-auto px-4">
                <div className="flex flex-col md:flex-row justify-between items-center">
                    <div className="mb-4 md:mb-0">
                        <p className="text-sm">© {new Date().getFullYear()} iTurg.ee. Kõik õigused kaitstud.</p>
                    </div>
                    <div className="flex gap-6">
                        <Link href="#" className="text-gray-300 hover:text-white transition-colors">
                            Privaatsuspoliitika
                        </Link>
                        <Link href="#" className="text-gray-300 hover:text-white transition-colors">
                            Kasutustingimused
                        </Link>
                        <Link href="#" className="text-gray-300 hover:text-white transition-colors">
                            Kontakt
                        </Link>
                    </div>
                </div>
            </div>
        </footer>
    );
}
