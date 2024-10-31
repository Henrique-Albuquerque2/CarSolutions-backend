from django.db import models
from django.conf import settings

class Lembrete(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateField()
    categoria = models.CharField(
        max_length=50,
        choices=[("Reunião", "Reunião"), ("Urgente", "Urgente"), ("Notícia", "Notícia"), ("Geral", "Geral"), ("Tarefas Diárias", "Tarefas Diárias")],
    )
    criador = models.CharField(max_length=255)  # Armazena o nome completo
    status_ok = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-data_criacao']
