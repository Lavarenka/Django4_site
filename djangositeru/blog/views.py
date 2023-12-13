from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect


def index(request): #функция предстовления
    return HttpResponse('Hello World')
def categories(request, cat_id):
    """
    :param request: обязательный параметр
    :param cat_id: вывод ид категории
    :return: возвращат страницу
    """
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>id: {cat_id}</p>')


def categories_by_slug(request, cat_slug):
    if request.POST:
        print(request.POST) # ?name=Gagarina&type=pop
    return HttpResponse(f'<h1>Статьи по категориям_slug</h1><p>slug: {cat_slug}</p>')

def archive(request, year):
    # if year > 2023:
    #     вызываем 404 если больше 2023
    #     raise Http404()
    if year > 2023:
        # перенаправление на главную страницу
        # home имя маршрута
        return redirect('home')
    return HttpResponse(f'<h1>Архив по годам</h1><p>year: {year}</p>')

def page_not_found(request, exception):
    """
    обработчик 404
    в настройках выключить дебаг
    нужно прописать handler404 = page_not_found в общих урлах
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
    # return redirect('/')