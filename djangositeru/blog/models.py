from django.db import models
"""
модели для баз данных/
"""
# Create your models here.

class Blog(models.Model):
    """
    id формируется автоматически
    blank=True // не обязательное поле
    auto_now_add=True // Изменения только в первый момент записи
    auto_now=True // меняется при редактировании
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
