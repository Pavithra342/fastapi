from datetime import datetime
from uuid import uuid4
from typing import List, Optional
import string
import random

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

# In-memory databases
products_db = {}
reviews_db = {}
offers_db = {}

def generate_alphanumeric_id():
    """
    Generate an alphanumeric ID.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

class Product(BaseModel):
    """
    Represents a product with basic information.
    """
    product_id: str = Field(default_factory=generate_alphanumeric_id)
    name: str
    description: str
    price: float
    created_by: str
    created_date: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None
    updated_date: Optional[datetime] = None

class ProductReview(BaseModel):
    """
    Represents a review for a product.
    """
    review_id: str = Field(default_factory=lambda: str(uuid4()))
    product_id: str
    review: str
    rating: int
    created_by: str
    created_date: datetime = Field(default_factory=datetime.utcnow)

class Offer(BaseModel):
    """
    Represents an offer related to a product.
    """
    offer_id: str = Field(default_factory=lambda: str(uuid4()))
    product_id: str
    description: str
    discount: float
    created_by: str
    created_date: datetime = Field(default_factory=datetime.utcnow)

@app.post("/products", response_model=Product)
def create_product(product: Product):
    """
    Create a new product.
    """
    products_db[product.product_id] = product
    return product

@app.get("/products/{product_id}", response_model=Product)
def fetch_product(product_id: str):
    """
    Fetch a product by its ID.
    """
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: str, product: Product):
    """
    Update attributes of an existing product.
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Retrieve existing product and update its fields
    updated_product = products_db[product_id]
    updated_product.name = product.name
    updated_product.description = product.description
    updated_product.price = product.price
    updated_product.updated_by = product.updated_by
    updated_product.updated_date = datetime.utcnow()
    
    products_db[product_id] = updated_product
    return updated_product

@app.post("/products/{product_id}/reviews", response_model=ProductReview)
def create_product_review(product_id: str, review: ProductReview):
    """
    Post a review for a specific product.
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    review.product_id = product_id
    reviews_db[review.review_id] = review
    return review

@app.post("/products/{product_id}/offers", response_model=Offer)
def create_offer(product_id: str, offer: Offer):
    """
    Post an offer related to a product.
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    offer.product_id = product_id
    offers_db[offer.offer_id] = offer
    return offer

@app.get("/products/{product_id}/reviews", response_model=List[ProductReview])
def list_product_reviews(product_id: str, skip: int = Query(0, ge=0), limit: int = Query(10, gt=0)):
    """
    List reviews for a specific product with pagination support.
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    reviews = [review for review in reviews_db.values() if review.product_id == product_id]
    return reviews[skip: skip + limit]

@app.delete("/products/{product_id}")
def remove_old_product(product_id: str):
    """
    Remove a product from the database.
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    del products_db[product_id]
    return {"message": "Product removed successfully"}
