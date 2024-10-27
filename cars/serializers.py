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
    cliente = serializers.ReadOnlyField(source='cliente.id')  # Define o campo como somente leitura
    class Meta:
        model = CarReservation
        fields = '__all__'

    def validate(self, data):
        # Pega os valores de `car`, `data_retirada`, `data_devolucao`, `hora_retirada` e `hora_devolucao` do novo pedido de reserva
        car = data.get('car')
        data_retirada = data.get('data_retirada')
        data_devolucao = data.get('data_devolucao')
        hora_retirada = data.get('hora_retirada')
        hora_devolucao = data.get('hora_devolucao')

        # Verifica se já existe uma reserva conflitante para o mesmo carro
        conflicting_reservations = CarReservation.objects.filter(
            car=car,
            data_devolucao__gte=data_retirada,  # A reserva existente termina após ou no início da nova reserva
            data_retirada__lte=data_devolucao    # A reserva existente começa antes ou no final da nova reserva
        ).exclude(id=self.instance.id if self.instance else None)  # Exclui a reserva atual se for uma atualização

        # Verifica se algum dos horários conflitantes coincide
        for reservation in conflicting_reservations:
            # Verifica se os horários se sobrepõem no mesmo dia
            if (reservation.data_retirada == data_retirada and reservation.hora_retirada < hora_devolucao) or \
               (reservation.data_devolucao == data_devolucao and reservation.hora_devolucao > hora_retirada) or \
               (reservation.data_retirada < data_devolucao and reservation.data_devolucao > data_retirada):
                raise serializers.ValidationError("Este carro já está reservado para o período selecionado.")

        return data