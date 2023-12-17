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