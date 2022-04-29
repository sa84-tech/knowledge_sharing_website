from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import WriterUser, WriterUserProfile
from django import forms
import hashlib
import random


class WriterUserLoginForm(AuthenticationForm):
    class Meta:
        model = WriterUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(WriterUserLoginForm, self).__init__(*args,**kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'


class WriterUserRegisterForm(UserCreationForm):
    class Meta:
        model = WriterUser
        fields = ('username', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super(WriterUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['id'] = f'reg_{field_name}'

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 0:
            raise forms.ValidationError("Возраст указан не верно")
        return data

    def save(self, *args, **kwargs):
        user = super(WriterUserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class WriterUserEditForm(UserChangeForm):
    class Meta:
        model = WriterUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super(WriterUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['id'] = f'reg_{field_name}'

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 0:
            raise forms.ValidationError("Возраст указан не верно")
        return data


class WriterUserProfileForm(forms.ModelForm):

    class Meta:
        model = WriterUserProfile
        fields = ('tagline', 'about_me', 'country', 'gender')

    def __init__(self, *args, **kwargs):
        super(WriterUserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['id'] = f'reg_{field_name}'
