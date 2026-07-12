from rest_framework.decorators import api_view
from rest_framework.response import Response
from db import (
    customers_collection, categories_collection, products_collection,
    carts_collection, orders_collection, serialize_doc
)
from bson.objectid import ObjectId

# ================= CUSTOMER APIs =================
@api_view(['POST'])
def add_customer(request):
    data = request.data
    # Convert string ID if provided to int or just save as is
    res = customers_collection.insert_one(data)
    return Response({"message": "Customer added", "id": str(res.inserted_id)})

@api_view(['GET'])
def get_customers(request):
    customers = list(customers_collection.find())
    return Response([serialize_doc(c) for c in customers])

@api_view(['PUT'])
def update_customer(request, id):
    customers_collection.update_one({"_id": ObjectId(id)}, {"$set": request.data})
    return Response({"message": "Customer updated"})

@api_view(['DELETE'])
def delete_customer(request, id):
    customers_collection.delete_one({"_id": ObjectId(id)})
    return Response({"message": "Customer deleted"})

# ================= CATEGORY APIs =================
@api_view(['POST'])
def add_category(request):
    res = categories_collection.insert_one(request.data)
    return Response({"message": "Category added", "id": str(res.inserted_id)})

@api_view(['GET'])
def get_categories(request):
    categories = list(categories_collection.find())
    return Response([serialize_doc(c) for c in categories])

@api_view(['PUT'])
def update_category(request, id):
    categories_collection.update_one({"_id": ObjectId(id)}, {"$set": request.data})
    return Response({"message": "Category updated"})

@api_view(['DELETE'])
def delete_category(request, id):
    categories_collection.delete_one({"_id": ObjectId(id)})
    return Response({"message": "Category deleted"})

# ================= PRODUCT APIs =================
@api_view(['POST'])
def add_product(request):
    res = products_collection.insert_one(request.data)
    return Response({"message": "Product added", "id": str(res.inserted_id)})

@api_view(['GET'])
def get_products(request):
    products = list(products_collection.find())
    return Response([serialize_doc(p) for p in products])

@api_view(['PUT'])
def update_product(request, id):
    products_collection.update_one({"_id": ObjectId(id)}, {"$set": request.data})
    return Response({"message": "Product updated"})

@api_view(['DELETE'])
def delete_product(request, id):
    products_collection.delete_one({"_id": ObjectId(id)})
    return Response({"message": "Product deleted"})

# ================= CART APIs =================
@api_view(['POST'])
def add_cart(request):
    res = carts_collection.insert_one(request.data)
    return Response({"message": "Cart item added", "id": str(res.inserted_id)})

@api_view(['GET'])
def get_carts(request):
    carts = list(carts_collection.find())
    return Response([serialize_doc(c) for c in carts])

@api_view(['PUT'])
def update_cart(request, id):
    carts_collection.update_one({"_id": ObjectId(id)}, {"$set": request.data})
    return Response({"message": "Cart item updated"})

@api_view(['DELETE'])
def delete_cart(request, id):
    carts_collection.delete_one({"_id": ObjectId(id)})
    return Response({"message": "Cart item deleted"})

# ================= ORDER APIs =================
@api_view(['POST'])
def add_order(request):
    res = orders_collection.insert_one(request.data)
    return Response({"message": "Order added", "id": str(res.inserted_id)})

@api_view(['GET'])
def get_orders(request):
    orders = list(orders_collection.find())
    return Response([serialize_doc(o) for o in orders])

@api_view(['PUT'])
def update_order(request, id):
    orders_collection.update_one({"_id": ObjectId(id)}, {"$set": request.data})
    return Response({"message": "Order updated"})

@api_view(['DELETE'])
def delete_order(request, id):
    orders_collection.delete_one({"_id": ObjectId(id)})
    return Response({"message": "Order deleted"})
