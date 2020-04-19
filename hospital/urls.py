from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name = 'logout'),
    path('register', views.register, name="register"),
    path('book_appoint', views.book_appoint, name="book_appoint"),
    path('^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    path('filter', views.DoctorListView.as_view(), name='doctor_changelist'),
    path('add/', views.DoctorCreateView.as_view(), name='doctor_add'),
    path('<int:pk>/', views.DoctorUpdateView.as_view(), name='doctor_change')
]
