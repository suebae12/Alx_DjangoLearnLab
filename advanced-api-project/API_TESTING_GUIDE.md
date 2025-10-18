# API Testing Guide

## Quick Test Commands

### 1. Start the Server
```bash
cd /Users/marfo/Desktop/ALX_DjangoLearnLab/advanced-api-project
python3 manage.py runserver
```

### 2. Test Read Operations (No Authentication)

```bash
# List all books
curl http://localhost:8000/api/books/

# Get book details
curl http://localhost:8000/api/books/1/

# Get statistics
curl http://localhost:8000/api/stats/

# Search books
curl "http://localhost:8000/api/books/?search=Harry"

# Filter by publication year
curl "http://localhost:8000/api/books/?publication_year=1997"

# Order by publication year (descending)
curl "http://localhost:8000/api/books/?ordering=-publication_year"

# List authors
curl http://localhost:8000/api/authors/

# Get author details
curl http://localhost:8000/api/authors/1/
```

### 3. Test Write Operations (Authentication Required)

```bash
# Create a new book
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"title": "Test Book", "publication_year": 2023, "author": 1}'

# Update a book (PUT - full update)
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"title": "Updated Title", "publication_year": 2024, "author": 1}'

# Update a book (PATCH - partial update)
curl -X PATCH http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"title": "Partially Updated Title"}'

# Delete a book
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -u admin:admin123
```

### 4. Test Combined Views

```bash
# List and Create (combined endpoint)
curl -X GET http://localhost:8000/api/books/combined/
curl -X POST http://localhost:8000/api/books/combined/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"title": "Combined Test Book", "publication_year": 2023, "author": 1}'

# Retrieve, Update, Delete (combined endpoint)
curl -X GET http://localhost:8000/api/books/1/combined/
curl -X PUT http://localhost:8000/api/books/1/combined/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"title": "Combined Updated", "publication_year": 2024, "author": 1}'
curl -X DELETE http://localhost:8000/api/books/1/combined/ \
  -u admin:admin123
```

### 5. Test Permission System

```bash
# Try to create without authentication (should fail)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Unauthorized Book", "publication_year": 2023, "author": 1}'

# Try to update without authentication (should fail)
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Unauthorized Update", "publication_year": 2024, "author": 1}'
```

### 6. Test Validation

```bash
# Try to create book with future publication year (should fail)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"title": "Future Book", "publication_year": 2030, "author": 1}'

# Try to create book with missing required fields (should fail)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"title": "Incomplete Book"}'
```

## Expected Responses

### Successful Creation (201)
```json
{
  "message": "Book created successfully",
  "data": {
    "id": 6,
    "title": "Test Book",
    "publication_year": 2023,
    "author": 1
  }
}
```

### Successful Update (200)
```json
{
  "message": "Book updated successfully",
  "data": {
    "id": 1,
    "title": "Updated Title",
    "publication_year": 2024,
    "author": 1
  }
}
```

### Successful Deletion (204)
```json
{
  "message": "Book \"Test Book\" deleted successfully"
}
```

### Authentication Error (401)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Validation Error (400)
```json
{
  "publication_year": ["Publication year cannot be in the future."]
}
```

### Not Found Error (404)
```json
{
  "detail": "Not found."
}
```

## Browser Testing

Visit these URLs in your browser for interactive testing:

- http://localhost:8000/api/books/ - Browseable API for books
- http://localhost:8000/api/authors/ - Browseable API for authors
- http://localhost:8000/api/stats/ - Statistics endpoint
- http://localhost:8000/admin/ - Django admin (admin/admin123)

## Test Credentials

- **Username**: admin
- **Password**: admin123

## Notes

- All write operations require authentication
- Read operations are publicly accessible
- The API includes pagination (20 items per page)
- Filtering and search are available on list endpoints
- Custom validation prevents future publication years
- Combined views provide RESTful endpoints following Django conventions
