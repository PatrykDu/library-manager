import datetime
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from rest_framework.views import APIView
from .models import Book, Author, Language
from .forms import BookForm
from datetime import date
import requests


class ImportBooks(APIView):

    def prepare_data(self, request):
        # fetchs data for query parameters from form
        query_data = {
            "intitle": self.request.GET.get("intitle", ''),
            "inauthor": self.request.GET.get("inauthor", ''),
            "inpublisher": self.request.GET.get("inpublisher", ''),
            "subject": self.request.GET.get("subject", ''),
            "isbn": self.request.GET.get("isbn", ''),
            "lccn": self.request.GET.get("lccn", ''),
            "oclc": self.request.GET.get("oclc", '')
        }

        # uses query parameters to make request to API
        number_of_all_generated_books, books_to_import = fetch_book_data(
            query_data)

        # pass fetched data to template
        context = {
            'imported_books': books_to_import,
            'query_data': query_data,
            'number_of_books': number_of_all_generated_books
        }

        return context

    def get(self, request):

        context = self.prepare_data(request)
        return render(request, 'books/import-book.html', context)

    def post(self, request):

        book_to_import = {}
        book_to_import['thumbnail'] = self.request.POST.get('thumbnail_data')
        book_to_import['title'] = self.request.POST.get('title_data')
        book_to_import['all_authors'] = self.request.POST.get('authors_data')
        book_to_import['published_date'] = self.request.POST.get('date_data')
        book_to_import['isbn_10'] = self.request.POST.get('isbn10_data')
        book_to_import['isbn_13'] = self.request.POST.get('isbn13_data')
        book_to_import['page_count'] = self.request.POST.get('pages_data')
        book_to_import['language'] = self.request.POST.get('language_data')

        title = book_to_import['title']
        published_date = book_to_import['published_date']
        if len(published_date) != 10:
            published_date = datetime.datetime(int(published_date), 1, 1)
            published_date = published_date.isoformat()
            published_date = published_date[:10]
        isbn_10 = book_to_import['isbn_10'] if len(
            book_to_import['isbn_10']) == 10 else None
        isbn_13 = book_to_import['isbn_13'] if len(
            book_to_import['isbn_13']) == 13 else None
        page_count = book_to_import['page_count']
        thumbnail = book_to_import['thumbnail']
        language = book_to_import['language']

        authors = []
        author_names = book_to_import['all_authors'][1:-1]
        author_names = author_names.replace("'", "")
        if "," in author_names:
            authors = author_names.split(",")
        else:
            authors.append(author_names)

        author_models = []
        for author in authors:
            if author[0] == " ":
                author = author[1:]
            try:
                found_author = Author.objects.get(name__icontains=author)
                author_models.append(found_author)
            except Author.DoesNotExist:
                new_author = Author.objects.create()
                new_author.name = author
                new_author.save()
                author_models.append(new_author)

        try:
            found_language = Language.objects.get(language__icontains=language)
        except Language.DoesNotExist:
            new_language = Language.objects.create()
            new_language.language = language
            new_language.save()
            found_language = new_language

        new_book = Book.objects.create()

        new_book.title = title
        new_book.authors.set(author_models)
        new_book.published_date = published_date
        new_book.isbn_10 = isbn_10
        new_book.isbn_13 = isbn_13
        new_book.page_count = page_count
        new_book.thumbnail = thumbnail
        new_book.language = found_language

        new_book.save()

        return HttpResponseRedirect(reverse("my-library"))


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


def fetch_book_data(query_data):

    def all_authors(authors):
        return ",\n".join([name for name in authors])

    def construct_query_params(query_data):
        query = ''
        for k, v in query_data.items():
            if v != "":
                query += f"+{k}:{v}"
        if query == "":
            return "intitle:"
        else:
            return query

    query_params = construct_query_params(query_data)
    url = f"https://www.googleapis.com/books/v1/volumes?q={query_params}&maxResults=40"
    response = requests.get(url)
    answer = response.json()
    numer_of_books = answer['totalItems'] if 'totalItems' in answer else 0
    books = []
    if answer['totalItems'] != 0:
        books_to_import = answer["items"]
    else:
        return books

    for book in books_to_import:
        book_data = {}
        book_data['title'] = book['volumeInfo']['title'] if 'title' in book['volumeInfo'] else 'empty title'
        book_data['authors'] = book['volumeInfo']['authors'] if "authors" in book['volumeInfo'] else [
            'Anonim']
        book_data['all_authors'] = all_authors(book_data['authors'])
        book_data['published_date'] = book['volumeInfo']['publishedDate'] if "publishedDate" in book['volumeInfo'] else None
        if 'industryIdentifiers' in book['volumeInfo'] and len(book['volumeInfo']['industryIdentifiers']) == 2:
            book_data['isbn_10'] = book['volumeInfo']['industryIdentifiers'][1]['identifier'] if book[
                'volumeInfo']['industryIdentifiers'][1]['type'] == 'ISBN_10' else ''
            book_data['isbn_13'] = book['volumeInfo']['industryIdentifiers'][0]['identifier'] if book[
                'volumeInfo']['industryIdentifiers'][0]['type'] == 'ISBN_13' else ''
        else:
            book_data['isbn_10'] = ''
            book_data['isbn_13'] = ''
        book_data['page_count'] = book['volumeInfo']['pageCount'] if "pageCount" in book['volumeInfo'] else 0
        if 'imageLinks' in book['volumeInfo']:
            book_data['thumbnail'] = book['volumeInfo']['imageLinks']['smallThumbnail'] if 'smallThumbnail' in book[
                'volumeInfo']['imageLinks'] else 'No Cover'
        else:
            book_data['thumbnail'] = 'No Cover'
        book_data['language'] = book['volumeInfo']['language'] if 'language' in book['volumeInfo'] else 'en'
        book_data['etag'] = book['etag']
        books.append(book_data)

    return (numer_of_books, books)
