from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'books', BookViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # This will create /api/books/ endpoint
] 