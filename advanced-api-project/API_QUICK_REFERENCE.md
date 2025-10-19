# API Quick Reference Card

## Book Endpoints

### Basic CRUD Operations
```
GET    /api/books/                    # List all books
GET    /api/books/<id>/               # Get book details
POST   /api/books/create/             # Create book (authenticated)
PUT    /api/books/update/<id>/        # Update book (authenticated)
DELETE /api/books/delete/<id>/        # Delete book (authenticated)
```

### Combined Endpoints
```
GET    /api/books/combined/           # List books (public) / Create book (authenticated)
GET    /api/books/<id>/combined/      # Get book details (public) / Update/Delete (authenticated)
PUT    /api/books/<id>/combined/      # Update book (authenticated)
DELETE /api/books/<id>/combined/      # Delete book (authenticated)
```

## Filtering Options

### Title Filtering
```
?title=Harry                         # Partial match
?title_exact=Harry Potter            # Exact match
?title_startswith=Harry              # Starts with
```

### Author Filtering
```
?author__name=Rowling                # Author name partial match
?author__name_exact=J.K. Rowling     # Exact author name
?author=1                            # Author ID
```

### Publication Year Filtering
```
?publication_year=1997               # Exact year
?publication_year__gte=1997          # Year >= 1997
?publication_year__lte=2000          # Year <= 2000
?publication_year__gt=1995           # Year > 1995
?publication_year__lt=2000           # Year < 2000
?publication_year_range_min=1900&publication_year_range_max=2000  # Range
```

### ID Filtering
```
?id=1                                # Single book ID
?id__in=1,2,3                        # Multiple book IDs
```

### Combined Search
```
?search=Potter                       # Search in title and author name
```

## Search Functionality
```
?search=Harry                        # DRF SearchFilter (searches title and author__name)
```

## Ordering Options
```
?ordering=title                      # Order by title (ascending)
?ordering=-title                     # Order by title (descending)
?ordering=publication_year           # Order by publication year (ascending)
?ordering=-publication_year          # Order by publication year (descending)
?ordering=author__name               # Order by author name (ascending)
?ordering=-author__name              # Order by author name (descending)
?ordering=id                         # Order by ID (ascending)
?ordering=-id                        # Order by ID (descending)
```

## Author Endpoints

### Basic Operations
```
GET    /api/authors/                 # List all authors
GET    /api/authors/<id>/            # Get author details
```

### Author Filtering
```
?name=Rowling                        # Author name partial match
?name_exact=J.K. Rowling             # Exact author name
?name_startswith=J.K.                # Author name starts with
?books_count=2                       # Authors with exactly 2 books
?books_count__gte=2                  # Authors with >= 2 books
?books_count__lte=5                  # Authors with <= 5 books
```

### Author Ordering
```
?ordering=name                       # Order by name (ascending)
?ordering=-name                      # Order by name (descending)
?ordering=books_count                # Order by book count (ascending)
?ordering=-books_count               # Order by book count (descending)
```

## Custom Endpoints

### Statistics
```
GET    /api/stats/                   # Book and author statistics
```

### Advanced Search
```
GET    /api/search/                  # Advanced search with multiple criteria
```

Query Parameters:
- `q`: Search term
- `year_min`: Minimum publication year
- `year_max`: Maximum publication year
- `author_id`: Author ID filter
- `limit`: Maximum results (default: 20)

Example:
```
GET /api/search/?q=Harry&year_min=1997&limit=5
```

### Author Analytics
```
GET    /api/authors/analytics/       # Author analytics and statistics
```

Query Parameters:
- `min_books`: Minimum number of books (default: 1)
- `sort_by`: Sort by 'name', 'book_count', or 'latest_book' (default: 'name')

Example:
```
GET /api/authors/analytics/?min_books=2&sort_by=book_count
```

## Combined Query Examples

### Complex Filtering
```
GET /api/books/?title=Harry&publication_year__gte=1997&author__name=Rowling&ordering=-publication_year
```

### Search with Filters
```
GET /api/books/?search=Potter&publication_year__gte=1990&ordering=title
```

### Range Filtering
```
GET /api/books/?publication_year_range_min=1900&publication_year_range_max=2000&ordering=-publication_year
```

### Multiple ID Filtering
```
GET /api/books/?id__in=1,2,3&ordering=title
```

## Authentication

### Test Credentials
- **Username**: admin
- **Password**: admin123

### Authentication Required Endpoints
- POST `/api/books/create/`
- PUT `/api/books/update/<id>/`
- PATCH `/api/books/update/<id>/`
- DELETE `/api/books/delete/<id>/`
- POST `/api/books/combined/`
- PUT `/api/books/<id>/combined/`
- PATCH `/api/books/<id>/combined/`
- DELETE `/api/books/<id>/combined/`

### Public Access Endpoints
- All GET endpoints for books and authors
- Statistics and analytics endpoints
- Search endpoints

## Response Format

### Paginated List Response
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/books/?page=2",
    "previous": null,
    "results": [...]
}
```

### Single Object Response
```json
{
    "id": 1,
    "title": "Book Title",
    "publication_year": 1997,
    "author": 1
}
```

### Custom Search Response
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

## Error Responses

### Authentication Required (401)
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Not Found (404)
```json
{
    "detail": "Not found."
}
```

### Validation Error (400)
```json
{
    "publication_year": ["Publication year cannot be in the future."]
}
```
