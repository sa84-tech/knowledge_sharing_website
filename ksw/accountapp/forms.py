from django import forms

from mainapp.models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    class Meta:
        model = Post
        fields = ['topic', 'annotation', 'article', 'category', 'image', 'status']
        exclude = ["author"]


