from django import template
import blog.views as views
from blog.models import Category, TagPost

"""
категории
"""
register = template.Library()


# регистрация тега


@register.inclusion_tag('blog/list_categories.html')
def show_categories(cat_selected=0):  # cat_selected=0 для категорий , выводит активную категорию
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('blog/list_tags.html')
def show_all_tags():

    return {'tags': TagPost.objects.all()}
