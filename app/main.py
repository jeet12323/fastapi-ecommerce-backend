from fastapi import FastAPI, Query
from app.schemas import ProductCreate, OrderCreate
from app import crud

app = FastAPI()

@app.post("/products", status_code=201)
async def create_product(product: ProductCreate):
    return await crud.create_product(product.dict())

@app.get("/products")
async def list_products(
    name: str = Query(None),
    size: str = Query(None),
    limit: int = Query(10),
    offset: int = Query(0)
):
    products = await crud.list_products(name, size, limit, offset)
    return {
        "data": products,
        "page": {
            "next": offset + limit,
            "limit": limit,
            "previous": max(0, offset - limit)
        }
    }

@app.post("/orders", status_code=201)
async def create_order(order: OrderCreate):
    return await crud.create_order(order.dict())

@app.get("/orders/{user_id}")
async def get_orders(user_id: str, limit: int = 10, offset: int = 0):
    orders = await crud.get_orders(user_id, limit, offset)
    return {
        "data": orders,
        "page": {
            "next": offset + limit,
            "limit": limit,
            "previous": max(0, offset - limit)
        }
    }
