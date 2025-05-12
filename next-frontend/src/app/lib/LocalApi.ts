import { Product } from "./types/Product";
import { ProductPreviewDTO } from "./types/ProductPreviewDTO";
import { FilterResponse } from "./types/FilterResponse";


const baseUrl = process.env.NEXT_PUBLIC_API_HOST || "http://localhost:8000/api"

interface FilterOptions {
    minPrice?: number;
    maxPrice?: number;
    device?: string;
}

export const LocalApi = {
    getProducts: async (search: string, page: number, pageSize: number, sortBy: string, sortDirection: string, filters?: FilterOptions) => {
        return await get<FilterResponse<ProductPreviewDTO>>(`products/search?search=${search}&page=${page}&page_size=${pageSize}&sort_by=${sortBy}&sort_direction=${sortDirection}${filters ? `&filters=${JSON.stringify(filters)}` : ""}`);
    },
    getProductDetails: async (id: string) => {
        return await get<Product>(`products/id/${id}`);
    },
    getSimilarProducts: async (id: string) => {
        return await get<ProductPreviewDTO[]>(`similar/products/${id}`);
    },
    getProductsByIds: async (ids: string[]) => {
        return await get<ProductPreviewDTO[]>(`products/ids?ids=${ids.join(',')}`);
    },
    incrementPostView: async (id: string) => {
        return await get<void>(`products/increment-post-view/${id}`);
    }
}



async function get<T>(endpoint: string): Promise<T> {
    try {
        const response = await fetch(`${baseUrl}/${endpoint}`);
        return response.json();
    } catch (error) {
        console.log('Error fetching data:', error);
        throw error;
    }
}
