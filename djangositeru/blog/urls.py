from django.urls import path, re_path, register_converter
from . import views
from . import converters
"""
https://proproprogs.ru/django4/django4-dinamicheskie-url-polzovatelskie-konvertery
все маршруты приложения blog
name='home' имя маршрута
"""
register_converter(converters.FourDigitYearConverter, "year4") # регистрируем конвертер для archive

urlpatterns = [
    path('', views.BlogHome.as_view(), name='home'), # подключаем наш урл + импортируем,
    path('about/', views.about, name='about'), # подключаем наш урл + импортируем,
    path('addpage/', views.AddPage.as_view(), name='add_page'), # добавление статьи, вызываем класс из views
    path('contact/', views.contact, name='contact'), # контакты,
    path('login/', views.login, name='login'), # логин,
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    # path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.BlogCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.BlogTag.as_view(), name='tag'),

    # path('cat/<int:cat_id>/', views.categories, name='cat_id'),
    # path('cat/', views.categories),  без пагинации
    # path('cat/<slug:cat_slug>/', views.categories_by_slug, name='cat'),
    # path("archive/<year4:year>/", views.archive, name='archive'),
    # с помощью регулярных выражений
]