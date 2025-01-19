'use client'
import { searchStore } from "../lib/stores/search-store";



export default function HomeSearch() {
    const { search, setSearch } = searchStore();
    return <div className="w-full max-w-3xl mt-32 mb-16 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
            Otsi kasutatud Apple tooteid
        </h1>

        <div className="relative">
            <input
                type="text"
                placeholder="Otsi tooteid"
                className="w-full px-6 py-4 text-lg rounded-full border border-gray-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
            <button className="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-500 text-white px-8 py-2 rounded-full hover:bg-blue-600 transition">
                Otsi
            </button>
        </div>
    </div>

}