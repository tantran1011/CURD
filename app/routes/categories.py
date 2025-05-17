from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import UpCategory, CategoryResponse, ProductResponse
from app.config import get_db
from app.models.database import Category, Products
from sqlalchemy.orm import Session

router = APIRouter()


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


@router.get('/')
def get_all_categories(db: Session = Depends(get_db)):
    # Get all categories from the database
    categories = db.query(Category).all()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    
    return {"data": categories}


@router.get('/by-category/products', response_model=list[ProductResponse])
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
