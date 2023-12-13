from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string


menu = ["О сайте","Добавить статью","Обратная связь","Войти"]
# в шаблоне обращатся через точку
def index(request):
    """
    функция предстовления
    подключаем шаблон
    data = title страницы
    """
    data = {
        'title': 'Главная страница',
        'sub_title': 'Главная страница 2',
        'menu': menu,
    }
    return render(request, 'blog/index.html', context=data)


def about(request):
    """
    подключаем шаблон 'О себе'
    data = title страницы
    """
    data = {'title': 'О сайте'}
    return render(request, 'blog/about.html', data)

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
        # uri = reverse('cat', args=('music',))

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