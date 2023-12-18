from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string

from .models import Blog, Category, Comment

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


# в шаблоне обращатся через точку
def index(request):
    """
    функция предстовления
    подключаем шаблон
    data = title страницы
    """
    posts = Blog.published.all()  # все опубл статьи , прописан класс в моделях
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,  # для вывода активной категории, прописана в block_tags
    }
    return render(request, 'blog/index.html', context=data)


def about(request):
    """
    подключаем шаблон 'О себе'
    data = title страницы
    """
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'blog/about.html', data)


def show_post(request, post_slug):
    post = get_object_or_404(Blog, slug=post_slug)  # берем из бз пост
    comment = Comment.objects.filter(com_id=post.pk) # к посту подрубаем коьменты
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'comment': comment,
        'cat_selected': 1,  # для вывода активной категории, прописана в block_tags
    }
    return render(request, 'blog/post.html', data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Blog.published.filter(cat_id=category.pk) # к категории добавляем пост
    """
    для вывода активной категории, все как в index
    """
    data = {
        'title': f'{category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'blog/index.html', context=data)





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
