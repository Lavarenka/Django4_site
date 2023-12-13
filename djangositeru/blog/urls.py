from django.urls import path, re_path, register_converter
from . import views
from . import converters
"""
https://proproprogs.ru/django4/django4-dinamicheskie-url-polzovatelskie-konvertery
все маршруты приложения blog
"""
register_converter(converters.FourDigitYearConverter, "year4") # регистрируем конвертер для archive

urlpatterns = [
    path('', views.index, name='home'), # подключаем наш урл + импортируем,  name='home' имя маршрута
    path('cat/<int:cat_id>/', views.categories),
    # path('cat/', views.categories),  без пагинации
    path('cat/<slug:cat_slug>/', views.categories_by_slug),
    path("archive/<year4:year>/", views.archive),
    # с помощью регулярных выражений
]