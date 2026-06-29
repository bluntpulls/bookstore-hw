from decimal import Decimal

from django.db.models import Avg, Count, Q

from .models import Book, Category


def get_books_in_stock():
    return Book.objects.filter(stock__gt=0)


def get_affordable_books(max_price: Decimal):
    return Book.objects.filter(price__lte=max_price).order_by('price')


def search_books(query: str):
    return Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    )


def get_books_by_author_or_category(author: str, category_slug: str):
    return Book.objects.filter(
        Q(author__iexact=author) | Q(category__slug=category_slug)
    )


def get_available_books_in_category(category_slug: str, min_stock: int = 1):
    return Book.objects.filter(
        Q(category__slug=category_slug) & Q(stock__gte=min_stock)
    )


def get_categories_with_book_stats():
    return Category.objects.annotate(
        books_count=Count('books'),
        avg_price=Avg('books__price'),
    ).order_by('-books_count')


def get_authors_with_book_count():
    return (
        Book.objects.values('author')
        .annotate(book_count=Count('id'))
        .order_by('-book_count')
    )


def get_out_of_stock_books():
    return Book.objects.filter(
        Q(stock=0) & ~Q(description='')
    )
