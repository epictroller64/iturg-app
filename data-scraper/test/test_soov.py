import pytest
from soov import SoovScraper
from models.ScraperConfig import ScraperConfig
from models.PreScrapedSoovProduct import PreScrapedSoovProduct

@pytest.fixture
def scraper():
    config = ScraperConfig(max_pages=1, retry_count=3, retry_delay=1)
    return SoovScraper(config)

def test_scrape_product_details(scraper: SoovScraper):
    test_product = PreScrapedSoovProduct(
        id="25668253",
        name="Wireless Apple CarPlay (teeb Carplay juhtmevabaks)", 
        href="/25668253-wireless-apple-carplay-teeb-carplay-juhtmevabaks/details.html",
    )
    
    product = scraper.scrape_product_details(test_product)
    
    assert product is not None
    assert product.product_id == "25668253"
    assert product.name == "Wireless Apple CarPlay (teeb Carplay juhtmevabaks)"
    assert isinstance(product.price, float)
    assert isinstance(product.description, str)
    assert isinstance(product.category, list)
    assert isinstance(product.images, list)
    assert isinstance(product.location, str)
    assert isinstance(product.time, str)
    assert isinstance(product.seller_url, str)
    assert product.product_url == "/25668253-wireless-apple-carplay-teeb-carplay-juhtmevabaks/details.html"

def test_scrape_by_keyword(scraper: SoovScraper):
    scraper.scrape_by_keyword("iphone")
    
    assert len(scraper.product_queue) > 0
    
    first_product = scraper.product_queue[0]
    assert isinstance(first_product, PreScrapedSoovProduct)
    assert isinstance(first_product.id, str)
    assert isinstance(first_product.name, str)
    assert isinstance(first_product.href, str)


