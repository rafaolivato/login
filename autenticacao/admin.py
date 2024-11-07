from django.contrib import admin


from .models import Estabelecimento

@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco')  # campos que você quer ver no painel do admin
