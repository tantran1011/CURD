from fastapi import APIRouter, Depends, HTTPException
from app.config import get_db
from app.models.database import Order, OrderItem, Products
from sqlalchemy.orm import Session
from app.models.user import InsertOrder
from datetime import datetime, timedelta


router = APIRouter()

"""Insert by Challenge Requirements"""

@router.post('/')
def insert_order(order: InsertOrder,db: Session = Depends(get_db)):
    # Check if the order exists
    existing_order = db.query(Order).filter(Order.id == order.id).first()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    # Check if the product exists
    existing_product = db.query(Products).filter(Products.id == existing_order.product_id).first()
    
    # Create a new order_items instance
    new_order_items = OrderItem(
        order_id=order.id,
        product_id= existing_order.product_id,
        quantity= existing_order.total_price // existing_product.price,
        price = existing_order.total_price
    )

    # Add the new order_items to the database
    db.add(new_order_items)  
    db.commit()
    db.refresh(new_order_items)
    return {
        "message": "Order items inserted successfully",
        "order_items": new_order_items
    }


@router.get('/{id}')
def get_order_items(db: Session = Depends(get_db)):
    # Get all orders from the database
    order = db.query(OrderItem).filter(OrderItem.order_id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="No order found")
    
    return {"data": order}


@router.get('/')
def get_all_orders(db: Session = Depends(get_db)):
    # Get all orders from the database
    orders = db.query(OrderItem).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    
    return {"data": orders}


"""Calculate the average order value by month"""

@router.get('/average-order-value')
def average_order_value(db: Session = Depends(get_db)):
    # Get all orders from the database
    orders = db.query(Order).all()
    
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    
    results = []
    # Calculate the average order value
    updated_months = set(
        (x.updated_at.year, x.updated_at.month)
        for x in orders
    )
    # Calculate the average price for each month
    for year, month in updated_months:
        month_orders = [x for x in orders if x.updated_at.year == year and x.updated_at.month == month]
        total_price = sum(x.total_price for x in month_orders)
        avg = total_price / len(month_orders) if month_orders else 0

        results.append({
            "month": f"{year}-{str(month).zfill(2)}",
            "average_order_value": avg
        })
    
    return {"data": results}


""" Calculate Churn Rate """

@router.get('/churn-rate')
def churn_rate(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    # Time line 
    today = datetime.now()
    six_months_ago = today - timedelta(days=180)
    twelve_months_ago = today - timedelta(days=365)

    # Users in the last 12 months
    users_with_orders = set(order.user_id for order in orders if order.updated_at >= twelve_months_ago)
    # Users in the last 6 months      
    users_with_recent_orders = set(order.user_id for order in orders if order.updated_at >= six_months_ago)

    # Calculate churn rate
    churned_users = users_with_orders - users_with_recent_orders
    churn_rate = len(churned_users) / len(users_with_orders) * 100 if users_with_orders else 0
    return {
        "churn_rate": churn_rate,
        "churned_users": len(churned_users),
        "total_users": len(users_with_orders)
    }