from django.urls import path
from . import views
"""
все маршруты приложения blog
"""
urlpatterns = [
    path('', views.index), # подключаем наш урл + импортируем
    path('cat/', views.categories), # подключаем наш урл + импортируем
]