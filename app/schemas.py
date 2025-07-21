from pydantic import BaseModel, Field
from typing import List, Optional

class SizeModel(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[SizeModel]

class ProductOut(BaseModel):
    id: str
    name: str
    price: float

class OrderItem(BaseModel):
    productid: str
    qty: int

class OrderCreate(BaseModel):
    userid: str
    items: List[OrderItem]

class OrderOutItem(BaseModel):
    productDetails: ProductOut
    qty: int

class OrderOut(BaseModel):
    id: str
    items: List[OrderOutItem]
    total: float
