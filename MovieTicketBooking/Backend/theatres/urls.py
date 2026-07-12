from django.urls import path
from . import views

urlpatterns = [
    path('theatres', views.theatres_list_create, name='theatres_list_create'),
    path('theatres/<str:theatre_id>', views.theatre_detail, name='theatre_detail'),
]
