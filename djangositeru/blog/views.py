from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string

from .forms import AddPostForm
from .models import Blog, Category, Comment, TagPost

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
    .select_related('cat') = убирает дублирование запросов
    """
    posts = Blog.published.all().select_related('cat')  # все опубл статьи , прописан класс в моделях
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
    comment = Comment.objects.filter(com_id=post.pk)  # к посту подрубаем коьменты
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
    posts = Blog.published.filter(cat_id=category.pk).select_related('cat')  # к категории добавляем пост
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


def show_tag_postlist(request, tag_slug):
    """
    отображение по тегам
    posts / выводит по тегу опубликованные посты
    """
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Blog.Status.PUBLICHED).select_related('cat')
    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None,
    }
    return render(request, 'blog/index.html', context=data)


def addpage(request):
    """Проерка на форму какой пришел запрос"""
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            print()
            # try:
            #     Blog.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except:
            #     form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()


    data = {
        "title": f"Добавление статьи",
        "menu": menu,
        "form": form
    }
    return render(request, 'blog/addpage.html', context=data)


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
