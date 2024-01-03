from django import forms
from .models import Category, TagPost


class AddPostForm(forms.Form):
    """
    Добавление статьи
    .///789
    required=False // не обязательное поле
    empty_label // штатное название в выборе категории
    initial=True // чекбокс тру
    widget // присваиваем класс css
    """
    title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class':'form-input'}))
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False, label='Текст')
    is_published = forms.BooleanField(initial=True, label='Публикация' )
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label='Категория не выбрана' ,label='Категория')
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), required=False, label='Тэг')
