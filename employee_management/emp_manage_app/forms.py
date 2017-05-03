from django.forms import ModelForm, TextInput
from employee_management.emp_manage_app.models import User
from django import forms
from django.contrib.auth import authenticate

class userform(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {'password': forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super(userform, self).__init__(*args, **kwargs)
        self.fields['email'].widget = TextInput(attrs={
            'id': 'emailID',
            'placeholder': 'Enter Your email',

        })
