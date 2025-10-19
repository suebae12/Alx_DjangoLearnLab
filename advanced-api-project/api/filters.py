# advanced-api-project/api/filters.py

import django_filters
from django.db import models
from .models import Book, Author

# Enhanced custom filter set for Book model
# Provides comprehensive filtering options for the Book API
class BookFilter(django_filters.FilterSet):
    # Title filtering with multiple options
    title = django_filters.CharFilter(lookup_expr='icontains', help_text='Filter by book title (partial match)')
    title_exact = django_filters.CharFilter(field_name='title', lookup_expr='exact', help_text='Filter by exact book title')
    title_startswith = django_filters.CharFilter(field_name='title', lookup_expr='startswith', help_text='Filter by book title starting with')
    
    # Author filtering
    author__name = django_filters.CharFilter(lookup_expr='icontains', help_text='Filter by author name (partial match)')
    author__name_exact = django_filters.CharFilter(field_name='author__name', lookup_expr='exact', help_text='Filter by exact author name')
    author = django_filters.NumberFilter(help_text='Filter by author ID')
    
    # Publication year filtering with range options
    publication_year = django_filters.NumberFilter(help_text='Filter by exact publication year')
    publication_year__gte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte', help_text='Filter by publication year greater than or equal to')
    publication_year__lte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte', help_text='Filter by publication year less than or equal to')
    publication_year__gt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gt', help_text='Filter by publication year greater than')
    publication_year__lt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lt', help_text='Filter by publication year less than')
    
    # Range filtering for publication years
    publication_year_range = django_filters.RangeFilter(field_name='publication_year', help_text='Filter by publication year range (e.g., ?publication_year_range_min=1900&publication_year_range_max=2000)')
    
    # ID filtering
    id = django_filters.NumberFilter(help_text='Filter by book ID')
    id__in = django_filters.BaseInFilter(field_name='id', help_text='Filter by multiple book IDs (comma-separated)')
    
    # Combined search field (searches both title and author name)
    search = django_filters.CharFilter(method='filter_search', help_text='Search in both title and author name')
    
    def filter_search(self, queryset, name, value):
        """Custom filter method for searching in multiple fields"""
        if value:
            return queryset.filter(
                models.Q(title__icontains=value) | 
                models.Q(author__name__icontains=value)
            )
        return queryset

    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains', 'startswith'],
            'author__name': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte', 'gt', 'lt'],
            'author': ['exact'],
            'id': ['exact', 'in'],
        }


# Custom filter for Author model
class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='Filter by author name (partial match)')
    name_exact = django_filters.CharFilter(field_name='name', lookup_expr='exact', help_text='Filter by exact author name')
    name_startswith = django_filters.CharFilter(field_name='name', lookup_expr='startswith', help_text='Filter by author name starting with')
    
    # Filter by number of books
    books_count = django_filters.NumberFilter(method='filter_books_count', help_text='Filter by number of books')
    books_count__gte = django_filters.NumberFilter(method='filter_books_count_gte', help_text='Filter by number of books greater than or equal to')
    books_count__lte = django_filters.NumberFilter(method='filter_books_count_lte', help_text='Filter by number of books less than or equal to')
    
    def filter_books_count(self, queryset, name, value):
        """Filter by exact number of books"""
        if value is not None:
            return queryset.annotate(book_count=models.Count('books')).filter(book_count=value)
        return queryset
    
    def filter_books_count_gte(self, queryset, name, value):
        """Filter by number of books >= value"""
        if value is not None:
            return queryset.annotate(book_count=models.Count('books')).filter(book_count__gte=value)
        return queryset
    
    def filter_books_count_lte(self, queryset, name, value):
        """Filter by number of books <= value"""
        if value is not None:
            return queryset.annotate(book_count=models.Count('books')).filter(book_count__lte=value)
        return queryset

    class Meta:
        model = Author
        fields = ['name', 'id']


# Models import already done at the top
