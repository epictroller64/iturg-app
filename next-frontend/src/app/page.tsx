import HomeSearch from "./components/HomeSearch";
import SearchResults from "./components/SearchResults";
import { LocalApi } from "./lib/LocalApi";
import LatestProducts from "./components/LatestProducts";


export default async function Home() {
  // Example products - would be fetched from API in real implementation
  const products = await LocalApi.getProducts("", 1, 10, "updated_at", "desc");
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center">
      <HomeSearch />
      <SearchResults />
      <LatestProducts products={products} />
    </main>
  );
}
