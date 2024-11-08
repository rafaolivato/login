# autenticacao/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login

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


from django.shortcuts import render, redirect
from .models import Medicamento, Estoque, Estabelecimento
from .forms import MedicamentoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def registrar_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            medicamento = form.save(commit=False)
            # Define o estabelecimento baseado no perfil do usuário logado
            if request.user.profile.estabelecimento:
                medicamento.estabelecimento = request.user.profile.estabelecimento
                medicamento.registrado_por = request.user
                medicamento.save()

                # Verifica se já existe um registro de estoque para esse medicamento e estabelecimento
                estoque, created = Estoque.objects.get_or_create(
                    medicamento=medicamento,
                    estabelecimento=request.user.profile.estabelecimento,
                    defaults={'quantidade': 0}  # Define a quantidade inicial como 0
                )

                if created:
                    messages.success(request, f"Estoque inicial criado para {medicamento.nome} com quantidade 0.")
                else:
                    messages.info(request, f"O estoque para {medicamento.nome} já existia e foi mantido.")

                return redirect('medicamento_lista')
            else:
                form.add_error(None, "Usuário não está associado a um estabelecimento.")
    else:
        form = MedicamentoForm()
    return render(request, 'registrar_medicamento.html', {'form': form})




from django.shortcuts import render
from .models import Medicamento

def medicamento_lista(request):
    # Obtém todos os medicamentos e seus estabelecimentos
    medicamentos = Medicamento.objects.select_related('estabelecimento').all()
    return render(request, 'medicamento_lista.html', {'medicamentos': medicamentos})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Estoque, Medicamento, Estabelecimento

def transferir_medicamento(request):
    if request.method == 'POST':
        medicamento_id = request.POST.get('medicamento')
        origem_id = request.POST.get('origem')
        destino_id = request.POST.get('destino')
        quantidade = int(request.POST.get('quantidade'))

        # Obter o estoque do estabelecimento de origem
        estoque_origem = Estoque.objects.filter(
            medicamento_id=medicamento_id, 
            estabelecimento_id=origem_id
        ).first()

        if estoque_origem and estoque_origem.quantidade >= quantidade:
            # Atualiza o estoque do estabelecimento de origem
            estoque_origem.quantidade -= quantidade
            estoque_origem.save()

            # Obter ou criar o estoque para o estabelecimento de destino
            estoque_destino, created = Estoque.objects.get_or_create(
                medicamento_id=medicamento_id, 
                estabelecimento_id=destino_id,
                defaults={'quantidade': 0}
            )
            estoque_destino.quantidade += quantidade
            estoque_destino.save()

            messages.success(request, 'Transferência realizada com sucesso.')
        else:
            estoque_disponivel = estoque_origem.quantidade if estoque_origem else 0
            messages.error(request, f'Estoque insuficiente no estabelecimento de origem. Estoque disponível: {estoque_disponivel}')

        return redirect('transferir_medicamento')

    medicamentos = Medicamento.objects.all()
    estabelecimentos = Estabelecimento.objects.all()
    return render(request, 'transferir_medicamento.html', {
        'medicamentos': medicamentos,
        'estabelecimentos': estabelecimentos,
    })
