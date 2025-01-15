import { LocalApi } from "./lib/LocalApi";

export default async function Home() {
  // Example products - would be fetched from API in real implementation
  const products = await LocalApi.getProducts();
  console.log(products);
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center px-4">
      {/* Hero Section */}
      <div className="w-full max-w-3xl mt-32 mb-16 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          Find Apple Products in Estonia
        </h1>

        {/* Search Bar */}
        <div className="relative">
          <input
            type="text"
            placeholder="Search for Apple products..."
            className="w-full px-6 py-4 text-lg rounded-full border border-gray-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
          <button className="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-500 text-white px-8 py-2 rounded-full hover:bg-blue-600 transition">
            Search
          </button>
        </div>
      </div>

      {/* Latest Products */}
      <div className="w-full max-w-6xl mb-16">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Latest Finds</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <div
              key={product.id}
              className="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition"
            >
              <img
                src={product.imageUrl}
                alt={product.name}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <h3 className="font-medium text-lg text-gray-900">{product.name}</h3>
                <p className="text-gray-500 text-sm mt-1">{product.price} €</p>
                <div className="mt-4 flex justify-between items-center">
                  <span className="text-sm font-medium text-blue-500">View Details →</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}