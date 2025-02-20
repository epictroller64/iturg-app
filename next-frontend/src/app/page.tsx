import HomeSearch from "./components/HomeSearch";
import SearchResults from "./components/SearchResults";
import { LocalApi } from "./lib/LocalApi";
import LatestProducts from "./components/LatestProducts";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Apple Toodete Hinnavõrdlus | Parimad Pakkumised',
  description: 'Jälgi ja võrdle kasutatud Apple toodete hindu Eesti populaarsematel turgudel. Leia parimad pakkumised iPhone\'idele, MacBook\'idele, iPad\'idele ja teistele.',
  keywords: 'apple, iphone, macbook, ipad, kasutatud, tooted, hinnavõrdlus, eesti, pakkumised, hindade võrdlus',
  openGraph: {
    title: 'Apple Toodete Hinnavõrdlus | Parimad Pakkumised',
    description: 'Jälgi ja võrdle kasutatud Apple toodete hindu Eesti populaarsematel turgudel',
    type: 'website',
    locale: 'et_EE',
  },
  robots: {
    index: true,
    follow: true,
  },
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#f9fafb'
};

export default async function Home() {
  const products = await LocalApi.getProducts("", 1, 10, "created_at", "desc");
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center">
      <HomeSearch />
      <SearchResults />
      <LatestProducts products={products} />
    </main>
  );
}
