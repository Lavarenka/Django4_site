from django.http import HttpResponse
from django.shortcuts import render



def index(request): #функция предстовления
    return HttpResponse('Hello World')
def categories(request):
    return HttpResponse('<h1>Статьи по категориям</h1>')