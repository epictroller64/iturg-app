'use client'
import { searchStore } from "../lib/stores/search-store";


export default function FilterControls() {
    const { filters, setFilters } = searchStore();

    return (
        <div className="flex flex-col gap-4 p-4 bg-white rounded-lg shadow">
            <h3 className="font-semibold">Filtreeri</h3>

            <div className="space-y-2">
                <p className="text-sm text-gray-600">Hind</p>
                <div className="flex gap-2 items-center">
                    <input
                        type="number"
                        placeholder="Min"
                        className="p-form-text w-24"
                        value={filters.minPrice || ''}
                        onChange={(e) => setFilters({
                            ...filters,
                            minPrice: e.target.value ? Number(e.target.value) : undefined
                        })}
                    />
                    <span>-</span>
                    <input
                        type="number"
                        placeholder="Max"
                        className="p-form-text w-24"
                        value={filters.maxPrice || ''}
                        onChange={(e) => setFilters({
                            ...filters,
                            maxPrice: e.target.value ? Number(e.target.value) : undefined
                        })}
                    />
                </div>
            </div>

            <div className="space-y-2">
                <p className="text-sm text-gray-600">Kategooria</p>
                <select
                    className="p-form-select w-full"
                    value={filters.device || ''}
                    onChange={(e) => setFilters({
                        ...filters,
                        device: e.target.value || undefined
                    })}
                >
                    <option value="">Kõik kategooriad</option>
                    {devices.map((device) => (
                        <option key={device} value={device}>{device}</option>
                    ))}
                </select>
            </div>
        </div>
    );
}



const devices = [
    'Watch',
    'iPhone 16 Pro',
    'iPhone',
    'iPhone 6 Plus',
    'Airpods 3',
    'Watch SE',
    'Airpods',
    'iPad',
    'iPad Mini 6',
    'iPhone 13 Pro',
    'MacBook Pro',
    'iPhone 12 Pro',
    'iPhone 11',
    'iPhone 12',
    'iPhone 12 Pro Max',
    'iPhone 16',
    'iPhone 5',
    'iPhone 4',
    'iPhone 13',
    'MacBook Air',
    'MacBook',
    'iPhone 14',
    'iPhone 14 Pro Max',
    'Airpods Pro',
    'iPhone 11 Pro Max',
    'iPhone 16 Pro Max',
    'iPhone 15 Pro Max',
    'iPhone 7',
    'iPad Pro',
    'iPad Mini',
    'iMac',
    'iPhone 15',
    'iPhone 14 Plus',
    'iPhone 13 Pro Max',
    'iPad Air',
    'Apple TV',
    'iPad Mini 5',
    'Airpods 2',
    'iPhone 14 Pro',
    'iPhone 15 Pro',
    'iPhone 6',
    'iPhone 15 Plus',
    'iPhone 11 Pro',
    'iPad Air 5',
    'iPhone 8 Plus',
    'iPhone 20',
    'iPad Pro 11',
    'iPad Mini 4',
    'iPad Air 2',
    'iPad Pro 12',
    'iPhone 8',
    'iPad Pro 10',
    'iPad Pro 9',
    'iPhone 16 Plus',
    'iPad Pro 2024',
    'iPhone 3',
    'iPad Air 10',
    'iPhone 7 Plus',
    'iPhone 2',
    'iPhone 14 Pro Max Plus',
    'iPhone 16 Pro Max Plus',
    'iPhone 10',
    'iPhone 13 Pro Plus',
    'iPhone 8 Pro Max',
    'iPad Air 4',
    'iPad Mini 2',
    'iPad Air 1',
    'iPad Mini 3',
    'iPad Air 11',
    'iPad Pro 2018'
]