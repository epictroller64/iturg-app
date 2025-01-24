import { Product } from "./types/Product";
import { ProductPreviewDTO } from "./types/ProductPreviewDTO";



const baseUrl = "http://localhost:8000/api"

export const LocalApi = {
    getProducts: async (search: string, page: number, pageSize: number, sortBy: string, sortOrder: string) => {
        return await get<ProductPreviewDTO[]>(`products?search=${search}&page=${page}&page_size=${pageSize}&sort_by=${sortBy}&sort_order=${sortOrder}`);
    },
    getProductDetails: async (id: string) => {
        return await get<Product>(`products/${id}`);
    },
    getSimilarProducts: async (id: string) => {
        return await get<ProductPreviewDTO[]>(`similar/products/${id}`);
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

async function post<T>(endpoint: string, body: T): Promise<T> {
    try {
        const response = await fetch(`${baseUrl}/${endpoint}`, {
            method: "POST",
            body: JSON.stringify(body),
        });
        return response.json();
    } catch (error) {
        console.log('Error posting data:', error);
        throw error;
    }
}