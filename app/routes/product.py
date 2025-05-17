from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.schemas import UpProduct, ProductResponse
from app.config import get_db
from app.models.database import Products
from sqlalchemy.orm import Session

router = APIRouter()

"""Product routes for adding, getting, updating, and deleting products"""

@router.post('/', response_model=ProductResponse)
def add_product(product: UpProduct, db: Session = Depends(get_db)):
    # Check if the product already exists
    existing_product = db.query(Products).filter(Products.name == product.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists")
    # Create a new product instance
    new_product = Products(
        name=product.name,
        price=product.price,
        size=product.size,
        quantity=product.quantity,
        color=product.color,
        category_id=product.category_id
    )
    # Add the new product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return ProductResponse(
        name=new_product.name,
        price=new_product.price,
        size=new_product.size,
        quantity=new_product.quantity,
        color=new_product.color,
        category_id=new_product.category_id
    )


@router.get('/search/', response_model=list[ProductResponse])
def search_product(db: Session = Depends(get_db), q: str = Query(None), min_price: int = Query(None), max_price: int = Query(None),
                   size: str = Query(None), color: str = Query(None), category_id: int = Query(None), in_stock: bool = Query(None),):

    query = db.query(Products)
    if q:
        query = query.filter(Products.name.ilike(f"%{q}%"))
    if min_price:
        query = query.filter(Products.price >= min_price)
    if max_price:
        query = query.filter(Products.price <= max_price)
    if size:
        query = query.filter(Products.size.ilike(f"%{size}%"))
    if color:
        query = query.filter(Products.color.ilike(f"%{color}%"))
    if category_id:
        query = query.filter(Products.category_id == category_id)
    if in_stock is not None:    
        if in_stock:
            query = query.filter(Products.quantity > 0)
        else:
            query = query.filter(Products.quantity == 0) 

    return query.all()


@router.get('/all-products/')
def get_all_products(db: Session = Depends(get_db)):
    # Get all products from the database
    products = db.query(Products).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    
    return products


@router.get('/{product_id}', response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    # Check if the product exists
    existing_product = db.query(Products).filter(Products.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return ProductResponse(
        name=existing_product.name,
        price=existing_product.price,
        size=existing_product.size,
        quantity=existing_product.quantity,
        color=existing_product.color,
        category_id=existing_product.category_id
    )


@router.put('/update/products', response_model=ProductResponse)
def update_product(product_id: int, product: UpProduct, db: Session = Depends(get_db)):
    # Check if the product exists
    existing_product = db.query(Products).filter(Products.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update the product details
    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.size = product.size
    existing_product.quantity = product.quantity
    existing_product.color = product.color
    existing_product.category_id = product.category_id


    db.commit()
    db.refresh(existing_product)

    return ProductResponse(
        name=existing_product.name,
        price=existing_product.price,
        size=existing_product.size,
        quantity=existing_product.quantity,
        color=existing_product.color,
        category_id=existing_product.category_id
    )


@router.delete('/delete/products')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Check if the product exists
    existing_product = db.query(Products).filter(Products.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete the product from the database
    db.delete(existing_product)
    db.commit()

    return {"detail": "Product deleted successfully"}
