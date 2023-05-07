from django.urls import path

from . import views

urlpatterns = [
    path("", views.books, name="books"),
    path("library", views.MyLibrary.as_view(), name="my-library")
]