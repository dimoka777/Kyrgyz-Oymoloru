from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, OfficeRegion
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label=False, error_messages={'required': "Это поле пустое"}, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ФИО'}))

    address = forms.CharField(label=False, error_messages={'required': "Это поле пустое"}, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Адрес'}))
    check_number = forms.CharField(label=False, error_messages={'required': "Это поле пустое"}, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Номер чека'}))
    check_image = forms.ImageField(label='Фото чека', error_messages={'required': "Это поле пустое"}, required=True, widget=forms.FileInput, )
    passport_number = forms.CharField(label=False, error_messages={'required': "Это поле пустое"}, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Номер паспорта'}))
    office_location = forms.ModelChoiceField(label=False, error_messages={'required': "Это поле пустое"}, queryset=OfficeRegion.objects.all(),
                                             empty_label="Выберите регион", required=True,
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label=False, error_messages={'required': "Это поле пустое"}, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}))
    by_whom = forms.ModelChoiceField(label=False, queryset=CustomUser.objects.all(),
                                     empty_label="От кого", required=False,
                                     widget=forms.Select(attrs={'class': 'form-control', 'data-plugin': 'select2',
                                                                'data-minimum-input-length': '1'}))
    password1 = forms.CharField(label=False, error_messages={'required': "Это поле пустое"}, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Пароль'}),)
    password2 = forms.CharField(label=False, error_messages={'required': "Это поле пустое"}, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['by_whom'].queryset = CustomUser.objects.filter(level=1, status=True)
        # .values_list('full_name', flat=True).distinct()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username', 'address', 'check_number', 'check_image',
                                                 'passport_number', 'office_location', 'phone_number', 'by_whom',)

    def clean_username(self):
        username = self.cleaned_data['username']
        r = CustomUser.objects.filter(username=username)
        if r.count():
            raise ValidationError("Бундай логин бош эмес")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Сырсөз тастыкталбай калды")

        return password2


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = UserCreationForm.Meta.fields + ('username', 'full_name', 'address', 'check_number', 'check_image',
#                                                  'passport_number', 'office_location', 'phone_number',
#                                                  'by_whom', 'is_staff')

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['by_whom'].queryset = CustomUser.objects.filter(level=1, status=True)

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'username', 'address', 'check_number', 'check_image', 'is_staff',
            'passport_number', 'office_location', 'phone_number', 'status',
            'by_whom')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
        }
    ))
