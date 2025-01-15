export type Product = {
    id: string;
    platform: string; // okidoki, soov, etc
    name: string;
    description: string;
    category: string;
    brand: string;
    seller_url: string;
    product_url: string;
    location: string;
    created_at: Date;
    updated_at: Date;
    images: string; // JSON array of image urls
}
