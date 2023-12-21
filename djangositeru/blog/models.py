from django.db import models
from django.urls import reverse
"""
модели для баз данных/
"""
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

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True ) # чпу , для урл
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLICHED)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts') # связываем категории, PROTECT запрещает удаление если есть посты
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

    objects = models.Manager()
    published = PublishedManager() #вызываем класс со статьями
    def __str__(self):
        return self.title

    class Meta:
        # сортировка по созданию запии
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        """вывод текущей записи по слагу """
        return reverse('post', kwargs={'post_slug': self.slug})

class Category(models.Model):
    """
    создаем категории
    """
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """вывод текущей записи по слагу """
        return reverse('category', kwargs={'cat_slug': self.slug})


class Comment(models.Model):
    """создаем коменты и подключаем к посту
        нужно еще добавить дату
    """

    name = models.CharField(max_length=100)
    content = models.TextField()
    com = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return self.name



class TagPost(models.Model):
    """
    тэги
    """
    tag = models.CharField(max_length=100,db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        """вывод текущей записи по слагу """
        return reverse('tag', kwargs={'tag_slug': self.slug})