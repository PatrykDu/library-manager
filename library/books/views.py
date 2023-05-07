from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView
from .models import Book, Author, Language
from datetime import date


def books(request):
    return HttpResponse("Hello, world. You're at the books index.")


class MyLibrary(ListView):
    template_name = 'books/my-library.html'
    model = Book
    context_object_name = 'library'

    def get_queryset(self):
        search_title = self.request.GET.get("t", '')
        searched_author = self.request.GET.get("a", '')
        searched_language = self.request.GET.get("l", '')
        date_from = self.request.GET.get("start", '1900-07-22')
        today = self.request.GET.get("stop", date.today())

        books = Book.objects.all().filter(
            published_date__range=[date_from, today])
        filtered_title = books.filter(title__icontains=search_title)
        filtered_author = filter_authors(searched_author, filtered_title)
        filtered_language = filter_language(searched_language, filtered_author)

        filtered_books = filtered_language
        authors = Author.objects.all()
        languages = Language.objects.all()

        queryset = {'filtered_books': filtered_books,
                    'all_authors': authors,
                    'all_languages': languages,
                    'date_from': str(date_from),
                    'today': str(today),
                    'searched_author': searched_author,
                    'searched_language': searched_language,
                    'searched_title': search_title}

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


def filter_language(searched_language, all_books: QuerySet[Book]):
    if searched_language == '':
        return all_books
    else:
        filtered_books = []
        for book in all_books:
            book_language = book.get_language()
            if searched_language == book_language:
                filtered_books.append(book)
        return filtered_books
