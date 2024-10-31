from rest_framework import serializers
from .models import Lembrete

class LembreteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lembrete
        fields = ['id', 'titulo', 'descricao', 'data_criacao', 'data_expiracao', 'categoria', 'criador', 'status_ok']
        read_only_fields = ['data_criacao', 'criador', 'status_ok']
