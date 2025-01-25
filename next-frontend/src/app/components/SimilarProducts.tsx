import { ProductPreviewDTO } from "../lib/types/ProductPreviewDTO";
import { ProductCard } from "./ProductCard";



export default function SimilarProducts({ products }: { products: ProductPreviewDTO[] }) {
    return <div>
        <h2>Sarnased tooted</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {products.map((product) => (
                <ProductCard key={product.id} product={product} />
            ))}
        </div>
    </div>
}