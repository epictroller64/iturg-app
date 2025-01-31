'use client'

function ProductSkeleton() {
    return (
        <div className="p-card h-[75vh] flex flex-col w-[20vw] animate-pulse">
            <div className="relative w-full h-[60%] bg-gray-200">
                <div className="absolute top-5 left-5 h-8 w-20 bg-gray-300 rounded-full"></div>
                <div className="absolute top-2 right-5 h-8 w-8 bg-gray-300 rounded-full"></div>
            </div>
            <div className="flex flex-col justify-between p-2 h-[40%]">
                <div className="flex flex-col justify-between h-[80%]">
                    <div className="h-6 bg-gray-200 w-3/4 rounded"></div>
                    <div className="h-[1px] bg-gray-200 w-full"></div>
                </div>
                <div className="flex flex-col gap-2 h-[20%]">
                    <div className="h-4 bg-gray-200 w-1/4 rounded"></div>
                    <div className="flex flex-row gap-2 items-center">
                        <div className="w-4 h-4 rounded-full bg-gray-200"></div>
                        <div className="h-4 bg-gray-200 w-1/4 rounded"></div>
                        <div className="h-4 bg-gray-200 w-1/4 rounded"></div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ProductSkeleton;
