from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.user import UpProduct, ProductResponse, UpCategory, CategoryResponse
from app.config import get_db
from app.models.database import Products, Category
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
        payment_method=new_product.payment_method
    )


@router.get('/', response_model=list[ProductResponse])
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


@router.get('/')
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
    )


@router.put('/{product_id}', response_model=ProductResponse)
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


    db.commit()
    db.refresh(existing_product)

    return ProductResponse(
        name=existing_product.name,
        price=existing_product.price,
        size=existing_product.size,
        quantity=existing_product.quantity,
        color=existing_product.color,
    )


@router.delete('/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Check if the product exists
    existing_product = db.query(Products).filter(Products.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete the product from the database
    db.delete(existing_product)
    db.commit()

    return {"detail": "Product deleted successfully"}


"""Category routes for adding, getting, updating, and deleting categories"""

@router.post('/', response_model=CategoryResponse)
def add_category(category: UpCategory, db: Session = Depends(get_db)):
    # Check if the category already exists
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    # Create a new category instance
    new_category = Category(
        name=category.name,
        discount_percentage=category.discount_percentage
    )
    # Add the new category to the database
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return CategoryResponse(
        name=new_category.name,
        discount_percentage=new_category.discount_percentage
    )


@router.get('/', response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    # Get all categories from the database
    categories = db.query(Category).all()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    
    return [CategoryResponse(
        name=category.name,
        discount_percentage=category.discount_percentage
    ) for category in categories]


@router.get('/', response_model=list[ProductResponse])
def get_product_by_category(category_id: int, db: Session = Depends(get_db)):
    # Check if the category exists
    existing_category = db.query(Category).filter(Category.id == category_id).first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Get all products in the specified category
    products = db.query(Products).filter(Products.category_id == category_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found in this category")
    
    return [ProductResponse(
        name=product.name,
        price=product.price,
        size=product.size,
        quantity=product.quantity,
        color=product.color,
        category_id=product.category_id
    ) for product in products]


@router.get('/{category_id}', response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    # Check if the category exists
    existing_category = db.query(Category).filter(Category.id == category_id).first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return CategoryResponse(
        name=existing_category.name,
        discount_percentage=existing_category.discount_percentage
    )


@router.put('/{category_id}', response_model=CategoryResponse)
def update_category(category_id: int, category: UpCategory, db: Session = Depends(get_db)):
    # Check if the category exists
    existing_category = db.query(Category).filter(Category.id == category_id).first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Update the category details
    existing_category.name = category.name
    existing_category.discount_percentage = category.discount_percentage

    db.commit()
    db.refresh(existing_category)

    return CategoryResponse(
        name=existing_category.name,
        discount_percentage=existing_category.discount_percentage
    )


@router.delete('/{category_id}')
def delete_category(category_id: int, db: Session = Depends(get_db)):
    # Check if the category exists
    existing_category = db.query(Category).filter(Category.id == category_id).first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Delete the category from the database
    db.delete(existing_category)
    db.commit()

    return {"detail": "Category deleted successfully"}
