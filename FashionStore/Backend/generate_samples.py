import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from db import (
    customers_collection, categories_collection, products_collection,
    carts_collection, orders_collection
)

print("Clearing collections...")
customers_collection.delete_many({})
categories_collection.delete_many({})
products_collection.delete_many({})
carts_collection.delete_many({})
orders_collection.delete_many({})

print("Inserting samples...")

customers_collection.insert_one({
  "customer_id": 101,
  "full_name": "Rahul Sharma",
  "email": "rahul@gmail.com",
  "phone": "9876543210",
  "address": "KPHB Colony",
  "city": "Hyderabad",
  "password": "password123" # Added for testing login
})

categories_collection.insert_one({
  "category_id": 201,
  "category_name": "Men's Clothing",
  "description": "Shirts, T-Shirts, Jeans, Jackets"
})

products_collection.insert_one({
  "product_id": 301,
  "product_name": "Slim Fit Denim Jacket",
  "category": "Men's Clothing",
  "brand": "Levi's",
  "size": "L",
  "color": "Blue",
  "price": 2499,
  "stock": 25,
  "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=500"
})

carts_collection.insert_one({
  "cart_id": 401,
  "customer_name": "Rahul Sharma",
  "product_name": "Slim Fit Denim Jacket",
  "quantity": 2,
  "price": 2499,
  "total_price": 4998
})

orders_collection.insert_one({
  "order_id": 501,
  "customer_name": "Rahul Sharma",
  "order_date": "2026-07-15",
  "total_amount": 4998,
  "payment_method": "UPI",
  "payment_status": "Paid",
  "delivery_status": "Processing"
})

print("Sample data generated!")
