from django.contrib import admin
from .models import Book, Author, Language

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'all_authors',)

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Language)