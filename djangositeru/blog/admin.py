from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Blog, Comment, Category, TagPost

"""
регистрация приложения в админке
"""


@admin.register(Blog)  # регистрация приложения
class BlogAdmin(admin.ModelAdmin):
    """
    настройка даминки статьи
    list_display // отображение полей в статьи
    list_display_links // кликабельность полей
    ordering // сортировка записей для админки
    list_editable // возможность редоктирования не входя в статью
    РЕДАКТИРУЕМОЕ ПОЛЕ НЕ МОЖЕТ БЫТЬ КЛИКАБЕЛЬНЫМ
    list_per_page // пагинация, отображение статей на админку
    """
    #fields = []   очередность полей в статье
    list_display = ('id', 'title', 'time_create', 'is_published','slug', 'cat','post_photo')
    # readonly_fields = ['slug'] # поле которое нельзя редактировать , слаги добавляются автоматом
    readonly_fields = ['post_photo', ]
    prepopulated_fields = {"slug": ("title", )} # для автоматического добавления слага
    filter_horizontal = ['tags'] # более удобное отображение тегов
    list_display_links = ('id', 'title')
    ordering = ['time_create', 'title']
    list_editable = ('is_published', 'cat', )
    list_per_page = 10
    actions = ['set_published', 'set_draft']  # подключаем дополнительные настройки
    search_fields = ['title__iregex'] # поиск, поля для поиска , __iregex не зависит от регистра
    list_filter = ['cat__name', 'is_published'] # фильтр по категориям и по публикациям,
    # cat__name так как категория отдельный модуль а вызывается в блоге то нужно присваивать еще имя
    save_on_top = True # кнопки сохранить сверху и снизу


    @admin.display(description='Фото', ordering='content')
    def post_photo(self, blog: Blog):
        """отображение фото в статьях"""
        if blog.photo:
            return mark_safe(f"<img src='{blog.photo.url}' width=50")
        return 'без фото '

    @admin.action(description='Опубликовать')
    def set_published(self, request, queryset):
        """в админке добавляем действе , опубликованные
            статусы описаны в моделях
        """
        count = queryset.update(is_published=Blog.Status.PUBLICHED)
        self.message_user(request, f'Опубликовано {count} записей')

    @admin.action(description='Убрать публикацию')
    def set_draft(self, request, queryset):
        """в админке добавляем действе , не опубликованные
            статусы описаны в моделях
            messages.WARNING другой значек
        """
        count = queryset.update(is_published=Blog.Status.DRAFT)
        self.message_user(request, f'снято с публикации {count} записей', messages.WARNING)


@admin.register(Category)  # регистрация приложения
class CategoryAdmin(admin.ModelAdmin):
    """
    настройка даминки категории
    """
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(TagPost)  # регистрация приложения
class TagAdmin(admin.ModelAdmin):
    """
    настройка даминки теги
    """
    list_display = ('tag',)
    list_display_links = ('tag',)


@admin.register(Comment)  # регистрация приложения
class CommentAdmin(admin.ModelAdmin):
    """
    настройка даминки категории
    """
    list_display = ('name', 'content')
    list_display_links = ('name', 'content')

# admin.site.register(Comment)  # регистрация приложения в админке, регистрация блога
