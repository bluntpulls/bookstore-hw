from django.contrib import admin

from .models import Book, Category


class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    fields = ('title', 'author', 'price', 'stock')
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'book_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    list_filter = ('name',)
    inlines = [BookInline]

    @admin.display(description='Книг')
    def book_count(self, obj):
        return obj.books.count()


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'stock', 'in_stock')
    list_filter = ('category', 'author')
    search_fields = ('title', 'author', 'description')
    list_editable = ('price', 'stock')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'category'),
        }),
        ('Деталі', {
            'fields': ('price', 'stock', 'description'),
        }),
        ('Службове', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    @admin.display(boolean=True, description='В наявності')
    def in_stock(self, obj):
        return obj.in_stock
