import { create } from 'zustand';

type SortOption = 'created_at' | 'price' | 'title';
type SortDirection = 'asc' | 'desc';

interface SearchState {
    search: string;
    sortBy: SortOption;
    sortDirection: SortDirection;
    filters: {
        minPrice?: number;
        maxPrice?: number;
        device?: string;
    };
    setSearch: (search: string) => void;
    setSorting: (sortBy: SortOption, direction: SortDirection) => void;
    setFilters: (filters: SearchState['filters']) => void;
}

export const searchStore = create<SearchState>((set) => ({
    search: '',
    sortBy: 'created_at',
    sortDirection: 'desc',
    filters: {},
    setSearch: (search) => set({ search }),
    setSorting: (sortBy, sortDirection) => set({ sortBy, sortDirection }),
    setFilters: (filters) => set({ filters }),
}));