'use client'

import { useQuery } from "@tanstack/react-query"
import { LocalApi } from "../lib/LocalApi"
import { likeStore } from "../lib/stores/liked-store"
import { ProductCard } from "./ProductCard"

export default function FavoriteProductsClient() {
    const { liked } = likeStore()
    const query = useQuery({
        queryKey: ['products', liked],
        queryFn: () => liked.length === 0 ? [] : LocalApi.getProductsByIds(liked),
    })
    if (query.isLoading) return <div>Loading...</div>
    if (query.isError) return <div>Error</div>
    if (!query.data) return null
    if (query.data.length === 0) return <div>Tooteid ei leitud. Lisa enne mõni toode lemmikutesse!</div>
    console.log(query.data)
    return <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
        {query.data?.map((product) => <ProductCard key={product.id} product={product} />)}
    </div>
}