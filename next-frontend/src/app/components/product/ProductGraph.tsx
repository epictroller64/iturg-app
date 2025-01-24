'use client'

import { Product } from "@/app/lib/types/Product";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function ProductPriceHistoryGraph({ product }: { product: Product }) {
    return <div className="mt-8 p-card bg-white/80 border border-gray-200/50">
        <div className="p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Hinna ajalugu</h2>
            <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={product.price_history}>
                        <XAxis
                            dataKey="found_at"
                            tickFormatter={(date) => new Date(date).toLocaleDateString()}
                            stroke="#94a3b8"
                            tickLine={false}
                            axisLine={false}
                        />
                        <YAxis
                            dataKey="price"
                            stroke="#94a3b8"
                            tickLine={false}
                            axisLine={false}
                        />
                        <Tooltip
                            labelFormatter={(date) => new Date(date).toLocaleDateString()}
                            formatter={(value) => [`€${value}`, 'Hind']}
                            contentStyle={{
                                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                                border: 'none',
                                borderRadius: '8px',
                                boxShadow: '0 2px 12px rgba(0, 0, 0, 0.08)'
                            }}
                        />
                        <Line
                            type="monotone"
                            dataKey="price"
                            stroke="#0ea5e9"
                            strokeWidth={2.5}
                            dot={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    </div>
}