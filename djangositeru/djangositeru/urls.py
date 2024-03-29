"""
URL configuration for djangositeru project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog.views import page_not_found
from djangositeru import settings

"""
https://proproprogs.ru/django4/django4-dinamicheskie-url-polzovatelskie-konvertery
Прописываем все маршруты ПРИЛОЖЕНИЙ на сайте, представление описано и импартировано в views
+ импортируем include из django.urls
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # подключаем маршруты приложения blog которые описаны в blog\urls.py
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    # для отображения файлов в режиме отдладки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# обработчик 404
handler404 = page_not_found

admin.site.site_header = "Админка" # хедер админки
admin.site.index_title = "Blog Артема" # хедер приложения в админке