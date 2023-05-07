from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView
from .models import Book, Author

def books(request):
    return HttpResponse("Hello, world. You're at the books index.")


class MyLibrary(ListView):
    template_name = 'books/my-library.html'
    model = Book
    context_object_name = 'library'

    def get_queryset(self):
        search_title = self.request.GET.get("t", '')
        searched_author = self.request.GET.get("a", '')
        books = Book.objects.all()
        filtered_title = books.filter(title__icontains=search_title)
        filtered_author = filter_authors(searched_author, filtered_title)
        filtered_books = filtered_author

        authors = Author.objects.all()
        
        queryset = {'filtered_books': filtered_books, 
                    'all_authors': authors}

        return queryset
    
def filter_authors(searcher_author, all_books: QuerySet[Book]):
    if searcher_author == '':
        return all_books
    else:
        filtered_books = []
        for book in all_books:
            book_authors = book.get_list_of_authors()
            if searcher_author in book_authors:
                filtered_books.append(book)
        return filtered_books



