# Advanced API Project - Django REST Framework

This project demonstrates the implementation of custom views using Django REST Framework's powerful generic views and mixins for efficient CRUD operations on Book and Author models.

## Features

- **Generic Views Implementation**: Complete CRUD operations using DRF generic views
- **Permission System**: Role-based access control with different permission levels
- **Filtering & Search**: Advanced filtering, searching, and ordering capabilities
- **Custom Validation**: Custom serializers with validation logic
- **API Documentation**: Comprehensive endpoint documentation

## Project Structure

```
advanced-api-project/
├── advanced_api_project/
│   ├── settings.py          # Django settings with DRF configuration
│   └── urls.py              # Main URL configuration
├── api/
│   ├── models.py            # Book and Author models
│   ├── serializers.py       # DRF serializers with custom validation
│   ├── views.py             # Generic views implementation
│   ├── urls.py              # API endpoint routing
│   └── management/
│       └── commands/
│           └── populate_data.py  # Sample data creation
└── manage.py
```

## Models

### Author Model
- `name`: CharField(max_length=100)

### Book Model
- `title`: CharField(max_length=200)
- `publication_year`: IntegerField
- `author`: ForeignKey to Author

## API Endpoints

### Book Endpoints

#### Individual Views

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/books/` | List all books | AllowAny |
| GET | `/api/books/<id>/` | Get book details | AllowAny |
| POST | `/api/books/create/` | Create new book | IsAuthenticated |
| PUT/PATCH | `/api/books/<id>/update/` | Update book | IsAuthenticated |
| DELETE | `/api/books/<id>/delete/` | Delete book | IsAuthenticated |

#### Combined Views

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/books/combined/` | List all books | IsAuthenticatedOrReadOnly |
| POST | `/api/books/combined/` | Create new book | IsAuthenticatedOrReadOnly |
| GET | `/api/books/<id>/combined/` | Get book details | IsAuthenticatedOrReadOnly |
| PUT/PATCH | `/api/books/<id>/combined/` | Update book | IsAuthenticatedOrReadOnly |
| DELETE | `/api/books/<id>/combined/` | Delete book | IsAuthenticatedOrReadOnly |

### Author Endpoints

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/authors/` | List all authors | AllowAny |
| GET | `/api/authors/<id>/` | Get author details | AllowAny |

### Utility Endpoints

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/stats/` | Get book statistics | AllowAny |

## Generic Views Implementation

### 1. BookListView (ListAPIView)
- **Purpose**: Retrieve all books with filtering and search
- **Features**: 
  - Filter by author and publication year
  - Search by title and author name
  - Ordering by title, publication year, or author name
  - Pagination (20 items per page)

### 2. BookDetailView (RetrieveAPIView)
- **Purpose**: Retrieve a single book by ID
- **Features**: Read-only access to individual book details

### 3. BookCreateView (CreateAPIView)
- **Purpose**: Create new books
- **Features**:
  - Custom response format with success message
  - Authentication required
  - Custom validation for publication year

### 4. BookUpdateView (UpdateAPIView)
- **Purpose**: Update existing books
- **Features**:
  - Supports both PUT (full update) and PATCH (partial update)
  - Custom response format with success message
  - Authentication required

### 5. BookDeleteView (DestroyAPIView)
- **Purpose**: Delete books
- **Features**:
  - Custom response with confirmation message
  - Authentication required

### 6. Combined Views
- **BookListCreateView**: Combines listing and creation
- **BookRetrieveUpdateDestroyView**: Combines retrieve, update, and delete

## Permission Classes

### Implemented Permissions

1. **AllowAny**: No authentication required (read-only endpoints)
2. **IsAuthenticated**: Authentication required (write operations)
3. **IsAuthenticatedOrReadOnly**: Authentication for write, read for all

### Permission Configuration

```python
# Read-only endpoints (public access)
permission_classes = [permissions.AllowAny]

# Write operations (authenticated users only)
permission_classes = [permissions.IsAuthenticated]

# Mixed permissions (authenticated write, public read)
permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```

## Filtering and Search

### Available Filters
- **Author**: Filter books by author ID
- **Publication Year**: Filter books by publication year
- **Search**: Search in title and author name
- **Ordering**: Sort by title, publication year, or author name

### Example Usage

```bash
# Filter by author
GET /api/books/?author=1

# Filter by publication year
GET /api/books/?publication_year=1997

# Search by title
GET /api/books/?search=Harry

# Order by publication year
GET /api/books/?ordering=-publication_year

# Combined filters
GET /api/books/?author=1&publication_year__gte=1990&ordering=title
```

## Custom Validation

### BookSerializer Validation
- **Publication Year**: Cannot be in the future
- **Custom Response Format**: Success messages for create/update operations

## Authentication

### Available Authentication Methods
- Session Authentication
- Basic Authentication

### Test Credentials
- **Username**: admin
- **Password**: admin123

## Testing the API

### 1. Start the Development Server
```bash
python3 manage.py runserver
```

### 2. Test Read Operations (No Authentication Required)
```bash
# List all books
curl http://localhost:8000/api/books/

# Get book details
curl http://localhost:8000/api/books/1/

# Get statistics
curl http://localhost:8000/api/stats/
```

### 3. Test Write Operations (Authentication Required)
```bash
# Create a new book
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"title": "Test Book", "publication_year": 2023, "author": 1}'

# Update a book
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"title": "Updated Title", "publication_year": 2024, "author": 1}'

# Delete a book
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -u admin:admin123
```

### 4. Test with Browsable API
Visit `http://localhost:8000/api/books/` in your browser to use the interactive API interface.

## Sample Data

The project includes a management command to populate the database with sample data:

```bash
python3 manage.py populate_data
```

This creates sample authors and books for testing purposes.

## Configuration

### Django REST Framework Settings
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

## Key Features Demonstrated

1. **Generic Views**: Efficient CRUD operations with minimal code
2. **Custom Behavior**: Overridden methods for custom responses
3. **Permission System**: Role-based access control
4. **Filtering & Search**: Advanced query capabilities
5. **Validation**: Custom serializer validation
6. **Documentation**: Comprehensive API documentation
7. **Error Handling**: Proper HTTP status codes and error responses

## Dependencies

- Django 5.2+
- Django REST Framework 3.16+
- django-filter 25.2+

## Installation

1. Install dependencies:
```bash
pip install django djangorestframework django-filter
```

2. Run migrations:
```bash
python3 manage.py migrate
```

3. Create superuser:
```bash
python3 manage.py createsuperuser
```

4. Populate sample data:
```bash
python3 manage.py populate_data
```

5. Start development server:
```bash
python3 manage.py runserver
```

This implementation demonstrates best practices for building robust APIs with Django REST Framework using generic views and proper permission management.
