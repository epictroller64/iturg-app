import { create } from "zustand";

type SearchStore = {
    search: string;
    page: number;
    pageSize: number;
    sortBy: string;
    sortOrder: string;
    setSearch: (search: string) => void;
    setPage: (page: number) => void;
    setPageSize: (pageSize: number) => void;
    setSortBy: (sortBy: string) => void;
    setSortOrder: (sortOrder: string) => void;
}


export const searchStore = create<SearchStore>((set) => ({
    search: "",
    page: 1,
    pageSize: 10,
    sortBy: "updated_at",
    sortOrder: "desc",
    setSearch: (search: string) => set({ search }),
    setPage: (page: number) => set({ page }),
    setPageSize: (pageSize: number) => set({ pageSize }),
    setSortBy: (sortBy: string) => set({ sortBy }),
    setSortOrder: (sortOrder: string) => set({ sortOrder }),
}))