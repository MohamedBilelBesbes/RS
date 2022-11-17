from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {forms.PasswordInput(attrs={'class': 'form-control', 'style':'background-color: #d0d4f5 !important;width: 40%;','placeholder':'Confirm Password ...'}),
        }


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UploadFileForm(forms.Form):
    file = forms.FileField()

class DownloadFileForm(forms.Form):
    brand_name = forms.CharField
    shop_id = forms.CharField
    item_id = forms.CharField
    start_date = forms.DateField
    end_date = forms.DateField