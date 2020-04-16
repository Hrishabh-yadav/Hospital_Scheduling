from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('register2', views.register2, name="register2"),
    path('book_appoint', views.book_appoint, name="book_appoint"),
]
