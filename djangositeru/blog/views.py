from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import AddPostForm, UploadFileForm, AddCommentForm
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


# def show_post(request, post_slug):
#     post = get_object_or_404(Blog, slug=post_slug)  # берем из бз пост
#     print(post.pk)
#     comment = Comment.objects.filter(com_id=post.pk)  # к посту подрубаем коьменты
#     print(comment)
# #
#     # comments = post.comments.filter(active=True)
# #     new_comment = None  # Comment posted
# #     if request.method == 'POST':
# #         comment_form =AddCommentForm(data=request.POST)
# #         if comment_form.is_valid():
# #             # Create Comment object but don't save to database yet
# #             new_comment = comment_form.save(commit=False)
# #             # Assign the current post to the comment
# #             # new_comment.post = post
# #             # Save the comment to the database
# #             new_comment.save()
# #     else:
# #         comment_form = AddCommentForm()
# #
# #
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'comment': comment,
#         # 'new_comment': new_comment,
#         # 'comment_form': comment_form,/
#         'cat_selected': 1,  # для вывода активной категории, прописана в block_tags
#     }
#     return render(request, 'blog/post.html', data)


class BlogCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Blog.published.filter(cat__slug=self.kwargs['cat_slug']).select_related(
            'cat')  # к категории добавляем пост

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        print(cat.pk)
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


class BlogTag(ListView):
    """выводим теги """
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])

        context['title'] = 'Тег - ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None

        return context

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


class ShowPost(DetailView):
    """Вывод отдельного поста"""
    # model = Blog
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'  # слаг с урла
    context_object_name = 'post'  # перменная в html

    def get_context_data(self, **kwargs):
        cat = Blog.objects.get(slug=self.kwargs['post_slug'])
        comment = Comment.objects.filter(com_id=cat.pk)
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        context['comment'] = comment
        context['form'] = AddCommentForm
        return context

    def get_object(self, queryset=None):
        """возвращает только опубликованные """
        return get_object_or_404(Blog.published, slug=self.kwargs[self.slug_url_kwarg])
