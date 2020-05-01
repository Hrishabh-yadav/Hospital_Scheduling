from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name = 'logout'),
    path('register', views.register, name="register"),
    path('book_appoint', views.book_appoint, name="book_appoint"),
    path('filter_d1', views.book_appoint, name="filter_d1"),
    path('filter_d2', views.filter_d2, name="filter_d2"),
    path('filter_d3', views.filter_d3, name="filter_d3"),
    path('filter_d4', views.filter_d4, name="filter_d4"),
    path('filter_d5', views.filter_d5, name="filter_d5"),
    path('filter_d6', views.filter_d6, name="filter_d6"),
    path('filter_d7', views.filter_d7, name="filter_d7"),
    path('^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
]
