from django import template
from django.db.models import Count

import blog.views as views
from blog.models import Category, TagPost
from blog.utils import menu

"""
категории
"""
register = template.Library()


# регистрация тега
@register.simple_tag
def get_menu():
    return menu

@register.inclusion_tag('blog/list_categories.html')
def show_categories(cat_selected=0):  # cat_selected=0 для категорий , выводит активную категорию

    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    # фильтр, выводит те категории к которых есть посты
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('blog/list_tags.html')
def show_all_tags():
    # фильтр, выводит те теги к которых есть посты
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}
