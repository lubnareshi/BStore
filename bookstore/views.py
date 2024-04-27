from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Book



def home(request):
    products = Book.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }

    return render(request, 'home.html', context)

    # return HttpResponse('Not able to load home')
    
    