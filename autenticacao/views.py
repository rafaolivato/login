# Create your views here.
# autenticacao/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.estabelecimento:
        context = {'estabelecimento': profile.estabelecimento}
        return render(request, 'dashboard.html', context)
    else:
        return redirect('login')  # Ou outra página de erro
