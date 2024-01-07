from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index_page(request):
    return HttpResponse("<h1>This is index page</h1>")
