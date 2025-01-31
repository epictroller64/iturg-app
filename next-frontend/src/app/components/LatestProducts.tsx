import { ProductPreviewDTO } from "../lib/types/ProductPreviewDTO";
import { ProductCard } from "./ProductCard";

export default function LatestProducts({ products }: { products: ProductPreviewDTO[] }) {

    return <div className="mb-16 mt-16">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Viimased leitud tooted</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full">
            {products.map((product) => (
                <ProductCard key={product.id} product={product} />
            ))}
        </div>
    </div>
}