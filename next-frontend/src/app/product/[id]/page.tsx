import ProductGraph from "@/app/components/product/ProductGraph";
import { LocalApi } from "@/app/lib/LocalApi"
import ProductGallery from "@/app/components/product/ProductGallery";



export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    const productDetails = await LocalApi.getProductDetails(id);
    return (
        <div className="container mx-auto p-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <ProductGallery images={productDetails.images} name={productDetails.name} />
                <div>
                    <h1 className="p-large-title mb-4">{productDetails.name}</h1>
                    <div className="space-y-4">
                        <div className="p-card">
                            <div className="p-card-content">
                                <h2>Viimane hind</h2>
                                <p className="text-2xl text-green-600">
                                    €{productDetails.price_history[productDetails.price_history.length - 1]?.price || 'N/A'}
                                </p>
                            </div>
                        </div>

                        <div className="p-card">
                            <div className="p-card-content">
                                <h2>Platform</h2>
                                <p>{productDetails.platform}</p>
                            </div>
                        </div>

                        <ProductCategory category={productDetails.category} />
                        <div className="p-card">
                            <div className="p-card-content">
                                <h2>Asukoht</h2>
                                <p>{productDetails.location}</p>
                            </div>
                        </div>


                        <ProductDescription description={productDetails.description} />

                        <div className="p-card">
                            <div className="p-card-content">
                                <h2>Lisatud</h2>
                                <p>Lisatud andmebaasi: {new Date(productDetails.created_at).toLocaleDateString()}</p>
                                <p>Uuendatud: {new Date(productDetails.updated_at).toLocaleDateString()}</p>
                            </div>
                        </div>

                        <a
                            href={productDetails.product_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-btn p-prim-col p-btn-lg"
                        >
                            Vaata pakkumist
                        </a>
                    </div>
                </div>
            </div>

            <ProductGraph product={productDetails} />
        </div>
    );
}




function ProductCategory({ category }: { category: string[] }) {
    return <div className="p-card">
        <div className="p-card-content">
            <h2 className="p-subhead">Kategooria</h2>
            <p>{category.join(' -> ')}</p>
        </div>
    </div>
}
function ProductDescription({ description }: { description: string }) {
    return <div className="p-card">
        <div className="p-card-content">
            <h2 className="p-subhead">Kirjeldus</h2>
            <div className="whitespace-pre-wrap" dangerouslySetInnerHTML={{ __html: description }} />
        </div>
    </div>
}
