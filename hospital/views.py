from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'Login.html')


def register(request):
    if(request.method == 'POST'):
        empid = request.POST('empid')
        emailid = request.POST('emailid')
        pass1 = request.POST('password1')
        pass2 = request.POST('password2')

    else:
        return render(request, 'Register1.html')



def book_appoint(request):
    return render(request, 'Book_appoint.html')
