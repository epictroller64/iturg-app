'use client'

import { useQuery } from "@tanstack/react-query";
import { searchStore } from "../lib/stores/search-store";
import { LocalApi } from "../lib/LocalApi";
import { ProductPreviewDTO } from "../lib/types/ProductPreviewDTO";
import { ProductCard } from "./ProductCard";

export default function SearchResults() {
    const { search, page, pageSize, sortBy, sortOrder } = searchStore();
    const { data: products, isLoading, error } = useQuery<ProductPreviewDTO[]>({
        queryKey: ["products", search, page, pageSize, sortBy, sortOrder],
        queryFn: () => LocalApi.getProducts(search, page, pageSize, sortBy, sortOrder)
    });

    if (isLoading) {
        return <div className="w-full h-96 flex items-center justify-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
        </div>
    }

    if (error) {
        return <div className="w-full h-96 flex items-center justify-center text-red-500">
            Error loading products
        </div>
    }

    if (!products?.length) {
        return <div className="w-full h-96 flex items-center justify-center text-gray-500">
            No products found
        </div>
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 p-6">
            {products.map((product) => (
                <ProductCard key={product.id} product={product} />
            ))}
        </div>
    );
}

