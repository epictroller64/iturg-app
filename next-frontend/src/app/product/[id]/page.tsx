import ProductPriceHistoryGraph from "@/app/components/product/ProductGraph";
import { LocalApi } from "@/app/lib/LocalApi"
import ProductGallery from "@/app/components/product/ProductGallery";
import { Product } from "@/app/lib/types/Product";
import { HiLocationMarker, HiOfficeBuilding, HiClock, HiRefresh, HiArrowDown, HiArrowUp, HiMinus } from "react-icons/hi";
import SimilarProducts from "@/app/components/SimilarProducts";
import NotFoundError from "@/app/components/NotFoundError";
import { ProductPreviewDTO } from "@/app/lib/types/ProductPreviewDTO";
import ProductLike from "@/app/components/product/ProductLike";

export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    let productDetails: Product | null = null;
    let similarProducts: ProductPreviewDTO[] = [];

    try {
        [productDetails, similarProducts] = await Promise.all([
            LocalApi.getProductDetails(id),
            LocalApi.getSimilarProducts(id)
        ]);
    } catch (error) {
        console.error('Error fetching product data:', error);
    }

    if (!productDetails) {
        return <NotFoundError />
    }

    return (
        <div className="container mx-auto p-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="flex flex-col gap-4">
                    <p className="p-subhead">{productDetails.category.join(' -> ')}</p>
                    <ProductGallery images={productDetails.images} name={productDetails.name} />
                </div>
                <div>
                    <div className="flex flex-row justify-between">
                        <h1 className="p-large-title mb-4">{productDetails.name}</h1>
                        <ProductLike id={productDetails.id} />
                    </div>
                    <div className="space-y-4">
                        <PriceCard productDetails={productDetails} />
                        <VisitProductButton productUrl={productDetails.product_url} platform={productDetails.platform} />

                        <Specifications productDetails={productDetails} />

                        <div className="p-card">
                            <div className="p-card-content">
                                <h2 className="text-xl font-semibold flex items-center gap-2">
                                    <HiRefresh className="text-gray-600" />
                                    Platform
                                </h2>
                                <p className="mt-2 text-gray-700 flex items-center gap-2">
                                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                                        {productDetails.platform}
                                    </span>
                                </p>
                            </div>
                        </div>

                        <div className="p-card">
                            <div className="p-card-content">
                                <h2 className="text-xl font-semibold flex items-center gap-2">
                                    <HiLocationMarker className="text-gray-600" />
                                    Asukoht
                                </h2>
                                <p className="mt-2 text-gray-700 flex items-center gap-2">
                                    <HiOfficeBuilding className="text-gray-500" />
                                    {productDetails.location}
                                </p>
                            </div>
                        </div>

                        <ProductDescription description={productDetails.description} />
                        <DateCard product={productDetails} />

                    </div>
                </div>
            </div>
            <ProductPriceHistoryGraph product={productDetails} />
            <SimilarProducts products={similarProducts} />
        </div>
    );
}


function Specifications({ productDetails }: { productDetails: Product }) {
    return <div className="p-card">
        <div className="p-card-content">
            <h2 className="text-xl font-semibold mb-4">Seadme spetsifikatsioonid</h2>
            <div className="grid grid-cols-2 gap-4">
                {productDetails.device && (
                    <div className="flex items-center gap-2">
                        <HiOfficeBuilding className="text-gray-600" />
                        <span className="text-gray-700">{productDetails.device}</span>
                    </div>
                )}
                {productDetails.chip && (
                    <div className="flex items-center gap-2">
                        <HiMinus className="text-gray-600" />
                        <span className="text-gray-700">{productDetails.chip}</span>
                    </div>
                )}
                {productDetails.ram && (
                    <div className="flex items-center gap-2">
                        <HiMinus className="text-gray-600" />
                        <span className="text-gray-700">{productDetails.ram}</span>
                    </div>
                )}
                {productDetails.storage && (
                    <div className="flex items-center gap-2">
                        <HiMinus className="text-gray-600" />
                        <span className="text-gray-700">{productDetails.storage}</span>
                    </div>
                )}
                {productDetails.screen_size && (
                    <div className="flex items-center gap-2">
                        <HiMinus className="text-gray-600" />
                        <span className="text-gray-700">{productDetails.screen_size}</span>
                    </div>
                )}
                {productDetails.color && (
                    <div className="flex items-center gap-2">
                        <HiMinus className="text-gray-600" />
                        <span className="text-gray-700">{productDetails.color}</span>
                    </div>
                )}
                {productDetails.status && (
                    <div className="flex items-center gap-2">
                        <HiMinus className="text-gray-600" />
                        <span className="text-gray-700">{productDetails.status}</span>
                    </div>
                )}
                {productDetails.year && (
                    <div className="flex items-center gap-2">
                        <HiClock className="text-gray-600" />
                        <span className="text-gray-700">{productDetails.year}</span>
                    </div>
                )}
                {productDetails.watch_mm && (
                    <div className="flex items-center gap-2">
                        <HiClock className="text-gray-600" />
                        <span className="text-gray-700">{productDetails.watch_mm}mm</span>
                    </div>
                )}
            </div>
        </div>
    </div>
}

function PriceCard({ productDetails }: { productDetails: Product }) {
    const currentPrice = productDetails.price_history[productDetails.price_history.length - 1]?.price;
    const previousPrice = productDetails.price_history[productDetails.price_history.length - 2]?.price;
    const priceDifference = currentPrice - previousPrice;
    const percentageChange = previousPrice ? ((priceDifference / previousPrice) * 100).toFixed(1) : 0;

    const status = {
        isIncrease: priceDifference > 0,
        isDecrease: priceDifference < 0,
        isSame: priceDifference === 0
    };

    return <div className="p-card">
        <div className="p-card-content">
            <h2 className="text-xl font-semibold mb-2">Viimane hind</h2>
            <div className="flex items-center gap-2">
                <p className={`text-3xl font-bold ${status.isIncrease ? 'text-red-600' :
                    status.isDecrease ? 'text-green-600' : 'text-blue-600'
                    }`}>
                    €{currentPrice || 'N/A'}
                </p>
                {productDetails.price_history.length > 1 && (
                    <span className={`flex items-center gap-1 text-sm px-2 py-1 rounded ${status.isDecrease ? 'bg-green-100 text-green-800' :
                        status.isIncrease ? 'bg-red-100 text-red-800' :
                            'bg-blue-100 text-blue-800'
                        }`}>
                        {status.isDecrease && (
                            <HiArrowDown className="h-4 w-4" />
                        )}
                        {status.isIncrease && (
                            <HiArrowUp className="h-4 w-4" />
                        )}
                        {status.isSame && (
                            <HiMinus className="h-4 w-4" />
                        )}
                        {percentageChange}%
                    </span>
                )}
            </div>
            {productDetails.price_history.length > 1 && (
                <p className="text-sm text-gray-500 mt-2">
                    Varasem hind: €{productDetails.price_history[productDetails.price_history.length - 2].price}
                </p>
            )}
        </div>
    </div>
}


function DateCard({ product }: { product: Product }) {
    return <div className="p-card">
        <div className="p-card-content space-y-4">
            <h2 className="text-xl font-semibold">Toote ajalugu</h2>
            <div className="flex flex-col gap-2 text-gray-600">
                <div className="flex items-center gap-2">
                    <HiClock className="h-5 w-5" />
                    <span className="font-medium">Lisatud andmebaasi:</span>
                    <span>{new Date(product.created_at).toLocaleDateString('et-EE', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    })}</span>
                </div>
                <div className="flex items-center gap-2">
                    <HiRefresh className="h-5 w-5" />
                    <span className="font-medium">Uuendatud:</span>
                    <span>{new Date(product.updated_at).toLocaleDateString('et-EE', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    })}</span>
                </div>
            </div>
        </div>
    </div>
}

function VisitProductButton({ productUrl, platform }: { productUrl: string, platform: string }) {
    return <div className="flex justify-center items-center flex-col">
        <a
            href={platform === "hinnavaatlus" ? `https://foorum.hinnavaatlus.ee/${productUrl}` : productUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="p-btn p-prim-col p-btn-lg"
        >
            Vaata pakkumist
        </a>
        <p className="p-subhead italic">Nupp suunab teid {platform} lehele</p>
    </div>
}


function ProductDescription({ description }: { description: string }) {
    return <div className="p-card">
        <div className="p-card-content">
            <div className="whitespace-pre-wrap" dangerouslySetInnerHTML={{ __html: description }} />
        </div>
    </div>
}
