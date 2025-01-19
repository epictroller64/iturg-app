import HomeSearch from "./components/HomeSearch";
import { ProductCard } from "./components/ProductCard";
import SearchResults from "./components/SearchResults";
import { LocalApi } from "./lib/LocalApi";


export default async function Home() {
  // Example products - would be fetched from API in real implementation
  const products = await LocalApi.getProducts("", 1, 10, "updated_at", "desc");
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center px-4">
      <HomeSearch />
      <SearchResults />
      <div className="w-full max-w-6xl mb-16">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Viimased leitud tooted</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </main>
  );
}
