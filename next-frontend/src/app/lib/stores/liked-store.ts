import { create } from "zustand";
import { persist } from "zustand/middleware";

type LikedStore = {
    liked: string[];
    addLiked: (id: string) => void;
    removeLiked: (id: string) => void;
}

export const likeStore = create<LikedStore>()(
    persist(
        (set) => ({
            liked: [],
            addLiked: (id: string) => set((state) => ({ liked: [...state.liked, id] })),
            removeLiked: (id: string) => set((state) => ({ liked: state.liked.filter((likedId) => likedId !== id) })),
        }),
        {
            name: 'liked-storage',
        }
    )
);