'use client'
import Image from 'next/image'
import { useState } from 'react'

export default function ProductGallery({ images, name }: { images: string[], name: string }) {
    const [selectedImage, setSelectedImage] = useState(images[0])

    if (images.length === 0) {
        return (
            <div className="flex flex-col gap-4">
                <div className="flex justify-center items-center relative h-[40vw] p-card overflow-hidden bg-gray-100">
                    <div className="text-gray-400 text-lg">Pildid puuduvad</div>
                </div>
                <div className="grid grid-cols-4 gap-2">
                    {[...Array(4)].map((_, index) => (
                        <div key={index}
                            className="flex justify-center items-center relative h-[100px] p-card overflow-hidden bg-gray-100">
                        </div>
                    ))}
                </div>
            </div>
        )
    }

    return <div>
        <div className="flex justify-center items-center relative h-[40vw] p-card overflow-hidden">
            <Image
                fill
                src={selectedImage}
                alt={name}
                className="w-full object-contain"
            />
        </div>
        <div className="grid grid-cols-4 gap-2 mt-4">
            {images.map((image: string, index: number) => (
                <div key={index}
                    onClick={() => setSelectedImage(image)}
                    className="flex justify-center items-center relative h-[100px] cursor-pointer p-card overflow-hidden hover:border-1 hover:border-blue-500">
                    <Image
                        fill
                        src={image}
                        alt={`${name} ${index + 2}`}
                        className="w-full object-contain"
                    />
                </div>
            ))}
        </div>
    </div>
}