import Link from 'next/link'

export default function Header() {
    return (
        <header className="fixed w-full p-blur-1 z-10">
            <div className="container mx-auto px-4 flex justify-between items-center">
                <Link href="/" className="p-nav-title font-bold text-2xl relative group">
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-teal-400">
                        i
                    </span>
                    <span className="text-gray-800 dark:text-gray-200">
                        Turg
                    </span>
                    <span className="text-blue-500">.ee</span>
                    <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-500 to-teal-400 group-hover:w-full transition-all duration-300"></span>
                </Link>
                <nav>
                    <ul className="flex space-x-4">
                        <li>
                            <Link href="/" className="p-btn p-btn-text">
                                Avaleht
                            </Link>
                        </li>
                        <li>
                            <Link href="/lemmikud" className="p-btn p-btn-text">
                                Lemmikud
                            </Link>
                        </li>
                    </ul>
                </nav>
            </div>
        </header>
    )
}
