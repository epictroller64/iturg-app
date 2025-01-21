from fastapi import FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from repository.product import get_all_products_preview, get_product, get_products_by_level2_group
from models.Product import Product
from models.ProductPreviewDTO import ProductPreviewDTO
from fastapi import Query
from dotenv import load_dotenv
from database import setup_database
from repository.product import init_cache

load_dotenv(override=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    await init_cache()
    print('setup complete')
    yield

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/products", response_model=List[ProductPreviewDTO])
async def get_products_handler(
    search: Optional[str] = Query(None),
    page: Optional[int] = Query(1),
    page_size: Optional[int] = Query(10),
    sort_by: Optional[str] = Query("updated_at"),
    sort_order: Optional[str] = Query("desc"),
):
    try:
        products = await get_all_products_preview(search, page, page_size, sort_by, sort_order)
        return products
    except Exception as e:
        print('here')
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product_handler(product_id: int):
    try:
        product = await get_product(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
            
        return Product.model_validate(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filter/products", response_model=List[Product])
async def get_filtered_products_handler(
    field: str = Query(..., description="Filter field (e.g. 'device')"),
    value: str = Query(..., description="Filter value (e.g. 'iphone')")
):
    try:
        products = await get_products_by_level2_group(field, value)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

