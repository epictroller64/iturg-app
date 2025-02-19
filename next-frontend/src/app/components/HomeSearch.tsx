'use client'
import { searchStore } from "../lib/stores/search-store";



export default function HomeSearch() {
    const { search, setSearch } = searchStore();
    return <div className="w-full max-w-3xl mt-32 mb-16 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
            Otsi kasutatud Apple tooteid
        </h1>

        <div className="relative w-full items-center inline-flex">
            <input
                type="text"
                placeholder="Otsi tooteid"
                className="p-form-text p-4 w-full absolute"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
            {/* <button className="absolute right-2 p-btn p-btn-round p-prim-col">
                Otsi
            </button> */}
        </div>
    </div>

}