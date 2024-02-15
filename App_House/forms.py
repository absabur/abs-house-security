from django import forms
from App_House.models import *

class CreateOwnerForm(forms.ModelForm):
    class Meta:
        model = HouseOwner
        fields = ('name', 'password_1', 'password_2',)
        labels = {
            'name': 'Name',
            'password_1': 'Password',
            'password_2': 'Confirm Password',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'password_1': forms.TextInput(attrs={'placeholder': 'Enter password', 'type': 'password'}),
            'password_2': forms.TextInput(attrs={'placeholder': 'Confirm your Password', 'type': 'password'}),
        }
        
class LockOpenForm(forms.ModelForm):
    class Meta:
        model = HouseOwner
        fields = ('password_1',)
        labels = {
            'password_1': 'Password',
        }
        widgets = {
            'password_1': forms.TextInput(attrs={'placeholder': 'Enter password', 'type': 'password'}),
        }

class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = HouseOwner
        fields = ('password_1', 'password_2',)
        labels = {
            'password_1': 'Password',
            'password_2': 'Confirm Password',
        }
        widgets = {
            'password_1': forms.TextInput(attrs={'placeholder': 'Enter new password', 'type': 'password'}),
            'password_2': forms.TextInput(attrs={'placeholder': 'Confirm new Password', 'type': 'password'}),
        }