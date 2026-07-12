from django.urls import path
from . import views

urlpatterns = [
    path('shows', views.shows_list_create, name='shows_list_create'),
    path('shows/<str:show_id>', views.show_detail, name='show_detail'),
    path('shows/movie/<str:movie_id>', views.shows_by_movie, name='shows_by_movie'),
    path('shows/theatre/<str:theatre_id>', views.shows_by_theatre, name='shows_by_theatre'),
]
