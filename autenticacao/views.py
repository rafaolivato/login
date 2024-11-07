# autenticacao/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.estabelecimento:
        contexto = {'estabelecimento': profile.estabelecimento}
        return render(request, 'dashboard.html', contexto)
    else:
        return redirect('associar_estabelecimento')  # Redireciona para a página de associação


from .models import Estabelecimento

@login_required
def associar_estabelecimento(request):
    if request.method == "POST":
        # Recupera o estabelecimento escolhido
        estabelecimento_id = request.POST.get("estabelecimento")
        estabelecimento = Estabelecimento.objects.get(id=estabelecimento_id)
        # Associa o estabelecimento ao perfil do usuário
        request.user.profile.estabelecimento = estabelecimento
        request.user.profile.save()
        return redirect('dashboard')  # Redireciona para o dashboard após a associação

    estabelecimentos = Estabelecimento.objects.all()
    return render(request, 'associar_estabelecimento.html', {'estabelecimentos': estabelecimentos})

# autenticacao/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)  # Logar o usuário após o registro
            return redirect('dashboard')  # Redireciona para a dashboard
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


# autenticacao/views.py
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.estabelecimento:
        context = {'estabelecimento': profile.estabelecimento}
        return render(request, 'dashboard.html', context)
    else:
        return redirect('register')  # Redireciona para o cadastro caso não tenha estabelecimento
