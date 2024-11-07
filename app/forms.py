
from django import forms
from django.contrib.auth.forms import UserCreationForm

from app.models import Reservation, Table, User, coffeemenu


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )

class signUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password1= forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password2= forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'is_customer', 'is_employee', 'is_admin')
        widgets = {
            'password': forms.PasswordInput(),
        }        

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','is_admin', 'is_customer', 'is_employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'autocomplete': 'new-password'})    

class UserFormUp(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']        

        
class CoffeemenuForm(forms.ModelForm):
    class Meta:
        model = coffeemenu
        fields = ['name', 'price', 'description', 'image','available']      

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'reservation_time','is_reserved']
        widgets = {
            'reservation_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }     
     