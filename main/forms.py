from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Todo

class RegisterForm(UserCreationForm):
    """Form that allows users to register for an account"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2'] # creating form fields
        
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','description','due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type':'date'}),
        }