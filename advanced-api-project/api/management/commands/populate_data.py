"""
Management command to populate the database with sample data for testing.
"""

from django.core.management.base import BaseCommand
from api.models import Author, Book


class Command(BaseCommand):
    help = 'Populate the database with sample authors and books for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample authors and books...')
        
        # Create sample authors
        authors_data = [
            {'name': 'George Orwell'},
            {'name': 'J.K. Rowling'},
            {'name': 'Harper Lee'},
            {'name': 'F. Scott Fitzgerald'},
            {'name': 'Jane Austen'},
        ]
        
        authors = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(**author_data)
            authors.append(author)
            if created:
                self.stdout.write(f'Created author: {author.name}')
            else:
                self.stdout.write(f'Author already exists: {author.name}')
        
        # Create sample books
        books_data = [
            {'title': '1984', 'publication_year': 1949, 'author': authors[0]},
            {'title': 'Animal Farm', 'publication_year': 1945, 'author': authors[0]},
            {'title': 'Harry Potter and the Philosopher\'s Stone', 'publication_year': 1997, 'author': authors[1]},
            {'title': 'Harry Potter and the Chamber of Secrets', 'publication_year': 1998, 'author': authors[1]},
            {'title': 'To Kill a Mockingbird', 'publication_year': 1960, 'author': authors[2]},
            {'title': 'The Great Gatsby', 'publication_year': 1925, 'author': authors[3]},
            {'title': 'Pride and Prejudice', 'publication_year': 1813, 'author': authors[4]},
            {'title': 'Emma', 'publication_year': 1815, 'author': authors[4]},
        ]
        
        for book_data in books_data:
            book, created = Book.objects.get_or_create(**book_data)
            if created:
                self.stdout.write(f'Created book: {book.title} by {book.author.name}')
            else:
                self.stdout.write(f'Book already exists: {book.title} by {book.author.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database with {len(authors)} authors and {len(books_data)} books'
            )
        )

