from django.urls import path
from . import views

urlpatterns = [
    path('screens', views.screens_list_create, name='screens_list_create'),
    path('screens/<str:screen_id>', views.screen_detail, name='screen_detail'),
]
