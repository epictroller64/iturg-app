import { Product } from "./types/Product";
import { ProductPreviewDTO } from "./types/ProductPreviewDTO";



const baseUrl = "http://localhost:8000/api"

export const LocalApi = {
    getProducts: async () => {
        return await get<ProductPreviewDTO[]>("products");
    },
    getProductDetails: async (id: string) => {
        return await get<Product>(`products/${id}`);
    }
}


async function get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${baseUrl}/${endpoint}`);
    return response.json();
}

async function post<T>(endpoint: string, body: T): Promise<T> {
    const response = await fetch(`${baseUrl}/${endpoint}`, {
        method: "POST",
        body: JSON.stringify(body),
    });
    return response.json();
}