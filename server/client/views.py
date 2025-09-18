from django.shortcuts import render

# Create your views here.
def index_page(request):
    
    context = {
       "page_name" : 'Демо оператора условия',
       "user_name" : 'Иван',
       "user_age" : 20,
    }
    return render(request,"index.html", context)
