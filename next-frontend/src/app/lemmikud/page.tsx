import FavoriteProductsClient from "../components/FavoriteProductsClient";

export default function Page() {
    return <main className="container mx-auto p-4">
        <h1 className="p-large-title">Lemmikud</h1>
        <FavoriteProductsClient />
    </main>

}