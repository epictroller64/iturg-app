'use client'
import Image from "next/image";
import { ProductPreviewDTO } from "../lib/types/ProductPreviewDTO";
import Link from "next/link";
import { motion } from "framer-motion";

export function ProductCard({ product }: { product: ProductPreviewDTO }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.3 }}
            key={product.id}
            className="bg-white rounded-xl shadow-sm overflow-hidden group relative"
        >
            <div className="relative w-full h-56 overflow-hidden">
                {product.imageUrl && (
                    <motion.div
                        whileHover={{ scale: 1.1 }}
                        transition={{ duration: 0.4 }}
                    >
                        <Image
                            src={product.imageUrl}
                            alt={product.name}
                            loading="lazy"
                            fill
                            className="w-full h-56 object-cover"
                        />
                    </motion.div>
                )}
                <div className="absolute top-3 right-3">
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm"
                    >
                        Used
                    </motion.div>
                </div>
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
                                href={`/product/${product.id}`}
                                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-full text-sm font-medium transition-colors duration-200"
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