from django.contrib import admin


from .models import Estabelecimento, Medicamento

@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco')  # campos que você quer ver no painel do admin

# admin.py
from django.contrib import admin
from .models import Medicamento

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade', 'validade', 'estabelecimento', 'registrado_por')
    search_fields = ('nome', 'estabelecimento__nome', 'registrado_por__username')
    list_filter = ('estabelecimento', 'validade', 'registrado_por')



