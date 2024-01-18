from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .models import Category, TagPost, Blog, Comment


class AddPostForm(forms.ModelForm):
    """
    Добавление статьи
    required=False // не обязательное поле
    empty_label // штатное название в выборе категории
    initial=True // чекбокс тру
    widget // присваиваем класс css
    error_messages // валидатор, описание ошибок, ключ такой же как и
    параметр НА СТОРОНЕ СЕРВЕРА
    """

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')

    class Meta:
        """
        подключаем к форме модели
        fields // перечисляем поля + их порядок
        """
        model = Blog
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            # подключаем виджеты , стили
            'titile': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50}),
        }

    def clean_title(self):
        """
        предпреждение для титла , можно дописать для остальных полей
        :return:
        """
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длинна болше писятки')
        return title

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите Имя', 'class': 'form-label input-group-text' }),
            'content': forms.Textarea(attrs={'placeholder': 'Комментарий', 'class': 'form-label input-group-text'}),
        }


class UploadFileForm(forms.Form):
    """для загрузки файлов, описан в about"""
    file = forms.ImageField(label='Файл')
