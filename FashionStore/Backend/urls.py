from django.urls import path
import views

urlpatterns = [
    # Customer APIs
    path('customers/add/', views.add_customer),
    path('customers/', views.get_customers),
    path('customers/update/<str:id>/', views.update_customer),
    path('customers/delete/<str:id>/', views.delete_customer),
    
    # Category APIs
    path('categories/add/', views.add_category),
    path('categories/', views.get_categories),
    path('categories/update/<str:id>/', views.update_category),
    path('categories/delete/<str:id>/', views.delete_category),
    
    # Product APIs
    path('products/add/', views.add_product),
    path('products/', views.get_products),
    path('products/update/<str:id>/', views.update_product),
    path('products/delete/<str:id>/', views.delete_product),
    
    # Cart APIs
    path('cart/add/', views.add_cart),
    path('cart/', views.get_carts),
    path('cart/update/<str:id>/', views.update_cart),
    path('cart/delete/<str:id>/', views.delete_cart),
    
    # Order APIs
    path('orders/add/', views.add_order),
    path('orders/', views.get_orders),
    path('orders/update/<str:id>/', views.update_order),
    path('orders/delete/<str:id>/', views.delete_order),
]
