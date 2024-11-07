# autenticacao/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()  # Usando o modelo de usuário personalizado

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Lógica para criar o perfil do usuário aqui
        pass
