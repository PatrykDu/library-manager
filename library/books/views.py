from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from .models import Book, Author, Language
from .forms import BookForm
from datetime import date


class CreateBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/add-book.html'
    success_url = "/thank-you"


class SingleBookView(UpdateView):
    model = Book
    fields = "__all__"
    template_name = 'books/single-book.html'

    def get(self, request, id):
        book: Book = Book.objects.get(id=id)

        # Add initial data to the form
        intaial_data = {
            'title': book.title,
            'authors': book.authors.all(),
            "published_date": book.published_date,
            "isbn_10": book.isbn_10,
            "isbn_13": book.isbn_13,
            "page_count": book.page_count,
            "thumbnail": book.thumbnail,
            "language": book.language
        }
        form = BookForm(initial=intaial_data)

        context = {
            "book": book,
            "book_form": form
        }

        return render(request, "books/single-book.html", context)

    def post(self, request, id):
        book_form: BookForm = BookForm(request.POST)
        book: Book = Book.objects.get(id=id)

        if book_form.is_valid():
            book.title = book_form.cleaned_data['title']
            book.authors.set(book_form.cleaned_data['authors'])
            book.published_date = book_form.cleaned_data['published_date']
            book.isbn_10 = book_form.cleaned_data['isbn_10']
            book.isbn_13 = book_form.cleaned_data['isbn_13']
            book.page_count = book_form.cleaned_data['page_count']
            book.thumbnail = book_form.cleaned_data['thumbnail']
            book.language = book_form.cleaned_data['language']

            book.save()
            return HttpResponseRedirect(reverse("book-detail-page", args=[id]))

        book: Book = Book.objects.get(id=id)

        context = {
            "book": book,
            "book_form": book_form,
        }
        return render(request, "blog/single-book.html", context)


class ThankYouView(TemplateView):
    template_name = "books/thank-you.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "tittle"
        return context


class MyLibraryView(ListView):
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
