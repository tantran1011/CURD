from fastapi import APIRouter, Depends, HTTPException
from app.config import get_db
from app.models.database import Order, Products, User
from sqlalchemy.orm import Session
from app.models.schemas import OrderResponse, CreateOrder


router = APIRouter()

@router.post('/', response_model=OrderResponse)
def create_order(order: CreateOrder, db: Session = Depends(get_db)):
    # Check if the user exists
    existing_user = db.query(User).filter(User.id == order.user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the product exists
    existing_product = db.query(Products).filter(Products.id == order.product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Calculate total price
    total_price = existing_product.price * order.quantity
    
    # Create a new order instance
    payment_method = order.payment_method or "CASH"
    new_order = Order(
        user_id=order.user_id,
        product_id=order.product_id,
        total_price=total_price,
        payment_method=payment_method
    )
    
    # Add the new order to the database
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return OrderResponse(
        user_id=new_order.user_id,
        product_id=new_order.product_id,
        total_price=new_order.total_price,
        order_day=new_order.order_day.strftime("%Y-%m-%d %H:%M:%S"),
        quantity=order.quantity,
        payment_method=new_order.payment_method
    )


@router.get('/')
def get_all_orders(db: Session = Depends(get_db)):      
    # Get all orders from the database
    orders = db.query(Order).all()
    
    return {"data": orders}


@router.get('/{order_id}')
def get_order(order_id: int, db: Session = Depends(get_db)):
    # Check if the order exists
    existing_order = db.query(Order).filter(Order.id == order_id).first()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return existing_order


@router.delete('/{order_id}')
def delete_order(order_id: int, db: Session = Depends(get_db)):
    # Check if the order exists
    existing_order = db.query(Order).filter(Order.id == order_id).first()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Delete the order from the database
    db.delete(existing_order)
    db.commit()
    
    return {"Message": "Order deleted successfully",
            "Order Information": existing_order}


@router.put('/{order_id}', response_model=OrderResponse)
def update_order(order_id: int, order: CreateOrder, db: Session = Depends(get_db)):
    # Check if the order exists
    existing_order = db.query(Order).filter(Order.id == order_id).first()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if the user exists
    existing_user = db.query(User).filter(User.id == order.user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the product exists
    existing_product = db.query(Products).filter(Products.id == order.product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update the order details
    existing_order.user_id = order.user_id
    existing_order.product_id = order.product_id
    existing_order.total_price = existing_product.price * order.quantity
    
    db.commit()
    db.refresh(existing_order)
    
    return OrderResponse(
        user_id=existing_order.user_id,
        product_id=existing_order.product_id,
        total_price=existing_order.total_price,
        order_day=existing_order.order_day.strftime("%Y-%m-%d %H:%M:%S"),
        quantity=order.quantity
    )