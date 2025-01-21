'use client'
import Image from 'next/image'
import { useState } from 'react'

export default function ProductGallery({ images, name }: { images: string[], name: string }) {
    const [selectedImage, setSelectedImage] = useState(images[0])
    return <div>
        <div className="flex justify-center items-center relative h-[40vw] p-card">
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
                    className="flex justify-center items-center relative h-[100px] cursor-pointer p-card">
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