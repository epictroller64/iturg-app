from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
from repository.product import get_all_products_preview, get_product
from models.Product import Product
from models.ProductPreviewDTO import ProductPreviewDTO

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
async def get_products():
    try:
        products = get_all_products_preview()
        return [ProductPreviewDTO.model_validate(product) for product in products] 
    except Exception as e:
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
