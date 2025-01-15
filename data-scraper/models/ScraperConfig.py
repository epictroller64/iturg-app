


class ScraperConfig:
    """Configuration for the scraper"""
    time_between_pages: int
    retry_count: int
    retry_delay: int
    max_pages: int
    hours_between_updates: int
    time_between_scrapes: int
    page_size: int

    def __init__(self, time_between_scrapes: int = 3600, time_between_pages: int = 0, retry_count: int = 3, retry_delay: int = 5, max_pages: int = 10, hours_between_updates: int = 24, page_size: int = 200):
        self.time_between_scrapes = time_between_scrapes
        self.time_between_pages = time_between_pages
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.max_pages = max_pages
        self.hours_between_updates = hours_between_updates
        self.page_size = page_size
