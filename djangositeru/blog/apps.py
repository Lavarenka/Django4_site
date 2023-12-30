from django.apps import AppConfig


class BlogConfig(AppConfig):
    verbose_name = 'Мой блог'  # название блога в админке
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
