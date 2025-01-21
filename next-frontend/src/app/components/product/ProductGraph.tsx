'use client'

import { Product } from "@/app/lib/types/Product";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function ProductGraph({ product }: { product: Product }) {
    return <div className="mt-8 p-card">
        <div className="p-card-content">
            <h2 className="text-2xl font-bold mb-4">Hinna ajalugu</h2>
            <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={product.price_history}>
                        <XAxis
                            dataKey="found_at"
                            tickFormatter={(date) => new Date(date).toLocaleDateString()}
                        />
                        <YAxis dataKey="price" />
                        <Tooltip
                            labelFormatter={(date) => new Date(date).toLocaleDateString()}
                            formatter={(value) => [`€${value}`, 'Hind']}
                        />
                        <Line
                            type="monotone"
                            dataKey="price"
                            stroke="#2563eb"
                            strokeWidth={2}
                            dot={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    </div>
}