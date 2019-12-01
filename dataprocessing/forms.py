from django import forms
from .models import User, Domain, Items, Data, Relation
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name' )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ('name', 'user')


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('name', 'domain')

class RelationForm(forms.ModelForm):
    class Meta:
        model = Relation
        fields = ('item1', 'item2', 'relation')

class UploadFileForm(forms.Form):
    file = forms.FileField()

class LoginForm(forms.Form):

    """Форма для входа в систему
    """
    username = forms.CharField()
    password = forms.CharField()