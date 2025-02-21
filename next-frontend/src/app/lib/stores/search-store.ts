import { create } from 'zustand';

type SortOption = 'created_at' | 'price' | 'title';
type SortDirection = 'asc' | 'desc';

interface SearchState {
    search: string;
    sortBy: SortOption;
    sortDirection: SortDirection;
    page: number;
    pageSize: number;
    filters: {
        minPrice?: number;
        maxPrice?: number;
        device?: string;
    };
    setSearch: (search: string) => void;
    setSorting: (sortBy: SortOption, direction: SortDirection) => void;
    setFilters: (filters: SearchState['filters']) => void;
    setPage: (page: number) => void;
    setPageSize: (pageSize: number) => void;
}

export const searchStore = create<SearchState>((set) => ({
    search: '',
    sortBy: 'created_at',
    sortDirection: 'desc',
    page: 1,
    pageSize: 10,
    filters: {},
    setSearch: (search) => set({ search }),
    setSorting: (sortBy, sortDirection) => set({ sortBy, sortDirection }),
    setFilters: (filters) => set({ filters }),
    setPage: (page) => set({ page }),
    setPageSize: (pageSize) => set({ pageSize }),
}));