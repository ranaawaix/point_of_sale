from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from POS.models import Store
from user_accounts.models import User
from django.contrib.auth.forms import PasswordChangeForm


class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput())
    stores = forms.ModelMultipleChoiceField(queryset=Store.objects.all())

    class Meta:
        model = User
        fields = ['group', 'first_name', 'last_name', 'phone', 'gender', 'email', 'username', 'password1', 'password2',
                  'status', 'stores']
        widgets = {'group': forms.Select(attrs={'class': 'form-control', 'empty_label': '---Please Select---'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name...'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name...'}),
                   'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number...'}),
                   'gender': forms.Select(attrs={'class': 'form-control', 'empty_label': '---Please Select---'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email...'}),
                   'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username...'}),
                   'status': forms.Select(attrs={'class': 'form-control', 'empty_label': '---Please Select---'}),
                   'stores': forms.SelectMultiple(attrs={'class': 'form-control', 'empty_label': '---Please Select---'}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter a password...'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Enter password again...'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control text-center'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username...'
        self.fields['password'].widget.attrs['class'] = 'form-control text-center'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password...'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'gender', 'group', 'username', 'email', 'status']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control', 'empty_label': '---Please Select---'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name...'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number...'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'empty_label': '---Please Select---'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email...'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username...'}),
            'status': forms.Select(attrs={'class': 'form-control', 'empty_label': '---Please Select---'}),
            'store': forms.Select(attrs={'class': 'form-control', 'empty_label': '---Please Select---'}),
        }


class AvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base_fields['old_password'].widget.attrs['class'] = 'form-control'
        self.base_fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.base_fields['new_password2'].widget.attrs['class'] = 'form-control'

