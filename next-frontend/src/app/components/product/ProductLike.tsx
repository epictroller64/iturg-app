'use client'
import { likeStore } from "@/app/lib/stores/liked-store";
import { useEffect, useState } from "react";
import { HiHeart } from "react-icons/hi";
import { motion, AnimatePresence } from "framer-motion";

export default function ProductLike({ id }: { id: string }) {
    const { liked, addLiked, removeLiked } = likeStore()
    const isLiked = liked.includes(id);
    const [isLoaded, setIsLoaded] = useState(false);
    useEffect(() => {
        setIsLoaded(true);
    }, []);

    const handleClick = () => {
        if (isLiked) {
            removeLiked(id);
        } else {
            addLiked(id);
        }
    };
    if (!isLoaded) {
        return null;
    }
    return (
        <div className="group relative">
            <motion.button
                onClick={handleClick}
                className="p-2 rounded-full hover:bg-gray-100 transition-colors duration-200"
                aria-label={isLiked ? "Remove from favorites" : "Add to favorites"}
                whileTap={{ scale: 0.9 }}
            >
                <motion.div
                    initial={false}
                    animate={isLiked ? {
                        scale: [1, 1.2, 1],
                        transition: { duration: 0.3 }
                    } : {
                        scale: 1
                    }}
                >
                    <HiHeart
                        className={`w-12 h-12 ${isLiked ? 'text-red-500' : 'text-gray-400'}`}
                    />
                </motion.div>
            </motion.button>
            <AnimatePresence>
                <motion.div
                    className="absolute z-20 -top-10 left-1/2 -translate-x-1/2 bg-gray-800 text-white px-3 py-1 rounded-md text-sm whitespace-wrap"
                    initial={{ opacity: 0, y: 10 }}
                    whileHover={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    transition={{ duration: 0.2 }}
                >
                    Lisa lemmikutesse
                </motion.div>
            </AnimatePresence>
        </div>
    );
}