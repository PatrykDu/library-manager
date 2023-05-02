from django.shortcuts import render
from django.http import HttpResponse


def books(request):
    return HttpResponse("Hello, world. You're at the books index.")