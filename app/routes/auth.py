from fastapi import APIRouter, Depends, HTTPException
from app.config import get_db
from app.models.database import User
from app.models.user import Register, Login, UserResponse, UpdateUser
from sqlalchemy.orm import Session


router = APIRouter()

@router.post('/register', response_model=UserResponse)  
def register_user(user: Register, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.name == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create a new user
    new_user = User(
        name=user.username,
        email=user.email,
        hashed_password=user.password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(username=new_user.name)


@router.post('/login', response_model=UserResponse)
def login_user(user: Login, db: Session = Depends(get_db)):
    # Check if the user exists
    existing_user = db.query(User).filter(User.name == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Check if the password is correct
    if existing_user. hashed_password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return UserResponse(username=existing_user.name)


@router.put('/update', response_model=UserResponse)
def update_user(user: UpdateUser, db: Session = Depends(get_db)):
    # Check if the user exists
    existing_user = db.query( User).filter(User.name == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Update user details
    existing_user.email = user.email
    existing_user.phone = user.phone
    existing_user.province = user.province
    existing_user.district = user.district
    existing_user.commune = user.commune
    existing_user.address = user.address
    existing_user.housing_type = user.housing_type

    db.commit()
    db.refresh(existing_user)

    return UserResponse(username=existing_user.name)


@router.delete('/delete/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Check if the user exists
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Delete the user
    db.delete(existing_user)
    db.commit()
    
    return {"message": "User deleted successfully"}


@router.get('/user/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Check if the user exists
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    return existing_user


@router.get('/users')
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users

