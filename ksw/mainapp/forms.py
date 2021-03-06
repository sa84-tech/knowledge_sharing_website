from django import forms


class CommentForm(forms.Form):
    """Форма комментария"""

    text = forms.CharField(widget=forms.Textarea)
    target_type = forms.CharField()
    target_id = forms.IntegerField()
    post_id = forms.IntegerField()


class ContentForm(forms.Form):
    """Форма для меток (Лайк, Закладка)"""

    target_type = forms.CharField()
    target_id = forms.IntegerField()
    post_id = forms.IntegerField()
    btn_type = forms.CharField()
