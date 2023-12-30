from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

"""
модели для баз данных/
"""


# def translit_to_eng(s: str) -> str:
#     """Функция для слага """
#     d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
#          'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
#          'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
#          'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
#          'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}
#
#     return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))

# Create your models here.
class PublishedManager(models.Manager):
    """
    возвращает все опубликованные статьи
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_published=Blog.Status.PUBLICHED)


class Blog(models.Model):
    """
    id формируется автоматически
    blank=True // не обязательное поле
    auto_now_add=True // Изменения только в первый момент записи
    auto_now=True // меняется при редактировании
    unique=True // уникальность
    """

    class Status(models.IntegerChoices):
        # для публикаций
        DRAFT = 0, 'Черновик'
        PUBLICHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')  # чпу , для урл
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLICHED, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts',
                            verbose_name='Категории')  # связываем категории, PROTECT запрещает удаление если есть посты
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')

    objects = models.Manager()
    published = PublishedManager()  # вызываем класс со статьями

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статьи'  # название блога в админке
        verbose_name_plural = 'Статьи'  # название блога в админке во множественном числе
        # сортировка по созданию запии
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        """вывод текущей записи по слагу """
        return reverse('post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs):
    #     """функия на автоматическое создание слага"""
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)

class Category(models.Model):
    """
    создаем категории
    """
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'  # название Категории в админке
        verbose_name_plural = 'Категории'  # название Категории в админке во множественном числе

    def get_absolute_url(self):
        """вывод текущей записи по слагу """
        return reverse('category', kwargs={'cat_slug': self.slug})


class Comment(models.Model):
    """создаем коменты и подключаем к посту
        нужно еще добавить дату
    """

    name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    content = models.TextField(verbose_name='Текст')
    com = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комментарий'  # название Категории в админке
        verbose_name_plural = 'Комментарии'  # название Категории в админке во множественном числе


class TagPost(models.Model):
    """
    тэги
    """
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тэг'  # название Тега в админке
        verbose_name_plural = 'Тэги'  # название Тега в админке во множественном числе

    def get_absolute_url(self):
        """вывод текущей записи по слагу """
        return reverse('tag', kwargs={'tag_slug': self.slug})
