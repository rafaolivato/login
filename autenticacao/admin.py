from django.contrib import admin


from .models import Estabelecimento, Medicamento, Estoque

@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco')  # campos que você quer ver no painel do admin

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'validade', 'estabelecimento', 'registrado_por')
    search_fields = ('nome', 'estabelecimento__nome', 'registrado_por__username')
    list_filter = ('estabelecimento', 'validade', 'registrado_por')


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('medicamento', 'estabelecimento', 'estoque')
    search_fields = ('medicamento__nome', 'estabelecimento__nome')






