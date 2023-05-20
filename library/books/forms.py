from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        labels = {
            "title": "Title here"
        },
        error_messages = {
            "title": {
                "required": "Title must not be empty!"
            }
        }
