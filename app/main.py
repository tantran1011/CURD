from fastapi import FastAPI
from app.routes import auth, product, order, insert
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(product.router, prefix='/products', tags=['products'])
app.include_router(order.router, prefix='/orders', tags=['orders'])
app.include_router(insert.router, prefix='/insert', tags=['insert'])

@app.get('/')
def home():
    return {"Message": "Server is running"}