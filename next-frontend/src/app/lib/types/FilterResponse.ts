
export type FilterResponse<T> = {
    page: number;
    page_size: number;
    max_pages: number;
    data: T[];
}


