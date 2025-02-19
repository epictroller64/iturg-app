from fastapi import FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from repository.product import get_all_products_preview, get_product, get_products_by_ids, get_products_by_level2_group, get_similar_products
from fastapi import Query
from dotenv import load_dotenv
from models.dto.ProductPreviewDTO import ProductPreviewDTO
from models.database.Product import Product
from database import setup_database
from repository.product import init_cache
from services.postviews import increment_post_view


load_dotenv(override=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    #await init_cache()
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


@app.get("/api/products/search", response_model=List[ProductPreviewDTO])
async def get_products_handler(
    search: Optional[str] = Query(None),
    page: Optional[int] = Query(1),
    page_size: Optional[int] = Query(10),
    sort_by: Optional[str] = Query("updated_at"),
    sort_order: Optional[str] = Query("desc"),
    filters: Optional[str] = Query(None, description="JSON string of filters, e.g. '{\"device\":\"iphone\",\"color\":\"red\"}'")
):
    try:
        products = await get_all_products_preview(search, page, page_size, sort_by, sort_order, filters)
        return products
    except Exception as e:
        print('Error in get_products_handler:', e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products/id/{product_table_id}", response_model=Product)
async def get_product_handler(product_table_id: int):
    try:
        product = await get_product(product_table_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
            
        return Product.model_validate(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/api/products/ids", response_model=List[ProductPreviewDTO])
async def get_products_by_ids_handler(ids: List[int] = Query(...)):
    try:
        products = await get_products_by_ids([str(id) for id in ids])
        return products
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/similar/products/{product_table_id}", response_model=List[ProductPreviewDTO])
async def get_similar_products_handler(product_table_id: int):
    try:
        products = await get_similar_products(product_table_id)
        return products
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filter/products", response_model=List[ProductPreviewDTO])
async def get_filtered_products_handler(
    field: str = Query(..., description="Filter field (e.g. 'device')"),
    value: str = Query(..., description="Filter value (e.g. 'iphone')")
):
    try:
        products = await get_products_by_level2_group(field, value)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products/increment-post-view/{product_table_id}")
async def increment_post_view_handler(product_table_id: int):
    try:
        await increment_post_view(product_table_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

