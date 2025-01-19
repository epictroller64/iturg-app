from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from repository.product import get_all_products_preview, get_product
from models.Product import Product
from models.ProductPreviewDTO import ProductPreviewDTO
from fastapi import Query

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/api/products", response_model=List[ProductPreviewDTO])
async def get_products(
    search: Optional[str] = Query(None),
    page: Optional[int] = Query(1),
    page_size: Optional[int] = Query(10),
    sort_by: Optional[str] = Query("updated_at"),
    sort_order: Optional[str] = Query("desc"),
):
    try:
        products = get_all_products_preview(search, page, page_size, sort_by, sort_order)
        return products
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    try:
        product = get_product(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
            
        return Product.model_validate(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
