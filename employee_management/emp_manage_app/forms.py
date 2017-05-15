from django.forms import ModelForm, TextInput
from employee_management.emp_manage_app.models import User, EmployeeSchedule
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


class signupform1(ModelForm):
    class Meta:
        model = User
        fields = ['fullname','email', 'phone_number']


class signupform2(ModelForm):
    class Meta:
        model = User
        fields = ['no_of_employees', 'password']
        widgets = {'password': forms.PasswordInput()}


class addsubuser(ModelForm):
    class Meta:
        model = User
        fields = ['fullname','email', 'password', 'phone_number', 'user_avatar']
        widgets = {'password': forms.PasswordInput()}

class addschedule(ModelForm):
    class Meta:
        model = EmployeeSchedule
        fields=['availability']

