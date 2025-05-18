# 🎒 GREEK TECHNICAL ASSESSMENT

---
 
# ⚙ Techology: 

- FastAPI - Backend
- SQLAlchemy - ORM
- Alembic - Migration
- PostgreSQL - Dadabase
- Python

---

# 📣 NOTE: In this code, from creating tables and inserting to database are carrying out by Python insead of SQL. By serveral reasons:

- Easily performent
- Convienince in changing and adding new attributes in **table**  

---

# 🔥 Question 1: Design a relational database to store all the information contained in the above images such as products, addresses, stores, categories, orders, users

- Due to the small assessment, I create only 5 tables:users (**addresses** will be concaternated in here) , producst, catergories, orders and orderitems (replace for **stores**)
- Start creating database:


```bash
sudo service postgresql start # Start postgresql server

# Create user and database for technical assessment
sudo -u postgres psql

CREATE USER new_username WITH PASSWORD 'new_password'; # Ex: CREATE USER tantran WITH PASSWORD '123456';

CREATE DATABASE new_db_name OWNER new_username; # Ex: CREATE DATABASE tech_db OWNER tantran;

GRANT ALL PRIVILEGES ON DATABASE new_db_name TO new_user;

# Start Alembic
alembic init alembic # Install alembic follow: pip install alembic 

# Change sqlalchemy.url with your DATABASE_API, for Ex: DATABASE_URL="postgresql://tantran:123456@localhost/tech_db"
# Adding base.metadata into alembic > env.py (*)

alembic revision --autogenerate -m "add users, products, categories, orders, orderitems"

alembic upgrade head

# Check database
psql -U tantran -d tech_db -h localhost

tech_db=> \dt
            List of relations
 Schema |      Name       | Type  | Owner 
--------+-----------------+-------+-------
 public | alembic_version | table | geek
 public | categories      | table | geek
 public | order_items     | table | geek
 public | orders          | table | geek
 public | products        | table | geek
 public | users           | table | geek
(6 rows)

tech_db=> \du
                            List of roles
  Role name  |                         Attributes                         
-------------+------------------------------------------------------------ | 
 tantran     | 
 postgres    | Superuser, Create role, Create DB, Replication, Bypass RLS
```

(*) You need to create **Base** to add into env.py to automcatically create tables:
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    province = Column(String)
    district = Column(String)
    commune = Column(String)
    address = Column(String)
    housing_type = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    orders = relationship("Order", back_populates="user")

# To get others, please review in Tech-Assesment-Code/CRUD-main/app/models/database.py
```
---

# 🔥 Question 2: User "assessment", with information as shown, purchased the product "KAPPA Women's Sneakers" in yellow, size 36, quantity 1. Please write a query to insert the order that this person purchased database.

- After completely generating tables, database, to insert data into suitable table, we must run **uvicorn** with FastAPI, and go to : 27.0.0.1:8000/docs#/ to insert 
- Review **auth.py** in Tech-Assesment-Code/CRUD-main/app/routes/auth.py (to Register/Login and adding information to data table **users**)
- Review **product.py** in Tech-Assesment-Code/CRUD-main/app/routes/product.py (To adding new data into table **products**)
- Review **main.py** in Tech-Assesment-Code/CRUD-main/app/main.py

- 🙆‍♂️ Insert user information

```bash
### at main.py
uvicorn app.main:app --reload
```
- Adding user information: 

```yaml
# API - request URL: http://127.0.0.1:8000/auth/register
# Input
{
  "username": "assessment",
  "email": "gu@gmail.com",
  "password": "123456"
}

# Response (successfully created )
{
  "username": "assessment"
}
```

- Updating information, adding address

```yaml
# API - request URL: http://127.0.0.1:8000/auth/update?id=3
# Input
{
  "username": "assessment",
  "email": "gu@gmail.com",
  "phone": "328355333",
  "province": "Bắc Kạn",
  "district": "Ba Bể",
  "commune": "Phúc Lộc",
  "address": "73 Tân Hoà 2",
  "housing_type": "nhà riêng"
}

# Response Body (Sucessfully updated)
{
  "username": "assessment"
}
```

- Results:

```bash
tech_db=> SELECT * FROM users;
 id |    name    |     email      |   phone   | province |  district  | commune  |   address    | housing_type | hashed_password |         created_at         |         updated_at         
----+------------+----------------+-----------+----------+------------+----------+--------------+--------------+-----------------+----------------------------+----------------------------
  3 | assessment | gu@gmail.com   | 328355333 | Băc Kạn  | Ba Bề      | Phúc Lộc | 73 Tân Hoà 2 | Nhà riêng    | 123456          | 2025-05-16 20:36:50.081476 | 2025-05-16 20:40:24.087029
  4 | tantran    | test@gmail.com | 112113114 | HCM      | Bình Thạnh | HCM      | Phan Huy Ôn  | nhà riêng    | 123456          | 2025-05-18 08:04:07.516369 | 2025-05-18 08:14:12.647317
(2 rows)
```

- 📕 Insert products

- It is as same as inserting information for user
- Creating new product

```yaml
# API : http://127.0.0.1:8000/products/1 
# Input
{
  "name": "string", # Name of product
  "price": 0, # Price
  "size": "string", # All size  
  "quantity": 0, # Quantity
  "color": "string", # Color
  "category_id": 0 # And categories Id: 1: Shoes, 2: Shirt, 3: Pants, 4: Dress
}

# Output (Response Body)
product_id = 1
{
  "name": "KAPPA Women's Sneakers",
  "price": 980000,
  "size": "36",
  "quantity": 5,
  "color": "Yellow",
  "category_id": 1
}
```

- Results:

```bash
tech_db=> SELECT * FROM  products;
 id |                     name                      |  price  |         size          | quantity |         color          | category_id |         created_at         |         updated_at         
----+-----------------------------------------------+---------+-----------------------+----------+------------------------+-------------+----------------------------+----------------------------
  2 | Man Gym Pants                                 |   10000 | XL, S                 |        5 | Red, Blue, White, Grey |           3 | 2025-05-16 20:49:54.219462 | 2025-05-17 19:57:48.374653
  3 | Man T-shirt                                   |   50000 | XL                    |        6 | White, Grey            |           2 | 2025-05-17 19:16:49.465361 | 2025-05-17 19:59:08.738793
  4 | Female Maxi Dress H&M                         |   15000 | S                     |        6 | Pink                   |           4 | 2025-05-17 19:20:14.934115 | 2025-05-17 20:00:55.794679
  5 | Polo Regular Fit H&M                          |   15000 | S,M,L,XL              |        8 | Ground, White, Red     |           2 | 2025-05-17 19:21:55.419267 | 2025-05-17 20:02:00.170787
  6 | Nike Air Force 1 '0                           | 2929000 | EU 40, EU 35          |        8 | White, Black           |           1 | 2025-05-17 19:24:24.859784 | 2025-05-17 20:05:35.728396
  7 | Adistar Cushion Sporty & Rich Originals Shoes | 3100000 |  3.5 UK, 4.5 UK, 6 UK |        4 | White                  |           1 | 2025-05-17 19:26:28.021247 | 2025-05-17 20:06:40.264237
  8 | Adidas Rekive Shorts                          |  900000 | S, M, L, XL, 2XL      |        7 | Light Grey             |           3 | 2025-05-17 19:29:48.597033 | 2025-05-17 20:07:44.628202
  9 | Slim-Fit Cargo Pants                          | 1050000 | S, M, L, XL, 2XL      |        7 | Blue                   |           3 | 2025-05-17 19:32:19.946851 | 2025-05-17 20:08:54.45455
  1 | KAPPA Women's Sneakers                        |  980000 | 36                    |        5 | Yellow                 |           1 | 2025-05-16 20:45:37.747313 | 2025-05-17 20:10:56.220576
(9 rows)
```
---

# 🔥 Question 3: Write a query to calculate the average order value (total price of items in an order) for each month in the current year.

- To review funtion: Tech-Assesment-Code/CRUD-main/app/routes/insert.py ( average_order_value)

- Accroding to **orders** table (Created and added at **🔥 question 5.4**):

```bash
id | user_id | product_id | total_price |         order_day          |         created_at         |         updated_at         | payment_method 
----+---------+------------+-------------+----------------------------+----------------------------+----------------------------+----------------
  1 |       3 |          1 |     1960000 | 2025-05-16 21:02:33.273192 | 2025-05-16 21:02:33.273199 | 2025-05-16 21:02:33.273199 | cod
  2 |       3 |          2 |       50000 | 2025-05-16 21:05:10.481813 | 2025-05-16 21:05:10.481821 | 2025-05-16 21:11:43.547913 | cod
  6 |       3 |          2 |       50000 | 2025-05-17 15:24:46.659247 | 2025-05-17 15:24:46.659273 | 2025-05-17 15:24:46.659276 | CASH
  7 |       3 |          2 |       50000 | 2025-05-17 15:26:42.484148 | 2025-05-17 15:26:42.484167 | 2025-05-17 15:26:42.484169 | CASH
  8 |       3 |          1 |      980000 | 2025-05-17 15:28:14.873452 | 2025-05-17 15:28:14.873459 | 2025-05-17 15:28:14.87346  | ONLINE
  9 |       3 |          9 |     1050000 | 2025-05-17 20:15:46.363391 | 2025-05-17 20:15:46.3634   | 2025-05-17 20:15:46.363401 | CASH
 10 |       3 |          1 |     1960000 | 2025-05-17 21:10:11.367386 | 2025-05-17 21:10:11.367422 | 2025-05-17 21:10:11.367425 | ONLINE
(7 rows)
```

- Calculating the average order value by month:

```yaml
# API: http://127.0.0.1:8000/insert/average-order-value
# Output
{
  "data": [
    {
      "month": "year-month",
      "average_order_value": "avg_values (float)"
    }
  ]
}
```

- Results:
```yaml
# Response Body
{
  "data": [
    {
      "month": "2025-05",
      "average_order_value": 871428.5714285715
    }
  ]
}
```

# 🔥 Question 4: Write a query to calculate the churn rate of customers

- To review funtion: Tech-Assesment-Code/CRUD-main/app/routes/insert.py (churn_rate)

- As same as **average order value**, based on **orders** table, calculating the churn-rate

```bash
tech_db=> select * from orders;
 id | user_id | product_id | total_price |         order_day          |         created_at         |         updated_at         | payment_method 
----+---------+------------+-------------+----------------------------+----------------------------+----------------------------+----------------
  1 |       3 |          1 |     1960000 | 2025-05-16 21:02:33.273192 | 2025-05-16 21:02:33.273199 | 2025-05-16 21:02:33.273199 | cod
  2 |       3 |          2 |       50000 | 2025-05-16 21:05:10.481813 | 2025-05-16 21:05:10.481821 | 2025-05-16 21:11:43.547913 | cod
  6 |       3 |          2 |       50000 | 2025-05-17 15:24:46.659247 | 2025-05-17 15:24:46.659273 | 2025-05-17 15:24:46.659276 | CASH
  7 |       3 |          2 |       50000 | 2025-05-17 15:26:42.484148 | 2025-05-17 15:26:42.484167 | 2025-05-17 15:26:42.484169 | CASH
  8 |       3 |          1 |      980000 | 2025-05-17 15:28:14.873452 | 2025-05-17 15:28:14.873459 | 2025-05-17 15:28:14.87346  | ONLINE
  9 |       3 |          9 |     1050000 | 2025-05-17 20:15:46.363391 | 2025-05-17 20:15:46.3634   | 2025-05-17 20:15:46.363401 | CASH
 10 |       3 |          1 |     1960000 | 2025-05-17 21:10:11.367386 | 2025-05-17 21:10:11.367422 | 2025-05-17 21:10:11.367425 | ONLINE
 11 |       4 |          6 |     2929000 | 2025-05-18 08:36:46.773541 | 2025-05-18 08:36:46.773547 | 2025-05-18 08:36:46.773547 | CASH
(8 rows)
```

- Results:

```yaml
# Resonse Body
{
  "churn_rate": 0, # churn_rate = 0 beacause no one leave over 6 months
  "churned_users": 0,
  "total_users": 2
}
```
---

# 🔥 Question 5.1: Fetches a list of all product categories available in the e-commerce platform 

- To review funtion: Tech-Assesment-Code/CRUD-main/app/routes/products.py (get_all_product)

- According to **products** table (showed at question 2)

```yaml
API: http://127.0.0.1:8000/products/all-products/
Response Body:
[
  {
    "price": 10000,
    "id": 2,
    "name": "Man Gym Pants  ",
    "size": "XL, S",
    "color": "Red, Blue, White, Grey",
    "quantity": 5,
    "category_id": 3,
    "created_at": "2025-05-16T20:49:54.219462",
    "updated_at": "2025-05-17T19:57:48.374653"
  },
  {
    "price": 50000,
    "id": 3,
    "name": "Man T-shirt",
    "size": "XL",
    "color": "White, Grey",
    "quantity": 6,
    "category_id": 2,
    "created_at": "2025-05-17T19:16:49.465361",
    "updated_at": "2025-05-17T19:59:08.738793"
  },
  {
    "price": 15000,
    "id": 4,
    "name": "Female Maxi Dress H&M",
    "size": "S",
    "color": "Pink",
    "quantity": 6,
    "category_id": 4,
    "created_at": "2025-05-17T19:20:14.934115",
    "updated_at": "2025-05-17T20:00:55.794679"
  },
  {
    "price": 15000,
    "id": 5,
    "name": "Polo Regular Fit H&M ",
    "size": "S,M,L,XL ",
    "color": "Ground, White, Red ",
    "quantity": 8,
    "category_id": 2,
    "created_at": "2025-05-17T19:21:55.419267",
    "updated_at": "2025-05-17T20:02:00.170787"
  },
  {
    "price": 2929000,
    "id": 6,
    "name": "Nike Air Force 1 '0",
    "size": "EU 40, EU 35",
    "color": "White, Black",
    "quantity": 8,
    "category_id": 1,
    "created_at": "2025-05-17T19:24:24.859784",
    "updated_at": "2025-05-17T20:05:35.728396"
  },
  {
    "price": 3100000,
    "id": 7,
    "name": "Adistar Cushion Sporty & Rich Originals Shoes",
    "size": " 3.5 UK, 4.5 UK, 6 UK",
    "color": "White",
    "quantity": 4,
    "category_id": 1,
    "created_at": "2025-05-17T19:26:28.021247",
    "updated_at": "2025-05-17T20:06:40.264237"
  },
  {
    "price": 900000,
    "id": 8,
    "name": "Adidas Rekive Shorts",
    "size": "S, M, L, XL, 2XL",
    "color": "Light Grey",
    "quantity": 7,
    "category_id": 3,
    "created_at": "2025-05-17T19:29:48.597033",
    "updated_at": "2025-05-17T20:07:44.628202"
  },
  {
    "price": 1050000,
    "id": 9,
    "name": "Slim-Fit Cargo Pants",
    "size": "S, M, L, XL, 2XL",
    "color": "Blue",
    "quantity": 7,
    "category_id": 3,
    "created_at": "2025-05-17T19:32:19.946851",
    "updated_at": "2025-05-17T20:08:54.454550"
  },
  {
    "price": 980000,
    "id": 1,
    "name": "KAPPA Women's Sneakers",
    "size": "36",
    "color": "Yellow",
    "quantity": 5,
    "category_id": 1,
    "created_at": "2025-05-16T20:45:37.747313",
    "updated_at": "2025-05-17T20:10:56.220576"
  }
]
```

- To get all catgories:
```yaml
API: http://127.0.0.1:8000/categories/

Response Body:
{
  "data": [
    {
      "id": 1,
      "name": "Shoes",
      "discount_percentage": 10
    },
    {
      "id": 2,
      "name": "Shirt",
      "discount_percentage": 0
    },
    {
      "id": 3,
      "name": "Pants",
      "discount_percentage": 20
    },
    {
      "id": 4,
      "name": "Dress",
      "discount_percentage": 0
    }
  ]
}
```

---

# 🔥 Question 5.2: Fetches a list of products that belong to a specific category

- To review funtion: Tech-Assesment-Code/CRUD-main/app/routes/categories.py (get_product_by_category)

- **categories** table: 
```bash
id | name  | discount_percentage 
----+-------+---------------------
  1 | Shoes |                  10
  2 | Shirt |                   0
  3 | Pants |                  20
  4 | Dress |                   0
(4 rows)
```

- Geting product based on categoires id:
```yaml
input: category_id

API: http://127.0.0.1:8000/categories/by-category/products?category_id=1

Result (Response body):
[
  {
    "name": "Nike Air Force 1 '0",
    "price": 2929000,
    "size": "EU 40, EU 35",
    "quantity": 8,
    "color": "White, Black",
    "category_id": 1
  },
  {
    "name": "Adistar Cushion Sporty & Rich Originals Shoes",
    "price": 3100000,
    "size": " 3.5 UK, 4.5 UK, 6 UK",
    "quantity": 4,
    "color": "White",
    "category_id": 1
  },
  {
    "name": "KAPPA Women's Sneakers",
    "price": 980000,
    "size": "36",
    "quantity": 5,
    "color": "Yellow",
    "category_id": 1
  }
]
```
---

# 🔥 Question 5.3: Allows users to search (full-text search) for products using various filters and search terms

- To review funtion: Tech-Assesment-Code/CRUD-main/app/routes/products.py (search_product)

- According to **products** table (showed at question 2)

- Using **Query Parameters Methods**

- Search:
```yaml
# Input one of them or both of them:
q:  # ex: pants
min_price, max_price:  # ex: 10000 & 50000
size: # ex: S, XL, EU 40,..
color: # white, red, ...
category_id: # 1,2,3,4
in_stock : # True or Flase :  if in_stock is not None:    if in_stock: query = query.filter(Products.quantity > 0) else: query = query.filter(Products.quantity == 0) 
```

- Results:
```yaml
API: http://127.0.0.1:8000/products/search/?q=pants&min_price=10000&max_price=50000

# Response Body
[
  {
    "name": "Man Gym Pants  ",
    "price": 10000,
    "size": "XL, S",
    "quantity": 5,
    "color": "Red, Blue, White, Grey",
    "category_id": 3
  }
]
```

# 🔥 Question 5.4: Creates a new order and processes payment.

- To review funtion: Tech-Assesment-Code/CRUD-main/app/routes/order.py (create_order)

```yaml
Input (Request Body):
{
  "user_id": 0,   # int 
  "product_id": 0, # int 
  "quantity": 0, # int 
  "payment_method": "CASH" #  Defaut : CASH, CASH or ONLINE 
}

Example:
{
  "user_id": 4,
  "product_id": 9,
  "quantity": 5,
  "payment_method": "ONLINE"
}

Output (Response Body):
{
  "user_id": 4,
  "product_id": 9,
  "total_price": 5250000,
  "order_day": "2025-05-18 09:12:53",
  "quantity": 5,
  "payment_method": "ONLINE"
}
```
- Check **orders** table

```bash
tech_db=> select * from orders;
 id | user_id | product_id | total_price |         order_day          |         created_at         |         updated_at         | payment_method 
----+---------+------------+-------------+----------------------------+----------------------------+----------------------------+----------------
  1 |       3 |          1 |     1960000 | 2025-05-16 21:02:33.273192 | 2025-05-16 21:02:33.273199 | 2025-05-16 21:02:33.273199 | cod
  2 |       3 |          2 |       50000 | 2025-05-16 21:05:10.481813 | 2025-05-16 21:05:10.481821 | 2025-05-16 21:11:43.547913 | cod
  6 |       3 |          2 |       50000 | 2025-05-17 15:24:46.659247 | 2025-05-17 15:24:46.659273 | 2025-05-17 15:24:46.659276 | CASH
  7 |       3 |          2 |       50000 | 2025-05-17 15:26:42.484148 | 2025-05-17 15:26:42.484167 | 2025-05-17 15:26:42.484169 | CASH
  8 |       3 |          1 |      980000 | 2025-05-17 15:28:14.873452 | 2025-05-17 15:28:14.873459 | 2025-05-17 15:28:14.87346  | ONLINE
  9 |       3 |          9 |     1050000 | 2025-05-17 20:15:46.363391 | 2025-05-17 20:15:46.3634   | 2025-05-17 20:15:46.363401 | CASH
 10 |       3 |          1 |     1960000 | 2025-05-17 21:10:11.367386 | 2025-05-17 21:10:11.367422 | 2025-05-17 21:10:11.367425 | ONLINE
 11 |       4 |          6 |     2929000 | 2025-05-18 08:36:46.773541 | 2025-05-18 08:36:46.773547 | 2025-05-18 08:36:46.773547 | CASH
 12 |       4 |          9 |     5250000 | 2025-05-18 09:12:53.244454 | 2025-05-18 09:12:53.244468 | 2025-05-18 09:12:53.24447  | ONLINE  # New Created
(9 rows)
```

---

# 🔥 Question 5.5: Send order confirmation email to user (processed asynchronously with order creation flow).

- Having many methods: Sendgrid, smtplib, Ouath2, ... But in this Technical Assessment, I will use the **BackGroundTasks** to simulate the progress. 

- To review funtion: Tech-Assesment-Code/CRUD-main/app/routes/order.py (create_order) (# Background task to send email confirmation)
```python
background_tasks.add_task(
        send_email_confirmation,
        email=existing_user.email,
        order_id=order.product_id,
        body=[{
            "Product Name": existing_product.name,
            "Quantity": order.quantity,
            "Total Price": total_price
        }]
    )
```

- Send email function (/app/backgroundtasks/bgtasks.py):
```python
def send_email_confirmation(email: str, order_id: str, body:list = []):
    # Simulate sending an email
    print(f"Sending email to {email}")
    x = f"""
    Dear Customer,
    Thank you for your order #{order_id}.
    Your order details are as follows:
    {body}
    """
    print(x)
```

- Results:
```yaml
# When **creating new order**, the confirmation email will be send:

Sending email to test@gmail.com

    Dear Customer,
    Thank you for your order #9.
    Your order details are as follows:
    [{'Product Name': 'Slim-Fit Cargo Pants', 'Quantity': 5, 'Total Price': 5250000}]
    
```

