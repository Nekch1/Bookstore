from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('catalog/', views.catalog_page, name="catalog"),
    path('contacts/', views.contacts_page, name="contacts"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
]