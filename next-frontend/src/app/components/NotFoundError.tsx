import Link from "next/link";

export default function NotFoundError() {
    return (
        <main className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
            <div className="text-center p-8 bg-white rounded-lg shadow-lg">
                <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
                <div className="w-16 h-1 bg-blue-500 mx-auto mb-4"></div>
                <h2 className="text-2xl font-semibold text-gray-700 mb-4">Ei leitud</h2>
                <p className="text-gray-600 mb-6">Kahjuks ei leidnud me otsitud lehte.</p>
                <Link
                    href="/"
                    className="p-btn p-btn-md"
                >
                    Tagasi avalehele
                </Link>
            </div>
        </main>
    );
}

