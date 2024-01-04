


from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView

from .forms import AddPostForm, UploadFileForm
from .models import Blog, Category, Comment, TagPost, UploadFiles

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]



class BlogHome(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Blog.published.all().select_related('cat')



def about(request):
    """
    подключаем шаблон 'О себе'
    data = title страницы
    UploadFileForm прописан в формах
    UploadFiles прописан в моделях
    """
    if request.method == 'POST':
        # handle_uploaded_file(request.FILES['file_upload'])
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    data = {'title': 'О сайте',
            'menu': menu,
            'form': form,
            }
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

class BlogCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False
    def get_queryset(self):
        return Blog.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')  # к категории добавляем пост

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context
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


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
            "title": f"Добавление статьи",
            "menu": menu,
            "form": form
        }
        return render(request, 'blog/addpage.html', context=data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
            "title": f"Добавление статьи",
            "menu": menu,
            "form": form
        }
        return render(request, 'blog/addpage.html', context=data)
