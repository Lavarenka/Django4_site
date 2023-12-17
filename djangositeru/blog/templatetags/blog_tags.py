from django import template
import blog.views as views
"""
категории
"""
register = template.Library()
# регистрация тега
@register.simple_tag()
def get_categories():
    return views.cats_db


@register.inclusion_tag('blog/list_categories.html')
def show_categories(cat_selected=0): #cat_selected=0 для категорий , выводит активную категорию
    cats = views.cats_db
    return {'cats': cats, 'cat_selected': cat_selected}