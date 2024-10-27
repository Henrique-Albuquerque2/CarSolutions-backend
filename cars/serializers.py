from rest_framework import serializers
from .models import Car, CarReservation

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class CarListSerializer(serializers.ModelSerializer):
    imagem = serializers.ImageField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'marca', 'modelo', 'ano', 'categoria',
                   'cambio', 'combustivel', 'cor', 'placa',
                   'preco_venda', 'preco_diaria', 'tipo_de_produto',
                     'imagem', 'is_disponivel']

class CarReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarReservation
        fields = '__all__'
