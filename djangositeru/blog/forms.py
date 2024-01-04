from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .models import Category, TagPost, Blog


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
    # title = forms.CharField(max_length=255,
    #                         min_length=5,
    #                         label='Заголовок',
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         error_messages={
    #                             'min_length': 'Маловимволов',
    #                             'max_length': 'Много символов',
    #                             'required': 'без заголовка никак', #required если пустое поле
    #                         }
    #
    #                         )
    # slug = forms.SlugField(max_length=255, validators=[
    #     MinLengthValidator(5, message='минимум 5'),
    #     MaxLengthValidator(20, message='максимум 20')
    # ])
    # content = forms.CharField(widget=forms.Textarea(), required=False, label='Текст')
    # is_published = forms.BooleanField(initial=True, label='Публикация')
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
    # tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), required=False, label='Тэг')

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


class UploadFileForm(forms.Form):
    """для загрузки файлов, описан в about"""
    file = forms.ImageField(label='Файл')
