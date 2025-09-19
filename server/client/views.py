from django.shortcuts import render

# Create your views here.
def index_page(request):
    context = {
        "title_page" : "Главная страница" 
    }
    return render(request,"index.html", context)

def catalog_page(request):
    context = {
        "title_page" : "Каталог" 
    }
    return render(request,"catalog.html", context)

def contacts_page(request):
    context = {
        'title_page' : 'Контакты'
    }
    return render(request,"contact.html", context)

def login_page(request):
    context = {
        'title_page' : 'Авторизация'
    }
    return render(request,"login.html", context)

def register_page(request):
    context = {
        'title_page' : 'Регистрация'
    }
    return render(request,"register.html", context)
