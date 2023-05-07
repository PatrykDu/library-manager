from django.contrib import admin
from .models import Book, Author, Language

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Language)