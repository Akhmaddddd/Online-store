from django import forms
from .models import Product, Comment, Profile,ShippingAddress,Customer
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'content', 'photo', 'category', 'price')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название продукта'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена продукта'
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Логин'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Потвердите пароль'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Логин'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Фамилия'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Почта'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control'

            })
        }


class EditAccountForm(UserChangeForm):
    old_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    username = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'old_password', 'new_password', 'confirm_password')


class EditProfileForm(forms.ModelForm):
    photo = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Profile
        fields = ['photo', 'phone', 'address']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form_control contact__section-input',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form_control contact__section-input',
                'placeholder': 'Фамилия'
            })
        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'region', 'phone']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form_control contact__section-input',
                'placeholder': 'Адрес ул. дом. кв.'
            }),
            'city': forms.Select(attrs={
                'class': 'form_select contact__section-input',
                'placeholder': 'Выберите Город'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form_control contact__section-input',
                'placeholder': 'Регион'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form_control contact__section-input',
                'placeholder': 'Номер телефона'
            })
        }
