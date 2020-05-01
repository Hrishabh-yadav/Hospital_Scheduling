from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User, auth
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import *
from datetime import datetime, timedelta
from django import template

register = template.Library()

@register.filter()
def addDays(days):
   newDate = datetime.today() + timedelta(days=days)
   return newDate


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Password or Username invalid!")
            return redirect('login')
    else:
        return render(request, 'Login.html')


def register(request):
    if (request.method == 'POST'):
        employee_id = request.POST['empid']
        email = request.POST['emailid']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=employee_id).exists():
                messages.info(request, 'Employee already registered')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered')
                return redirect('register')
            user = User.objects.create_user(username=employee_id, password=password1, email=email)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your hospital account.'
            message = render_to_string('acc_active_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, "Accept your email confirmation")
            return redirect('register')
        else:
            messages.info(request, "Password doesn't match")
            return redirect('register')


    else:
        return render(request, 'Register1.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


DAY_CHOICES = [
    'MON',
    'TUES',
    'WED',
    'THURS',
    'FRI',
    'SAT',
    'SUN'
]


def book_appoint(request, days=0):
    #day1 = DAY_CHOICES[datetime.datetime.today().weekday()]
    dayx = addDays(days)
    dayx = DAY_CHOICES[dayx.weekday()]
    query = Schedule.objects.filter(day=dayx)
    context = {'query': query}
    if request.method == 'POST':
        dept = request.POST['filter']
        if dept is not None:
            query = Schedule.objects.filter(doc__dept__deptid=int(dept) + 1, day=dayx)
            context = {'query': query}
            return render(request, 'Book_appoint.html', context)
        else:
            return render(request, 'Book_appoint.html', context)

    else:
        return render(request, 'Book_appoint.html', context)


def filter_d2(request):
    return book_appoint(request, 1)


def filter_d3(request):
    return book_appoint(request, 2)


def filter_d4(request):
    return book_appoint(request, 3)


def filter_d5(request):
    return book_appoint(request, 4)


def filter_d6(request):
    return book_appoint(request, 5)


def filter_d7(request):
    return book_appoint(request, 1)
