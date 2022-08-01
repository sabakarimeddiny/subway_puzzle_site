from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('subway_puzzle_app.urls')),
    path('admin/', admin.site.urls),
]