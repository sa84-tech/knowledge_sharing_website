from django import forms


class CommentForm(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea)


class ContentForm(forms.Form):
    target_type = forms.CharField()
    target_id = forms.IntegerField()
    post_id = forms.IntegerField()
    btn_type = forms.CharField()
