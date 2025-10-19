# Advanced Filtering, Searching, and Ordering Implementation Guide

## Overview

This document provides comprehensive documentation for the enhanced filtering, searching, and ordering capabilities implemented in the advanced-api-project. The implementation provides powerful query capabilities that allow API consumers to efficiently filter, search, and order book data based on various criteria.

## Implementation Architecture

### 1. Custom Filter Classes (`api/filters.py`)

#### BookFilter
A comprehensive filter class that provides multiple filtering options for the Book model:

```python
class BookFilter(django_filters.FilterSet):
    # Title filtering with multiple options
    title = django_filters.CharFilter(lookup_expr='icontains')
    title_exact = django_filters.CharFilter(field_name='title', lookup_expr='exact')
    title_startswith = django_filters.CharFilter(field_name='title', lookup_expr='startswith')
    
    # Author filtering
    author__name = django_filters.CharFilter(lookup_expr='icontains')
    author__name_exact = django_filters.CharFilter(field_name='author__name', lookup_expr='exact')
    author = django_filters.NumberFilter()
    
    # Publication year filtering with range options
    publication_year = django_filters.NumberFilter()
    publication_year__gte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    publication_year__lte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    publication_year__gt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gt')
    publication_year__lt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lt')
    
    # Range filtering for publication years
    publication_year_range = django_filters.RangeFilter(field_name='publication_year')
    
    # ID filtering
    id = django_filters.NumberFilter()
    id__in = django_filters.BaseInFilter(field_name='id')
    
    # Combined search field
    search = django_filters.CharFilter(method='filter_search')
```

#### AuthorFilter
Enhanced filter class for Author model with book count filtering:

```python
class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    name_exact = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    name_startswith = django_filters.CharFilter(field_name='name', lookup_expr='startswith')
    
    # Filter by number of books
    books_count = django_filters.NumberFilter(method='filter_books_count')
    books_count__gte = django_filters.NumberFilter(method='filter_books_count_gte')
    books_count__lte = django_filters.NumberFilter(method='filter_books_count_lte')
```

### 2. Enhanced Views (`api/views.py`)

#### BookListView
Enhanced with comprehensive filtering, searching, and ordering capabilities:

```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter  # Custom filter class
    search_fields = ['title', 'author__name', 'author__name__icontains']
    ordering_fields = ['title', 'publication_year', 'author__name', 'id', 'author']
    ordering = ['title']  # Default ordering
```

## API Endpoints and Usage Examples

### 1. Book Filtering Endpoints

#### Basic Filtering

**Filter by Title (Partial Match)**
```bash
GET /api/books/?title=Harry
```

**Filter by Exact Title**
```bash
GET /api/books/?title_exact=Harry Potter and the Philosopher's Stone
```

**Filter by Title Starting With**
```bash
GET /api/books/?title_startswith=Harry
```

**Filter by Author Name (Partial Match)**
```bash
GET /api/books/?author__name=Rowling
```

**Filter by Exact Author Name**
```bash
GET /api/books/?author__name_exact=J.K. Rowling
```

**Filter by Author ID**
```bash
GET /api/books/?author=1
```

#### Publication Year Filtering

**Filter by Exact Publication Year**
```bash
GET /api/books/?publication_year=1997
```

**Filter by Publication Year >= Value**
```bash
GET /api/books/?publication_year__gte=1997
```

**Filter by Publication Year <= Value**
```bash
GET /api/books/?publication_year__lte=2000
```

**Filter by Publication Year > Value**
```bash
GET /api/books/?publication_year__gt=1995
```

**Filter by Publication Year < Value**
```bash
GET /api/books/?publication_year__lt=2000
```

**Filter by Publication Year Range**
```bash
GET /api/books/?publication_year_range_min=1900&publication_year_range_max=2000
```

#### ID Filtering

**Filter by Book ID**
```bash
GET /api/books/?id=1
```

**Filter by Multiple Book IDs**
```bash
GET /api/books/?id__in=1,2,3
```

#### Combined Search

**Search in Both Title and Author Name**
```bash
GET /api/books/?search=Potter
```

### 2. Search Functionality

#### DRF SearchFilter

**Search in Title**
```bash
GET /api/books/?search=Harry
```

**Search in Author Name**
```bash
GET /api/books/?search=Rowling
```

#### Advanced Search Endpoint

**Custom Search with Multiple Criteria**
```bash
GET /api/search/?q=Harry&year_min=1997&year_max=2000&author_id=1&limit=10
```

Query Parameters:
- `q`: Search term (searches in title and author name)
- `year_min`: Minimum publication year
- `year_max`: Maximum publication year
- `author_id`: Filter by specific author
- `limit`: Maximum number of results (default: 20)

### 3. Ordering Functionality

#### Order by Title
```bash
GET /api/books/?ordering=title          # Ascending
GET /api/books/?ordering=-title         # Descending
```

#### Order by Publication Year
```bash
GET /api/books/?ordering=publication_year      # Ascending
GET /api/books/?ordering=-publication_year     # Descending
```

#### Order by Author Name
```bash
GET /api/books/?ordering=author__name          # Ascending
GET /api/books/?ordering=-author__name         # Descending
```

#### Order by Book ID
```bash
GET /api/books/?ordering=id                    # Ascending
GET /api/books/?ordering=-id                   # Descending
```

### 4. Combined Filtering, Searching, and Ordering

#### Complex Queries

**Filter + Search + Order**
```bash
GET /api/books/?title=Harry&publication_year__gte=1997&ordering=-publication_year
```

**Multiple Filters + Ordering**
```bash
GET /api/books/?author__name=Rowling&publication_year__gte=1990&publication_year__lte=2000&ordering=title
```

**Search + Filter + Order**
```bash
GET /api/books/?search=Potter&publication_year__gte=1997&ordering=-publication_year
```

### 5. Author Filtering and Analytics

#### Author Filtering

**Filter by Author Name**
```bash
GET /api/authors/?name=Rowling
```

**Filter by Exact Author Name**
```bash
GET /api/authors/?name_exact=J.K. Rowling
```

**Filter by Authors with Minimum Book Count**
```bash
GET /api/authors/?books_count__gte=2
```

**Filter by Authors with Maximum Book Count**
```bash
GET /api/authors/?books_count__lte=5
```

#### Author Analytics

**Get Author Analytics**
```bash
GET /api/authors/analytics/?min_books=1&sort_by=book_count
```

Query Parameters:
- `min_books`: Minimum number of books (default: 1)
- `sort_by`: Sort by 'name', 'book_count', or 'latest_book' (default: 'name')

### 6. Statistics and Analytics

#### Book Statistics
```bash
GET /api/stats/
```

Returns comprehensive statistics including:
- Total books and authors
- Books by publication year
- Top authors by book count
- Recent books

## Implementation Features

### 1. Performance Optimizations

#### Query Optimization
- **select_related('author')**: Reduces database queries for author information
- **prefetch_related('author__books')**: Optimizes queries for related book data
- **annotate()**: Adds computed fields like book counts

#### Database Efficiency
```python
def get_queryset(self):
    queryset = super().get_queryset()
    return queryset.select_related('author').prefetch_related('author__books')
```

### 2. Custom Filter Methods

#### Combined Search Filter
```python
def filter_search(self, queryset, name, value):
    """Custom filter method for searching in multiple fields"""
    if value:
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(author__name__icontains=value)
        )
    return queryset
```

#### Book Count Filters
```python
def filter_books_count(self, queryset, name, value):
    """Filter by exact number of books"""
    if value is not None:
        return queryset.annotate(book_count=Count('books')).filter(book_count=value)
    return queryset
```

### 3. Error Handling and Validation

#### Input Validation
- Automatic type conversion for numeric filters
- Proper handling of empty or invalid parameters
- Graceful fallbacks for malformed queries

#### Query Safety
- Protection against SQL injection through Django ORM
- Proper escaping of user input
- Validation of filter parameters

## Testing Examples

### 1. Basic Filtering Tests

```bash
# Test title filtering
curl "http://localhost:8000/api/books/?title=Harry"

# Test publication year filtering
curl "http://localhost:8000/api/books/?publication_year__gte=1997"

# Test author filtering
curl "http://localhost:8000/api/books/?author__name=Rowling"
```

### 2. Combined Query Tests

```bash
# Test multiple filters
curl "http://localhost:8000/api/books/?title=Harry&publication_year__gte=1997&ordering=-publication_year"

# Test search with filters
curl "http://localhost:8000/api/books/?search=Potter&author__name=Rowling"

# Test range filtering
curl "http://localhost:8000/api/books/?publication_year_range_min=1900&publication_year_range_max=2000"
```

### 3. Advanced Search Tests

```bash
# Test custom search endpoint
curl "http://localhost:8000/api/search/?q=Harry&year_min=1997&limit=5"

# Test author analytics
curl "http://localhost:8000/api/authors/analytics/?min_books=2&sort_by=book_count"
```

## Response Formats

### 1. Standard List Response
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Harry Potter and the Philosopher's Stone",
            "publication_year": 1997,
            "author": 1
        }
    ]
}
```

### 2. Custom Search Response
```json
{
    "search_term": "Harry",
    "filters_applied": {
        "year_min": "1997",
        "year_max": null,
        "author_id": null
    },
    "results_count": 3,
    "books": [...]
}
```

### 3. Statistics Response
```json
{
    "total_books": 4,
    "total_authors": 3,
    "recent_books_by_year": [...],
    "top_authors_by_book_count": [...],
    "recent_books": [...]
}
```

## Best Practices

### 1. Query Optimization
- Use `select_related()` for foreign key relationships
- Use `prefetch_related()` for reverse foreign key relationships
- Add database indexes for frequently filtered fields

### 2. Filter Design
- Provide multiple lookup types (exact, icontains, startswith)
- Include range filters for numeric fields
- Implement custom filter methods for complex queries

### 3. API Design
- Use consistent naming conventions
- Provide clear help text for filter parameters
- Support both simple and complex query patterns

### 4. Documentation
- Document all available filter options
- Provide usage examples
- Include response format specifications

## Conclusion

The enhanced filtering, searching, and ordering implementation provides a powerful and flexible API interface that allows clients to efficiently query and manipulate book data. The implementation follows Django REST Framework best practices and provides excellent performance through query optimization and proper database indexing.

Key benefits:
- **Flexibility**: Multiple filtering options for different use cases
- **Performance**: Optimized queries with proper database relationships
- **Usability**: Clear API interface with comprehensive documentation
- **Scalability**: Efficient implementation that can handle large datasets
- **Maintainability**: Clean, well-documented code with proper separation of concerns
