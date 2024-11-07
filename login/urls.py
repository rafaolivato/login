from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from autenticacao import views  # Certifique-se de que este é o caminho correto


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('associar_estabelecimento/', views.associar_estabelecimento, name='associar_estabelecimento'),
    path('registrar_medicamento/', views.registrar_medicamento, name='registrar_medicamento'),
    path('medicamentos/', views.medicamento_lista, name='medicamento_lista'),  # URL para a lista de medicamentos
    path('registrar_medicamento/', views.registrar_medicamento, name='registrar_medicamento'),
    path('transferir_medicamento/', views.transferir_medicamento, name='transferir_medicamento'),
]


