import pytest
import uuid
from datetime import datetime
from models.Product import Product
from models.ProductPreviewDTO import ProductPreviewDTO
from repository.product import (
    get_all_products_preview,
    get_product,
    upsert_product,
    get_similar_products
)



@pytest.fixture
async def sample_product():
    return Product(
        id=1,
        product_id="13092936",
        platform="okidoki",
        name="Apple Magic Trackpad 2",
        description="Test Description",
        category=["Elektroonika", "Arvutiseadmed", "Klaviatuurid, hiired ja sisendseadmed", "Joistikud, mängupuldid"],
        brand="Apple",
        seller_url="https://okidoki.ee/product/apple-magic-trackpad-2",
        product_url="https://okidoki.ee/product/apple-magic-trackpad-2",
        location="Tartu",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        images=["https://okidoki.ee/image/product/apple-magic-trackpad-2"],
        price_history=[]
    )

@pytest.fixture
async def sample_product_preview():
    return ProductPreviewDTO(
        id=1,
        platform_product_id="13092936",
        name="Apple Magic Trackpad 2",
        price=70.0,
        imageUrl="https://okidoki.ee/image/product/apple-magic-trackpad-2",
        platform="okidoki",
        device="",
        chip="",
        ram="",
        screen_size="",
        generation="",
        storage="",
        color="",
        status="",
        year="",
        watch_mm=""
    )

@pytest.mark.asyncio
async def test_get_all_products_preview():
    products = await get_all_products_preview()
    assert isinstance(products, list)
    if len(products) > 0:
        assert isinstance(products[0], ProductPreviewDTO)

    products = await get_all_products_preview(search="iphone")
    assert isinstance(products, list)

    products = await get_all_products_preview(page=1, page_size=5)
    assert len(products) <= 5

@pytest.mark.asyncio
async def test_get_product():
    product = await get_product(1, prefer_cache=False)
    if product:
        assert isinstance(product, Product)
        assert product.id == 1

    #invalid id
    product = await get_product(-1)
    assert product is None

@pytest.mark.asyncio
async def test_get_product_cached():
    product = await get_product(1, prefer_cache=True)
    if product:
        assert isinstance(product, Product)
        assert product.id == 1

@pytest.mark.asyncio
async def test_upsert_product():
    test_product = Product(
        product_id="test-{}".format(uuid.uuid4()),
        platform="test",
        name="Test Product",
        description="Test Description",
        category=["Electronics"],
        brand="Test Brand",
        seller_url="http://test.com/seller",
        product_url="http://test.com/product",
        location="Test Location",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        images=["http://test.com/image.jpg"],
        price_history=[]
    )

    # test insert
    product_id = await upsert_product(test_product)
    assert product_id is not None

    # test update
    test_product.name = "Updated Test Product"
    updated_id = await upsert_product(test_product)
    assert updated_id == product_id

    updated_product = await get_product(product_id, prefer_cache=False)
    assert updated_product.name == "Updated Test Product"

@pytest.mark.asyncio
async def test_get_similar_products():
    # test with valid product ID
    similar_products = await get_similar_products(1)
    assert isinstance(similar_products, list)
    if len(similar_products) > 0:
        assert isinstance(similar_products[0], ProductPreviewDTO)

    # test with invalid product ID
    similar_products = await get_similar_products(-1)
    assert len(similar_products) == 0