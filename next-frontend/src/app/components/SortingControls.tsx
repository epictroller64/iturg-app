'use client'

import { searchStore } from "../lib/stores/search-store";

export default function SortingControls() {
    const { sortBy, sortDirection, setSorting } = searchStore();

    return (
        <div className="flex gap-4 items-center">
            <select
                className="p-form-select"
                value={`${sortBy}-${sortDirection}`}
                onChange={(e) => {
                    const [newSortBy, newDirection] = e.target.value.split('-');
                    setSorting(
                        newSortBy as 'updated_at' | 'price' | 'title',
                        newDirection as 'asc' | 'desc'
                    );
                }}
            >
                <option value="updated_at-desc">Uuemad ees</option>
                <option value="updated_at-asc">Vanemad ees</option>
                <option value="price-asc">Hind kasvav</option>
                <option value="price-desc">Hind kahanev</option>
                <option value="title-asc">Nimi A-Z</option>
                <option value="title-desc">Nimi Z-A</option>
            </select>
        </div>
    );
}
