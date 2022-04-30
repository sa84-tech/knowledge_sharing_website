from django import forms


class CommentForm(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea)


class LikeForm(forms.Form):
    target_type = forms.CharField()
    target_id = forms.IntegerField()
