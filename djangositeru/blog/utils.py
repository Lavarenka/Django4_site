"""
Миксины
"""
from django.shortcuts import render

from blog.forms import AddCommentForm

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class DataMixin:
    paginate_by = 5 # количество стаей на страницу
    title_page = None
    cat_selected = None
    extra_context = {}


    def __init__(self):
        """
        если title_page не None то присваеваем
        дополнительно прописывае ключ меню
        """
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)  # для дополнительных параметров
        return context

class Qawsda:
    def get(self, request):

        form = AddCommentForm()

        data = {
            "title": f"Добавление статьи",
            "menu": menu,
            "form": form
        }
        return render(request, 'blog/addpage.html', context=data)
    def post(self, request):
        form = AddCommentForm(request.POST)
        print(form)
        print(request.POST)