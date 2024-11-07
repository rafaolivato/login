# autenticacao/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Estabelecimento,Medicamento

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


from django import forms
from .models import Medicamento, Estabelecimento

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome', 'quantidade', 'validade']

    # Adiciona o campo 'estabelecimento' para não ser exibido no formulário
    estabelecimento = forms.ModelChoiceField(
        queryset=Estabelecimento.objects.all(),
        required=False,  # Não precisa ser preenchido pelo usuário
        widget=forms.HiddenInput()  # Deixa o campo oculto no formulário
    )

    def save(self, commit=True, request=None):
        medicamento = super().save(commit=False)
        if self.instance.pk is None:  # Se o objeto for novo
            if request:
                # Define o estabelecimento baseado no perfil do usuário logado
                medicamento.estabelecimento = request.user.profile.estabelecimento
                medicamento.registrado_por = request.user
        if commit:
            medicamento.save()
        return medicamento

