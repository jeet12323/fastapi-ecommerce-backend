from app.database import products_collection, orders_collection
from bson import ObjectId
from pymongo import ASCENDING
from fastapi import HTTPException

def obj_id_to_str(obj):
    obj["id"] = str(obj["_id"])
    del obj["_id"]
    return obj

async def create_product(data):
    result = await products_collection.insert_one(data)
    return {"id": str(result.inserted_id)}

async def list_products(name=None, size=None, limit=10, offset=0):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size

    cursor = products_collection.find(query).skip(offset).limit(limit)
    products = [obj_id_to_str(p) async for p in cursor]
    return products

async def create_order(data):
    total = 0
    items = []
    for item in data["items"]:
        product = await products_collection.find_one({"_id": ObjectId(item["productid"])})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        price = product["price"]
        total += price * item["qty"]
        items.append(item)

    result = await orders_collection.insert_one({
        "userid": data["userid"],
        "items": items,
        "total": total
    })
    return {"id": str(result.inserted_id)}

async def get_orders(user_id, limit=10, offset=0):
    cursor = orders_collection.find({"userid": user_id}).skip(offset).limit(limit)
    orders = []
    async for order in cursor:
        out_items = []
        for item in order["items"]:
            product = await products_collection.find_one({"_id": ObjectId(item["productid"])})
            out_items.append({
                "productDetails": {
                    "id": str(product["_id"]),
                    "name": product["name"],
                    "price": product["price"]
                },
                "qty": item["qty"]
            })
        orders.append({
            "id": str(order["_id"]),
            "items": out_items,
            "total": order["total"]
        })
    return orders
