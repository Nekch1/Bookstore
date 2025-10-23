from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Books, Genre

# Create your views here.
def index_page(request):
    context = {
        "title_page" : "Главная страница" 
    }
    return render(request,"index.html", context)

def catalog_page(request):
    sort = request.GET.get('sort')
    selected_genres = request.GET.getlist('genre')

    books = Books.objects.all().order_by('-id')  # по умолчанию — новинки

    # фильтр по жанрам
    if selected_genres:
        books = books.filter(genre__name__in=selected_genres).distinct()

    # сортировка
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

# @csrf_exempt
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

# @csrf_exempt
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
    context = {
        'title_page' : 'Профиль'
    }
    return render(request,"profile.html", context)

@login_required
def logout_func(request):
    logout(request)
    return redirect('home')

@login_required
def admin_page(request):
    if request.user.role != 'admin':
        return redirect('home')  # доступ только для админа

    # добавление жанра
    if request.method == "POST" and 'genre_submit' in request.POST:
        genre_name = request.POST.get('genre_name')
        if genre_name:
            Genre.objects.create(name=genre_name)
            return redirect('admin_dash')

    # добавление книги
    if request.method == "POST" and 'book_submit' in request.POST:
        title = request.POST.get('title')
        description = request.POST.get('description')
        author = request.POST.get('author')
        price = request.POST.get('price')
        country = request.POST.get('country')
        year = request.POST.get('year')
        image = request.FILES.get('image')
        genres = request.POST.getlist('genres')

        book = Books.objects.create(
            title=title,
            description=description,
            author=author,
            price=price,
            country=country,
            year=year,
            image=image
        )

        if genres:
            book.genre.set(genres)

        return redirect('admin_dash')

    genres = Genre.objects.all()
    books = Books.objects.all().order_by('-id')  # новые сверху

    context = {
        'title_page': 'Панель администратора',
        'genres': genres,
        'books': books
    }
    return render(request, "admin-dashboard.html", context)

def book_detail_page(request, book_id):
    book = Books.objects.get(id=book_id)
    context = {'book': book}
    return render(request, 'book_detail.html', context)