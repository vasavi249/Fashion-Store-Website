from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/', include('movies.urls')),
    path('api/', include('theatres.urls')),
    path('api/', include('screens.urls')),
    path('api/', include('shows.urls')),
    path('api/', include('bookings.urls')),
    path('api/', include('dashboard.urls')),
]
