from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]

data_db = [
    {'id': 1, 'title': 'Анжелина джоли',
     'content': '''<h1>Lorem Ipsum</h1> is simply dummy text of the printing and typesetting industry. 
     Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown 
     printer took a galley of type and scrambled it to make a type specimen book. It has survived 
     not only five centuries, but also the leap into electronic typesetting, remaining essentially 
     unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
     and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Анжелины ДжолиБиография Джулия Робертс',
     'is_published': True},
    {'id': 4, 'title': 'Джулия Робертс2', 'content': 'Биография Анжелины ДжолиБиография Джулия Робертс2',
     'is_published': True},
    {'id': 5, 'title': 'Джулия Робертс3', 'content': 'Биография Анжелины ДжолиБиография Джулия Робертс3',
     'is_published': True},
    {'id': 6, 'title': 'Джулия Робертс4', 'content': 'Биография Анжелины ДжолиБиография Джулия Робертс4',
     'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Актрисы'},
    {'id': 2, 'name': 'Певицы'},
    {'id': 3, 'name': 'Спортсменки'},
]


# в шаблоне обращатся через точку
def index(request):
    """
    функция предстовления
    подключаем шаблон
    data = title страницы
    """
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': 0, # для вывода активной категории, прописана в block_tags
    }
    return render(request, 'blog/index.html', context=data)


def about(request):
    """
    подключаем шаблон 'О себе'
    data = title страницы
    """
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'blog/about.html', data)


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def show_category(request, cat_id):
    """
    для вывода активной категории, все как в index
    """
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'blog/index.html', context=data)


# def categories(request, cat_id):
#     """
#     :param request: обязательный параметр
#     :param cat_id: вывод ид категории
#     :return: возвращат страницу
#     """
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>id: {cat_id}</p>')


# def categories_by_slug(request, cat_slug):
#     if request.POST:
#         print(request.POST)  # ?name=Gagarina&type=pop
#     return HttpResponse(f'<h1>Статьи по категориям_slug</h1><p>slug: {cat_slug}</p>')


# def archive(request, year):
#     # if year > 2023:
#     #     вызываем 404 если больше 2023
#     #     raise Http404()
#     if year > 2023:
#         # перенаправление на главную страницу
#         # home имя маршрута
#         # uri = reverse('cat', args=('music',))
#
#         return redirect('home')
#     return HttpResponse(f'<h1>Архив по годам</h1><p>year: {year}</p>')

def addpage(request):
    return HttpResponse('Добавление статьи')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def page_not_found(request, exception):
    """
    обработчик 404
    в настройках выключить дебаг
    нужно прописать handler404 = page_not_found в общих урлах
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
    # return redirect('/')
