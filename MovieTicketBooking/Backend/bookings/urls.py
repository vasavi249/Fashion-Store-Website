from django.urls import path
from . import views

urlpatterns = [
    path('bookings', views.bookings_list_create, name='bookings_list_create'),
    path('bookings/<str:booking_id>', views.booking_detail, name='booking_detail'),
    path('seats/<str:show_id>', views.get_seats, name='get_seats'),
    path('seats/book', views.book_seats, name='book_seats'),
]
