from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Books, Genre, CartItem, Order, OrderItem
from decimal import Decimal

def index_page(request):
    context = {
        "title_page" : "Главная страница" 
    }
    return render(request,"index.html", context)

def catalog_page(request):
    sort = request.GET.get('sort')
    selected_genres = request.GET.getlist('genre')

    books = Books.objects.all().order_by('-id')  

    if selected_genres:
        books = books.filter(genre__name__in=selected_genres).distinct()

    if sort == 'price_asc':
        books = books.order_by('price')
    elif sort == 'price_desc':
        books = books.order_by('-price')
    elif sort == 'title_asc':
        books = books.order_by('title')
    elif sort == 'title_desc':
        books = books.order_by('-title')
    elif sort == 'year':
        books = books.order_by('-year')

    context = {
        "title_page": "Каталог",
        "books": books,
        "genres": Genre.objects.all(),
        "selected_genres": selected_genres,
        "sort": sort
    }
    return render(request,"catalog.html", context)

def contacts_page(request):
    context = {
        'title_page' : 'Контакты'
    }
    return render(request,"contact.html", context)

def register_page(request):
    context = {
        'title_page' : 'Регистрация'
    }
    if request.method == "POST":
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        patronymic = request.POST.get('patronymic')
        username = request.POST.get('login')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirmPassword')

        if (password1 != password2):
            return render(request,"auth/register.html", {'error':'Пароли не совпадают'})
        
        if CustomUser.objects.filter(username=username).exists():
            return render(request,"auth/register.html", {'error':'Пользователь с таким имененм уже существует'})
        
        user = CustomUser.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            patronymic = patronymic, 
            email = email,
            password = password1,
        )

        login(request, user)
        return redirect('home')
    return render(request,"auth/register.html", context)

def login_page(request):
    context = {
        'title_page' : 'Авторизация'
    }

    if request.method == "POST":
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request,"auth/login.html", {"error":"Неверный логин или пароль"})
        
    return render(request,"auth/login.html", context)

@login_required
def profile_page(request):
    orders = Order.objects.filter(user = request.user).order_by('-created_at')
    context = {
        'title_page' : 'Профиль',
        'orders': orders
    }
    return render(request,"profile.html", context)

@login_required
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect("profile")

    if not order.is_confirmed:  
        order.delete()

    return redirect("profile")

@login_required
def logout_func(request):
    logout(request)
    return redirect('home')

@login_required
def admin_page(request):
    if request.user.role != 'admin':
        return redirect('home')  

    if request.method == "POST" and 'genre_submit' in request.POST:
        genre_name = request.POST.get('genre_name')
        if genre_name:
            Genre.objects.create(name=genre_name)
            return redirect('admin_dash')

    if request.method == "POST" and 'book_submit' in request.POST:
        title = request.POST.get('title')
        description = request.POST.get('description')
        author = request.POST.get('author')
        price = request.POST.get('price')
        country = request.POST.get('country')
        year = request.POST.get('year')
        image = request.FILES.get('image')
        quantity = request.POST.get('quantity')
        genres = request.POST.getlist('genres')

        book = Books.objects.create(
            title=title,
            description=description,
            author=author,
            price=price,
            country=country,
            year=year,
            image=image,
            quantity=quantity
        )

        if genres:
            book.genre.set(genres)

        return redirect('admin_dash')

    genres = Genre.objects.all()
    books = Books.objects.all().order_by('-id') 

    context = {
        'title_page': 'Панель администратора',
        'genres': genres,
        'books': books
    }
    return render(request, "admin-dashboard.html", context)

def book_detail_page(request, book_id):
    book = Books.objects.get(id=book_id)
    in_cart = False

    if request.user.is_authenticated:
        in_cart = CartItem.objects.filter(user=request.user, book=book).exists()

    context = {
        'book': book,
        'in_cart': in_cart
    }
    return render(request, 'book_detail.html', context)



@login_required
def add_to_cart(request, book_id):
    book = Books.objects.get(id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)

    if not created: 
        if cart_item.quantity < book.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            return JsonResponse({"error": "Недостаточно книг в наличии"}, status=400)

    return redirect('cart')


@login_required
def cart_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum([item.total_price() for item in cart_items])
    return render(request, "cart.html", {"cart_items": cart_items, "total": total})


@login_required
@require_GET
def update_cart_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id, user=request.user)
    action = request.GET.get('action')

    if action == 'plus' and item.quantity < item.book.quantity:
        item.quantity += 1
    elif action == 'minus' and item.quantity > 1:
        item.quantity -= 1

    item.save()

    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(i.total_price() for i in cart_items)

    return JsonResponse({
        'quantity': item.quantity,
        'item_total': item.total_price(),
        'cart_total': total
    })


@login_required
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('cart')

@login_required
def create_order(request):
    if request.method == "POST":
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is None:
            return JsonResponse({'error': 'Неверный пароль'}, status=400)

        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return JsonResponse({'error': 'Корзина пуста'}, status=400)

        total = sum(item.total_price() for item in cart_items)
        order = Order.objects.create(user=request.user, total_amount=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            item.book.quantity -= item.quantity
            item.book.save()

        cart_items.delete()

        return JsonResponse({'success': True})

@login_required
def order_confirm_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, "order_confirm.html", {"cart_items": cart_items, "total": total})
