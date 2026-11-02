# Step 2: path parameters, query parameters and automatic validation.
# Run:  fastapi dev examples/02_params.py
# Try:  /products/3            -> ok
#       /products/abc          -> 422, "abc" is not an integer
#       /products?max_price=500&in_stock=true&limit=2
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

PRODUCTS = [
    {"id": 1, "name": "Keyboard", "price": 1200, "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 450, "in_stock": True},
    {"id": 3, "name": "Monitor", "price": 9800, "in_stock": False},
    {"id": 4, "name": "USB cable", "price": 199, "in_stock": True},
]


@app.get("/products/{product_id}")
def get_product(product_id: Annotated[int, Path(ge=1)]):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products")
def list_products(
    max_price: float | None = None,
    in_stock: bool = False,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    result = PRODUCTS
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    if in_stock:
        result = [p for p in result if p["in_stock"]]
    return result[:limit]
