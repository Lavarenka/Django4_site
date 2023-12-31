# Generated by Django 4.2.1 on 2023-12-19 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blog_cat_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='blog.tagpost'),
        ),
    ]