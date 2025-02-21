'use client'
import Image from "next/image";
import { ProductPreviewDTO } from "../lib/types/ProductPreviewDTO";
import Link from "next/link";
import { FiSmartphone } from "react-icons/fi";
import { FiCpu } from "react-icons/fi";
import { FiServer } from "react-icons/fi";
import { FiTablet } from "react-icons/fi";
import { FiWatch } from "react-icons/fi";
import ProductLike from "./product/ProductLike";



export function ProductCard({ product }: { product: ProductPreviewDTO }) {
    return <div className="p-card h-[75vh] flex flex-col w-[20vw]">
        <div className="relative w-full h-[60%]">
            <ProductImage product={product} />
            <div className="absolute top-5 left-5  text-2xl p-blur-1 font-bold text-black px-2 rounded-full">{product.price} €</div>
            <div className="absolute top-2 right-5"><ProductLike id={product.id} /></div>
            <DaysSinceAdded daysSinceAdded={product.days_since_added} />
        </div>
        <div className="flex flex-col justify-between p-2 h-[40%]">
            <div className="flex flex-col justify-between h-[80%]">
                <Link href={`/product/${product.id}`} className="!text-xl hover:cursor-pointer">{product.name}</Link>
                <div className="h-[1px] bg-gray-200 w-full"></div>
            </div>
            <div className="flex flex-col gap-2 h-[20%]">
                <Platform platform={product.platform} />
                <div className="flex flex-row gap-2 items-center">
                    <Color color={product.color} />
                    <Device device={product.device} />
                    <Chip chip={product.chip} />
                </div>
            </div>
        </div>
    </div>
}


function ProductImage({ product }: { product: ProductPreviewDTO }) {
    if (product.imageUrl.length > 0) {
        return <Image sizes="100vw" src={product.imageUrl} alt={product.name} fill className="object-cover" />
    }
    function pickImageBasedOnDevice(device: string) {
        const deviceLower = device.toLowerCase()
        if (deviceLower.includes("iphone")) {
            return <Image sizes="100vw" src="/generic-product-images/iphone.jpg" alt="iphone" fill className="object-cover" />
        }
        if (deviceLower.includes("macbook")) {
            return <Image sizes="100vw" src="/generic-product-images/macbook.jpeg" alt="macbook" fill className="object-cover" />
        }
        if (deviceLower.includes("ipad")) {
            return <Image sizes="100vw" src="/generic-product-images/ipad.jpg" alt="ipad" fill className="object-cover" />
        }
        return <Image sizes="100vw" src="/generic-product-images/apple.png" alt="apple" fill className="object-cover" />
    }
    return pickImageBasedOnDevice(product.device)
}

// Render product color as a small circle
function Color({ color }: { color: string }) {
    switch (color.toLowerCase()) {
        case "midnight":
            return <div className="w-4 h-4 rounded-full bg-[#1C1C1E]" />
        case "black":
        case "must":
            return <div className="w-4 h-4 rounded-full bg-black" />
        case "space gray":
        case "space grey":
            return <div className="w-4 h-4 rounded-full bg-[#8E8E93]" />
        case "red":
        case "punane":
            return <div className="w-4 h-4 rounded-full bg-red-600" />
        case "gold":
            return <div className="w-4 h-4 rounded-full bg-[#FFD700]" />
        case "white":
        case "valge":
            return <div className="w-4 h-4 rounded-full bg-white border border-gray-200" />
        case "green":
            return <div className="w-4 h-4 rounded-full bg-green-600" />
        case "desert titanium":
            return <div className="w-4 h-4 rounded-full bg-[#DBB59C]" />
        case "black titanium":
            return <div className="w-4 h-4 rounded-full bg-[#2F2F2F]" />
        case "natural titanium":
            return <div className="w-4 h-4 rounded-full bg-[#E3C4A6]" />
        case "pink":
            return <div className="w-4 h-4 rounded-full bg-pink-400" />
        case "blue":
        case "sinine":
            return <div className="w-4 h-4 rounded-full bg-blue-600" />
        case "starlight":
            return <div className="w-4 h-4 rounded-full bg-[#FAF7F2]" />
        case "purple":
            return <div className="w-4 h-4 rounded-full bg-purple-600" />
        default:
            return null
    }
}

function Chip({ chip }: { chip: string }) {
    if (chip) {
        return <div className="text-gray-500 font-bold flex flex-row items-center gap-1"><FiCpu /> {chip}</div>
    }
}

function Device({ device }: { device: string }) {
    if (device.toLowerCase().startsWith("iphone")) {
        return <div className="text-gray-500 font-bold flex flex-row items-center gap-1"><FiSmartphone /> {device}</div>
    }
    if (device.toLowerCase().startsWith("macbook")) {
        return <div className="text-gray-500 font-bold flex flex-row items-center gap-1"><FiServer /> {device}</div>
    }
    if (device.toLowerCase().startsWith("ipad")) {
        return <div className="text-gray-500 font-bold flex flex-row items-center gap-1"><FiTablet /> {device}</div>
    }
    if (device.toLowerCase().startsWith("watch")) {
        return <div className="text-gray-500 font-bold flex flex-row items-center gap-1"><FiWatch /> {device}</div>
    }
    return null
}

function Platform({ platform }: { platform: string }) {
    switch (platform) {
        case "okidoki":
            return <span className="text-green-500 font-bold">Okidoki.ee</span>
        case "soov":
            return <span className="text-blue-500 font-bold">Soov.ee</span>
        case "hinnavaatlus":
            return <span className="text-red-500 font-bold">Hinnavaatlus.ee</span>
        default:
            return <span className="text-gray-500 font-bold">{platform}</span>

    }
}

function DaysSinceAdded({ daysSinceAdded }: { daysSinceAdded: number }) {
    if (daysSinceAdded > 1) {
        return <div className="absolute bottom-2 right-2 text-sm bg-black/50 text-white px-2 py-1 rounded">
            {daysSinceAdded} päeva tagasi
        </div>
    }
    else if (daysSinceAdded === 1) {
        return <div className="absolute bottom-2 right-2 text-sm bg-black/50 text-white px-2 py-1 rounded">
            Eile
        </div>
    }
    else if (daysSinceAdded === 0) {
        return <div className="absolute bottom-2 right-2 text-sm bg-black/50 text-white px-2 py-1 rounded">
            Täna
        </div>
    }
    else {
        return null
    }
}
