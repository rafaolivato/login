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
from .models import Medicamento, Estoque
from .forms import MedicamentoForm
from django.contrib.auth.decorators import login_required

@login_required
def registrar_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            medicamento = form.save(commit=False)
            # Define o estabelecimento baseado no perfil do usuário logado
            if request.user.profile.estabelecimento:
                medicamento.estabelecimento = request.user.profile.estabelecimento
                medicamento.registrado_por = request.user  # Registra o usuário logado
                medicamento.save()
                
                # Criar estoque inicial para o medicamento no estabelecimento
                Estoque.objects.create(
                    medicamento=medicamento,
                    estabelecimento=request.user.profile.estabelecimento,
                    estoque=0  # Inicialmente com 0, pode ser ajustado conforme necessário
                )
                
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

from django.contrib import messages  # Importe o módulo de mensagens
from django.shortcuts import render, redirect
from .models import Estoque, Medicamento, Estabelecimento
from django.contrib.auth.decorators import login_required

@login_required
def transferir_medicamento(request):
    if request.method == 'POST':
        medicamento_id = request.POST.get('medicamento')
        origem_id = request.POST.get('origem')
        destino_id = request.POST.get('destino')
        quantidade = int(request.POST.get('quantidade'))

        # Busca o estoque do estabelecimento de origem
        estoque_origem = Estoque.objects.filter(medicamento_id=medicamento_id, estabelecimento_id=origem_id).first()

        if estoque_origem and estoque_origem.estoque >= quantidade:
            # Atualiza o estoque de origem
            estoque_origem.estoque -= quantidade
            estoque_origem.save()

            # Verifica se já existe estoque no estabelecimento de destino
            estoque_destino = Estoque.objects.filter(medicamento_id=medicamento_id, estabelecimento_id=destino_id).first()

            if estoque_destino:
                # Se já existir, apenas atualiza o estoque
                estoque_destino.estoque += quantidade
                estoque_destino.save()
            else:
                # Se não existir, cria um novo estoque para o estabelecimento de destino
                Estoque.objects.create(
                    medicamento_id=medicamento_id,
                    estabelecimento_id=destino_id,
                    estoque=quantidade
                )

            messages.success(request, 'Transferência realizada com sucesso!')
            return redirect('transferencia_sucesso')  # Redireciona para uma página de sucesso
        else:
            messages.error(request, 'Estoque insuficiente ou não encontrado para o estabelecimento de origem.')
            return redirect('transferir_medicamento')  # Redireciona para a mesma página em caso de erro

    # Passa os medicamentos e estabelecimentos para o template
    medicamentos = Medicamento.objects.all()
    estabelecimentos = Estabelecimento.objects.all()
    return render(request, 'transferir_medicamento.html', {
        'medicamentos': medicamentos,
        'estabelecimentos': estabelecimentos
    })






