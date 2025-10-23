from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_page, name='home'),
    path('catalog/', views.catalog_page, name="catalog"),
    path('contacts/', views.contacts_page, name="contacts"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('profile/', views.profile_page, name="profile"),
    path('logout/', views.logout_func, name="logout"),
    path('adminDash/', views.admin_page, name="admin_dash"),
    path('book/<int:book_id>/', views.book_detail_page, name='book_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)