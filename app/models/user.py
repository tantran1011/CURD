from pydantic import BaseModel 

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

class ProductResponse(BaseModel):
    name: str
    price: int
    size: str
    quantity: int
    color: str

class UpCategory(BaseModel):
    name: str
    discount_percentage: int

class CategoryResponse(BaseModel):
    name: str
    discount_percentage: int


"""Order models"""
class CreateOrder(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class InsertOrder(BaseModel):
    id: int

class OrderResponse(BaseModel):
    user_id: int
    product_id: int
    total_price: int
    order_day: str
    quantity: int

