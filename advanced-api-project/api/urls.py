"""
URL configuration for api app.

This file defines the URL patterns for the API endpoints.
Each view is mapped to a specific URL path with appropriate HTTP methods.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets (if needed in the future)
router = DefaultRouter()

# URL patterns for individual views
urlpatterns = [
    # Book CRUD endpoints - Individual views following RESTful conventions
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Book CRUD endpoints - Combined views
    path('books/combined/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/combined/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-retrieve-update-destroy'),
    
    # Author endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Custom endpoints
    path('stats/', views.book_stats, name='book-stats'),
    
    # Include router URLs (for future ViewSets)
    path('', include(router.urls)),
]

# API Documentation URLs (for future use with drf-spectacular or similar)
# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls')),
#     path('schema/', include('drf_spectacular.urls')),
# ]

