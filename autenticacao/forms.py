# autenticacao/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Estabelecimento

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# autenticacao/forms.py
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['estabelecimento']


# forms.py
from django import forms
from .models import Medicamento

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome', 'quantidade', 'validade']
