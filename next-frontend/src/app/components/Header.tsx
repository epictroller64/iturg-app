import Link from 'next/link'

export default function Header() {
    return (
        <header className="fixed w-full p-blur-1 z-10">
            <div className="container mx-auto px-4 flex justify-between items-center">
                <Link href="/" className="p-nav-title">
                    iTurg.ee
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
