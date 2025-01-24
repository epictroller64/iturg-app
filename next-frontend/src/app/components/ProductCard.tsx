'use client'
import Image from "next/image";
import { ProductPreviewDTO } from "../lib/types/ProductPreviewDTO";
import Link from "next/link";
import { motion } from "framer-motion";
import { FiSmartphone } from "react-icons/fi";
import { FiCpu } from "react-icons/fi";
import { FiServer } from "react-icons/fi";
import { FiTablet } from "react-icons/fi";
import { FiWatch } from "react-icons/fi";



export function ProductCard({ product }: { product: ProductPreviewDTO }) {
    return <div className="p-card h-[75vh] flex flex-col">
        <div className="relative w-full h-[60%]">
            <Image src={product.imageUrl} alt={product.name} fill className="object-cover" />
            <div className="absolute top-5 left-5  text-2xl p-blur-1 font-bold text-black px-2 rounded-full">{product.price} €</div>
        </div>
        <div className="flex flex-col justify-between p-2 h-[40%]">
            <div className="flex flex-col justify-between h-[80%]">
                <Link href={`/product/${product.product_table_id}`} className="!text-xl hover:cursor-pointer">{product.name}</Link>
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
        default:
            return <span className="text-gray-500 font-bold">{platform}</span>
    }
}


export function ProductCard2({ product }: { product: ProductPreviewDTO }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.3 }}
            className="bg-white rounded-xl shadow-sm overflow-hidden group relative p-card"
        >
            <div className="relative w-full h-56">
                {product.imageUrl && (
                    <div className="overflow-hidden">
                        <motion.div
                            whileHover={{ scale: 1.1 }}
                            transition={{
                                duration: 0.4,
                                ease: "easeOut"
                            }}
                            className="relative w-full h-56"
                        >
                            <Image
                                src={product.imageUrl}
                                alt={product.name}
                                loading="lazy"
                                fill
                                className="object-cover"
                                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                            />
                        </motion.div>
                    </div>
                )}
            </div>
            <div className="p-6">
                <motion.h3
                    className="font-semibold text-xl text-gray-900 mb-2"
                    whileHover={{ x: 5 }}
                    transition={{ duration: 0.2 }}
                >
                    {product.name}
                </motion.h3>
                <div className="space-y-2">
                    <div className="flex justify-between items-center mt-4">
                        <motion.p
                            className="text-2xl font-bold text-blue-600"
                            whileHover={{ scale: 1.1 }}
                        >
                            {product.price} €
                        </motion.p>
                        <motion.div
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <Link
                                href={`/product/${product.product_table_id}`}
                                className="p-btn p-prim-col"
                            >
                                Vaata üksikasju →
                            </Link>
                        </motion.div>
                    </div>
                </div>
            </div>
            <motion.div
                className="absolute bottom-0 left-0 w-full h-1 bg-blue-500"
                initial={{ scaleX: 0 }}
                whileHover={{ scaleX: 1 }}
                transition={{ duration: 0.3 }}
            />
        </motion.div>
    );
}