from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.language

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)
    published_date = models.DateField()
    isbn_10 = models.CharField(max_length=10)
    isbn_13 = models.CharField(max_length=13)
    page_count = models.IntegerField()
    thumbnail = models.CharField(max_length=255)
    language = models.ManyToManyField(Language)

    def __str__(self) -> str:
        return f"Title: {self.title}, By: [x for x in self.authors]"