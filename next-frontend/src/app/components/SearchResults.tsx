'use client'

import { useQuery } from "@tanstack/react-query";
import { searchStore } from "../lib/stores/search-store";
import { LocalApi } from "../lib/LocalApi";
import { ProductCard } from "./ProductCard";
import SortingControls from "./SortingControls";
import FilterControls from "./FilterControls";
import { ProductPreviewDTO } from "../lib/types/ProductPreviewDTO";
import ProductSkeleton from "./product/ProductSkeleton";



export default function SearchResults() {
    const { search, sortBy, sortDirection, filters } = searchStore();

    const { data: products = [], isLoading } = useQuery({
        queryKey: ['products', search, sortBy, sortDirection, filters],
        queryFn: () => LocalApi.getProducts(
            search,
            1,
            10,
            sortBy,
            sortDirection,
            filters
        )
    });
    console.log(products)
    console.log(isLoading)
    return (
        <div className="flex gap-6 w-full">
            <div className="flex-shrink-0">
                <FilterControls />
            </div>

            <div className="w-full">
                <div className="flex justify-between items-center mb-6">
                    <SortingControls />
                </div>
                <Products isLoading={isLoading} products={products} />
            </div>
        </div>
    );
}


function Products({ isLoading, products }: { isLoading: boolean, products: ProductPreviewDTO[] }) {
    if (isLoading) {
        return <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full">
            {Array.from({ length: 6 }).map((_, index) => (
                <ProductSkeleton key={index} />
            ))}
        </div>
    }
    if (products.length === 0) {
        return <div className="text-center text-gray-500 w-full">
            <h2 className="text-2xl font-semibold text-gray-900">Otsingu tulemused</h2>
            <p className="text-lg">Ei leitud ühtegi toodet</p>
        </div>
    }
    return <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full">
        {products.map((product) => (
            <ProductCard key={product.id} product={product} />
        ))}
    </div>
}
