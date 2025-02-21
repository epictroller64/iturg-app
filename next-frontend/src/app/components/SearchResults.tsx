'use client'

import { useQuery } from "@tanstack/react-query";
import { searchStore } from "../lib/stores/search-store";
import { LocalApi } from "../lib/LocalApi";
import { ProductCard } from "./ProductCard";
import SortingControls from "./SortingControls";
import FilterControls from "./FilterControls";
import { ProductPreviewDTO } from "../lib/types/ProductPreviewDTO";
import ProductSkeleton from "./product/ProductSkeleton";
import Pagination from "./Pagination";



export default function SearchResults() {
    const { search, sortBy, sortDirection, filters, page, pageSize, setPage } = searchStore();

    const { data: filterResponse = { data: [], page: 1, page_size: pageSize, max_pages: 1 }, isLoading } = useQuery({
        queryKey: ['products', search, sortBy, sortDirection, filters, page, pageSize],
        queryFn: () => LocalApi.getProducts(
            search,
            page,
            pageSize,
            sortBy,
            sortDirection,
            filters
        )
    });
    console.log(filterResponse)
    function onPageChange(page: number) {
        setPage(page);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    return (
        <div className="flex gap-6 w-full">
            <div className="flex-shrink-0">
                <FilterControls />
            </div>

            <div className="w-full">
                <div className="flex justify-between items-center mb-6">
                    <SortingControls />
                </div>
                <Products isLoading={isLoading} products={filterResponse.data} />
                <Pagination currentPage={page} totalPages={filterResponse.max_pages} onPageChange={onPageChange} />
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
