from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Book

def books(request):
    return HttpResponse("Hello, world. You're at the books index.")


class MyLibrary(ListView):
    template_name = 'books/my-library.html'
    model = Book
    context_object_name = 'all_imported_books'
