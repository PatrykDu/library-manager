from django.db import models
from django.urls import reverse

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
    title = models.CharField(max_length=200, null=True, blank=True)
    authors = models.ManyToManyField(Author, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    isbn_10 = models.CharField(max_length=10, null=True, blank=True)
    isbn_13 = models.CharField(max_length=13, null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    thumbnail = models.CharField(max_length=255, null=True, blank=True)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title}"

    def all_authors(self):
        return ",\n".join([a.name for a in self.authors.all()])

    def get_list_of_authors(self):
        list_of_authors = []
        for author in self.authors.all():
            list_of_authors.append(author.name)
        return list_of_authors

    def get_language(self):
        return self.language.language

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.pk})
