from django.contrib import admin
from .models import Book


# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('book_title', )}


admin.site.register(Book, BookAdmin)
