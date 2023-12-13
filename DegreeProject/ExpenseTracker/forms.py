from django import forms
from .models import Category, Expense
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control',}))
    email = forms.EmailField(max_length=100,required=True, widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'form-control',}))
    password1 = forms.CharField(max_length=100,required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control',}))
    password2 = forms.CharField(max_length=100,required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control',}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control',}))
    password = forms.CharField(max_length=50,required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control', 'data-toggle': 'password','id': 'password','name': 'password',}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class ExpenseForm(forms.ModelForm):
    #date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'description']





