from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'Login.html')

def book_appoint(request):
    return render(request, 'Book_appoint.html')