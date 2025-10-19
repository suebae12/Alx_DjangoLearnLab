from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Q, Max
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .filters import BookFilter, AuthorFilter


class BookListView(generics.ListAPIView):
    """
    Enhanced ListView for retrieving all books with comprehensive filtering, searching, and ordering capabilities.
    
    Filtering Options:
    - title: Filter by book title (partial match)
    - title_exact: Filter by exact book title
    - title_startswith: Filter by book title starting with
    - author__name: Filter by author name (partial match)
    - author__name_exact: Filter by exact author name
    - author: Filter by author ID
    - publication_year: Filter by exact publication year
    - publication_year__gte: Filter by publication year >= value
    - publication_year__lte: Filter by publication year <= value
    - publication_year__gt: Filter by publication year > value
    - publication_year__lt: Filter by publication year < value
    - publication_year_range_min/max: Filter by publication year range
    - id: Filter by book ID
    - id__in: Filter by multiple book IDs (comma-separated)
    - search: Search in both title and author name
    
    Search Fields:
    - title: Search in book titles
    - author__name: Search in author names
    
    Ordering Fields:
    - title, -title: Order by title (ascending/descending)
    - publication_year, -publication_year: Order by publication year
    - author__name, -author__name: Order by author name
    - id, -id: Order by book ID
    
    Example Usage:
    - GET /api/books/?title=Harry&publication_year__gte=1990&ordering=-publication_year
    - GET /api/books/?search=Potter&author__name=Rowling
    - GET /api/books/?publication_year_range_min=1900&publication_year_range_max=2000
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated read access
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter  # Use custom filter class instead of filterset_fields
    search_fields = ['title', 'author__name', 'author__name__icontains']
    ordering_fields = ['title', 'publication_year', 'author__name', 'id', 'author']
    ordering = ['title']  # Default ordering
    
    def get_queryset(self):
        """
        Enhance the queryset with additional annotations for advanced filtering.
        """
        queryset = super().get_queryset()
        return queryset.select_related('author').prefetch_related('author__books')


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    Provides read-only access to individual Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated read access


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Customize the creation process.
        This method is called when a new Book instance is created.
        """
        # You can add custom logic here, such as:
        # - Setting additional fields
        # - Logging the creation
        # - Sending notifications
        serializer.save()
        
    def create(self, request, *args, **kwargs):
        """
        Override create method to customize the response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Book created successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    Supports both PUT (full update) and PATCH (partial update).
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Customize the update process.
        This method is called when a Book instance is updated.
        """
        # You can add custom logic here, such as:
        # - Logging the update
        # - Sending notifications
        # - Tracking changes
        serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Override update method to customize the response.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
            
        return Response(
            {
                'message': 'Book updated successfully',
                'data': serializer.data
            }
        )


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        """
        Customize the deletion process.
        This method is called when a Book instance is deleted.
        """
        # You can add custom logic here, such as:
        # - Logging the deletion
        # - Soft delete implementation
        # - Sending notifications
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to customize the response.
        """
        instance = self.get_object()
        book_title = instance.title  # Store title for response
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'Book "{book_title}" deleted successfully'
            },
            status=status.HTTP_204_NO_CONTENT
        )


class BookListCreateView(generics.ListCreateAPIView):
    """
    Combined ListView and CreateView for books with enhanced filtering capabilities.
    Provides both listing and creation functionality in a single endpoint.
    
    Supports all the same filtering, searching, and ordering options as BookListView.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter  # Use custom filter class
    search_fields = ['title', 'author__name', 'author__name__icontains']
    ordering_fields = ['title', 'publication_year', 'author__name', 'id', 'author']
    ordering = ['title']
    
    def get_queryset(self):
        """
        Enhance the queryset with additional annotations for advanced filtering.
        """
        queryset = super().get_queryset()
        return queryset.select_related('author').prefetch_related('author__books')


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Combined DetailView, UpdateView, and DeleteView for individual books.
    Provides retrieve, update, and delete functionality in a single endpoint.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Additional views for demonstration purposes
class AuthorListView(generics.ListAPIView):
    """
    Enhanced ListView for retrieving all authors with their books.
    
    Filtering Options:
    - name: Filter by author name (partial match)
    - name_exact: Filter by exact author name
    - name_startswith: Filter by author name starting with
    - books_count: Filter by exact number of books
    - books_count__gte: Filter by number of books >= value
    - books_count__lte: Filter by number of books <= value
    
    Search Fields:
    - name: Search in author names
    
    Ordering Fields:
    - name, -name: Order by author name (ascending/descending)
    - id, -id: Order by author ID
    
    Example Usage:
    - GET /api/authors/?name=Orwell&books_count__gte=2
    - GET /api/authors/?search=Rowling
    """
    queryset = Author.objects.annotate(books_count=Count('books')).all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuthorFilter  # Use custom filter class
    search_fields = ['name']
    ordering_fields = ['name', 'id', 'books_count']
    ordering = ['name']
    
    def get_queryset(self):
        """
        Enhance the queryset with book count annotations.
        """
        queryset = super().get_queryset()
        return queryset.annotate(books_count=Count('books')).prefetch_related('books')


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author with their books.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


# Custom API endpoints for demonstration
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def book_stats(request):
    """
    Custom endpoint to get comprehensive statistics about books.
    """
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    
    # Get books by publication year
    books_by_year = Book.objects.values('publication_year').annotate(
        count=Count('id')
    ).order_by('-publication_year')[:5]
    
    # Get authors with book counts
    authors_with_counts = Author.objects.annotate(
        book_count=Count('books')
    ).values('name', 'book_count').order_by('-book_count')[:5]
    
    # Get recent books
    recent_books = Book.objects.select_related('author').order_by('-publication_year')[:5]
    recent_books_data = BookSerializer(recent_books, many=True).data
    
    return Response({
        'total_books': total_books,
        'total_authors': total_authors,
        'recent_books_by_year': list(books_by_year),
        'top_authors_by_book_count': list(authors_with_counts),
        'recent_books': recent_books_data
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def book_search(request):
    """
    Advanced search endpoint for books with multiple search criteria.
    
    Query Parameters:
    - q: Search term (searches in title and author name)
    - year_min: Minimum publication year
    - year_max: Maximum publication year
    - author_id: Filter by specific author
    - limit: Maximum number of results (default: 20)
    """
    search_term = request.GET.get('q', '')
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    author_id = request.GET.get('author_id')
    limit = int(request.GET.get('limit', 20))
    
    queryset = Book.objects.select_related('author').all()
    
    # Apply search term
    if search_term:
        queryset = queryset.filter(
            Q(title__icontains=search_term) | 
            Q(author__name__icontains=search_term)
        )
    
    # Apply year filters
    if year_min:
        queryset = queryset.filter(publication_year__gte=year_min)
    if year_max:
        queryset = queryset.filter(publication_year__lte=year_max)
    
    # Apply author filter
    if author_id:
        queryset = queryset.filter(author_id=author_id)
    
    # Order by publication year descending and limit results
    queryset = queryset.order_by('-publication_year')[:limit]
    
    serializer = BookSerializer(queryset, many=True)
    
    return Response({
        'search_term': search_term,
        'filters_applied': {
            'year_min': year_min,
            'year_max': year_max,
            'author_id': author_id,
        },
        'results_count': len(serializer.data),
        'books': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def author_analytics(request):
    """
    Analytics endpoint for authors with various statistics.
    
    Query Parameters:
    - min_books: Minimum number of books (default: 1)
    - sort_by: Sort by 'name', 'book_count', or 'latest_book' (default: 'name')
    """
    min_books = int(request.GET.get('min_books', 1))
    sort_by = request.GET.get('sort_by', 'name')
    
    queryset = Author.objects.annotate(
        book_count=Count('books'),
        latest_book_year=Max('books__publication_year')
    ).filter(book_count__gte=min_books)
    
    # Apply sorting
    if sort_by == 'book_count':
        queryset = queryset.order_by('-book_count')
    elif sort_by == 'latest_book':
        queryset = queryset.order_by('-latest_book_year')
    else:  # default to name
        queryset = queryset.order_by('name')
    
    # Get detailed data
    authors_data = []
    for author in queryset:
        author_data = {
            'id': author.id,
            'name': author.name,
            'book_count': author.book_count,
            'latest_book_year': author.latest_book_year,
            'books': [{'id': book.id, 'title': book.title, 'publication_year': book.publication_year} 
                     for book in author.books.all()]
        }
        authors_data.append(author_data)
    
    return Response({
        'min_books_filter': min_books,
        'sort_by': sort_by,
        'total_authors': len(authors_data),
        'authors': authors_data
    })


# All imports already done at the top
