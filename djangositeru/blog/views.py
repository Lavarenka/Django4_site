from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView

from .forms import AddPostForm, UploadFileForm, AddCommentForm
from .models import Blog, Category, Comment, TagPost, UploadFiles
from .utils import DataMixin, Qawsda

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class BlogHome(DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    title_page = 'Главная станица'
    cat_selected = 0

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

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    data = {'title': 'О сайте',
            'menu': menu,
            'form': form,
            }
    return render(request, 'blog/about.html', data)


class BlogCategory(DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Blog.published.filter(cat__slug=self.kwargs['cat_slug']).select_related(
            'cat')  # к категории добавляем пост

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


class BlogTag(DataMixin, ListView):
    """выводим теги """
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег - ' + tag.tag)

    def get_queryset(self):
        return Blog.published.filter(tags__slug=self.kwargs['tag_slug']).select_related(
            'cat')  # к категории добавляем пост


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


class AddPage(DataMixin, View):
    title_page = "Добавление статьи"

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
        print(request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
            "title": f"Добавление статьи",
            "menu": menu,
            "form": form
        }
        return render(request, 'blog/addpage.html', context=data)


class ShowPost(DataMixin, DetailView, Qawsda):
    """Вывод отдельного поста"""
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'  # слаг с урла
    context_object_name = 'post'  # перменная в html

    def get_context_data(self, **kwargs):
        cat = Blog.objects.get(slug=self.kwargs['post_slug'])
        comment = Comment.objects.filter(com_id=cat.pk)
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(context, title=context['post'].title, comment=comment, form=AddCommentForm)

    def get_object(self, queryset=None):
        """возвращает только опубликованные """
        return get_object_or_404(Blog.published, slug=self.kwargs[self.slug_url_kwarg])


class CreateComment(CreateView):
    """Добавление коммента"""
    model = Comment
    form_class = AddCommentForm

    def form_valid(self, form):
        form.instance.com_id = self.kwargs.get('pk')
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """действе после отправки комента , остается на странице"""

        return self.object.com.get_absolute_url()


class Search(DataMixin, ListView):
    """Поиск
    sqlite не поддерживает регистрозависимоть кириллицуы
    """

    template_name = 'blog/search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Blog.published.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Поиск', s=f"s={self.request.GET.get('s')}&")
