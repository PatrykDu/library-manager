from django.urls import path

from . import views

urlpatterns = [
    path("add-book", views.CreateBookView.as_view(), name="add-book"),
    path("", views.MyLibraryView.as_view(), name="my-library"),
    path("thank-you", views.ThankYouView.as_view(), name="thank-you"),
    path("<slug:id>", views.SingleBookView.as_view(), name="book-detail-page"),
]
