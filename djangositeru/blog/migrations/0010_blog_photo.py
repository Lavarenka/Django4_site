# Generated by Django 4.2.1 on 2024-01-03 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_uploadfiles_alter_blog_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d', verbose_name='Фото'),
        ),
    ]
