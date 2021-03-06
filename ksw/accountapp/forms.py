from django import forms

from mainapp.models import Post


class PostForm(forms.ModelForm):
    """Форма. Создание статьи"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = Post
        fields = ['topic', 'annotation', 'article', 'category', 'image']
        exclude = ["author"]
        widgets = {'image': forms.FileInput()}
