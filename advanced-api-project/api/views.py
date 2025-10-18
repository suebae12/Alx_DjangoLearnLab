from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    Provides read-only access to all Book instances with filtering and search capabilities.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated read access
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering


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
    Combined ListView and CreateView for books.
    Provides both listing and creation functionality in a single endpoint.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']


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
    ListView for retrieving all authors with their books.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author with their books.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


# Custom API endpoint for demonstration
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def book_stats(request):
    """
    Custom endpoint to get statistics about books.
    """
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    
    # Get books by publication year
    from django.db.models import Count
    books_by_year = Book.objects.values('publication_year').annotate(
        count=Count('id')
    ).order_by('-publication_year')[:5]
    
    return Response({
        'total_books': total_books,
        'total_authors': total_authors,
        'recent_books_by_year': list(books_by_year)
    })
