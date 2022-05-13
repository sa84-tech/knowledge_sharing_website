from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django_countries.fields import CountryField

from .models import WriterUser, WriterUserProfile
from django import forms
import hashlib
import random

# from django.utils.translation import gettext as _


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
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(WriterUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['id'] = f'reg_{field_name}'

    def save(self, *args, **kwargs):
        user = super(WriterUserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class DatesInput(forms.DateInput):
    input_type = 'date'


class WriterUserEditForm(UserChangeForm):
    class Meta:
        model = WriterUser
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'password', 'birthday')
        widgets = {'birthday': DatesInput()}

    def __init__(self, *args, **kwargs):
        super(WriterUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['id'] = f'reg_{field_name}'

    # def clean_age(self):
    #     data = self.cleaned_data['age']
    #     if data < 0:
    #         raise forms.ValidationError("Возраст указан не верно")
    #     return data


class WriterUserProfileForm(forms.ModelForm):

    class Meta:
        model = WriterUserProfile
        fields = ('tagline', 'about_me', 'country', 'gender')
        country = CountryField(blank_label='(select country)')

    def __init__(self, *args, **kwargs):
        super(WriterUserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['id'] = f'reg_{field_name}'


class PassChangeForm(PasswordChangeForm):
    class Meta:
        model = WriterUser

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class EmailChangeForm(forms.Form):
    error_messages = {
        'email_mismatch': "Два поля адреса электронной почты не совпадают.",
        'email_inuse': "Данный адрес электронной почты уже используется. Введите другой адрес",
        'password_incorrect': "Неверный пароль.",
    }

    current_password = forms.CharField(
        label="Текущий пароль",
        widget=forms.PasswordInput,
        required=True
    )

    new_email1 = forms.EmailField(
        label="Новый email",
        max_length=254,
        required=True
    )

    new_email2 = forms.EmailField(
        label="Подтвердите новый email",
        max_length=254,
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise forms.ValidationError(self.error_messages['password_incorrect'], code='password_incorrect',)
        return current_password

    def clean_new_email1(self):
        email1 = self.cleaned_data.get('new_email1')
        if WriterUser.objects.filter(email=email1).count() > 0:
            raise forms.ValidationError(self.error_messages['email_inuse'], code='email_inuse',)
        return email1

    def clean_new_email2(self):
        email1 = self.cleaned_data.get('new_email1')
        email2 = self.cleaned_data.get('new_email2')
        if email1 and email2:
            if email1 != email2:
                raise forms.ValidationError(self.error_messages['email_mismatch'], code='email_mismatch',)
        return email2

    def save(self, commit=True):
        self.user.email = self.cleaned_data['new_email1']
        if commit:
            self.user.save()
        return self.user
