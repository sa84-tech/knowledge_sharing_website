from django import forms


class CommentForm(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea)
