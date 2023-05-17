from django.urls import path

from . import views

urlpatterns = [
    path("books", views.CreateBookView.as_view(), name="books"),
    path("", views.MyLibraryView.as_view(), name="my-library"),
    path("thank-you", views.ThankYouView.as_view(), name="thank-you")
]