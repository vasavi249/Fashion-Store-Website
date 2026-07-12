from django.urls import path
from . import views

urlpatterns = [
    path('movies', views.movies_list_create, name='movies_list_create'),
    path('movies/<str:movie_id>', views.movie_detail, name='movie_detail'),
    path('movies/search', views.movie_search, name='movie_search'),
    path('movies/genre/<str:genre>', views.movie_by_genre, name='movie_by_genre'),
    path('movies/language/<str:language>', views.movie_by_language, name='movie_by_language'),
]
