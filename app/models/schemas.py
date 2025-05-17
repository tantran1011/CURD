from pydantic import BaseModel
from enum import Enum 

"""User models for registration and login."""
class Register(BaseModel):
    username: str
    email: str
    password: str


class Login(BaseModel):
    username: str
    password: str


class UpdateUser(BaseModel):
    username: str
    email: str
    phone: str
    province: str
    district: str
    commune: str
    address: str
    housing_type: str
 

class UserResponse(BaseModel):
    username: str


"""Products and Category models"""
class UpProduct(BaseModel):
    name: str 
    price: int 
    size: str 
    quantity: int 
    color: str
    category_id: int

class ProductResponse(BaseModel):
    name: str
    price: int
    size: str
    quantity: int
    color: str
    category_id: int

class UpCategory(BaseModel):
    name: str
    discount_percentage: int

class CategoryResponse(BaseModel):
    name: str
    discount_percentage: int


"""Order models"""

class PaymentMethod(str, Enum):
    CASH = "CASH"
    ONLINE = "ONLINE"

class CreateOrder(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    payment_method: PaymentMethod = PaymentMethod.CASH

class InsertOrder(BaseModel):
    id: int

class OrderResponse(BaseModel):
    user_id: int
    product_id: int
    total_price: int
    order_day: str
    quantity: int
    payment_method: str