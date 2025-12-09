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
    path('profile/delete-order/<int:order_id>/', views.delete_order, name='delete_order'),

    path('logout/', views.logout_func, name="logout"),
    path('adminDash/', views.admin_page, name="admin_dash"),
    path('book/<int:book_id>/', views.book_detail_page, name='book_detail'),
    
    path('cart/', views.cart_page, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),

    path('order/confirm/', views.order_confirm_page, name='order_confirm'),
    path('order/create/', views.create_order, name='create_order'),


    path('adminDash/delete-book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('adminDash/edit-book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('adminDash/delete-genre/<int:genre_id>/', views.delete_genre, name='delete_genre'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)