import { PriceHistory } from "./PriceHistory";

export type Product = {
    id: string;
    platform: string; // okidoki, soov, etc
    name: string;
    description: string;
    category: string[];
    brand: string;
    seller_url: string;
    product_url: string;
    location: string;
    created_at: Date;
    updated_at: Date;
    images: string[]; // JSON array of image urls
    price_history: PriceHistory[];
    device: string | null;
    chip: string | null;
    ram: string | null;
    screen_size: string | null;
    generation: string | null;
    storage: string | null;
    color: string | null;
    status: string | null;
    year: string | null;
    watch_mm: string | null;
}
