from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard_stats, name='dashboard_stats'),
    path('dashboard/revenue', views.dashboard_revenue, name='dashboard_revenue'),
    path('dashboard/bookings', views.dashboard_bookings, name='dashboard_bookings'),
    path('dashboard/top-movies', views.dashboard_top_movies, name='dashboard_top_movies'),
]
