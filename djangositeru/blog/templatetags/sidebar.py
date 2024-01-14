from django import template
from blog.models import  Blog

"""
кастомные 
последние статьи
"""
register = template.Library()


@register.inclusion_tag('blog/popular_posts.html')
def get_popular(cnt=3):
    # cnt количество выводимых постов
    posts = Blog.objects.order_by('-time_create')[:cnt]
    return {"posts": posts , }
