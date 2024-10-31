from django.shortcuts import render

# Create your views here.
# cars/views.py
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from .models import Car, CarReservation
from .serializers import CarSerializer, CarListSerializer, CarReservationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsFuncionario  # Importa a permissão personalizada

# cars/views.py

from rest_framework.views import APIView
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Car, CarReservation
from .serializers import CarSerializer, CarListSerializer, CarReservationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsFuncionario  # Permissão personalizada


class CarViewSet(APIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['marca', 'categoria', 'tipo_de_produto', 'is_disponivel']
    search_fields = ['modelo', 'marca']
    # views.py
class CarViewSet(APIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['marca', 'categoria', 'preco_venda', 'preco_diaria', 'tipo_de_produto']
    search_fields = ['modelo', 'marca']

    # Outras permissões e métodos get/post/patch já implementados anteriormente.


    def get_permissions(self):
        if self.request.method == 'GET':
            # Permitir acesso a qualquer usuário para GET
            return [permissions.AllowAny()]
        else:
            # Restringir acesso a funcionários para métodos POST, PATCH, DELETE
            return [IsFuncionario()]
        
    def get(self, request):
        # Lista todos os carros se funcionário, caso contrário, apenas carros disponíveis
        if request.user.is_authenticated and request.user.isfuncionario:
            cars = Car.objects.all()
        else:
            cars = Car.objects.filter(is_disponivel=True)
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        print('entro no post')
        if not self.get_permissions():  # Verifica a permissão de adicionar
            return Response({'message': 'Você não tem permissão para realizar esta ação!'}, status=403)
        print('passou da verificação do post')
        serializer = CarSerializer(data=request.data)
        print('passou da criação do serializer')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Carro cadastrado com sucesso!'}, status=201)
        print('não foi validado o serializer')
        print("Erros de validaçao: ", serializer.errors)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk=None):
        if not self.get_permissions():  # Verifica a permissão de alterar
            return Response({'message': 'Você não tem permissão para realizar esta ação!'}, status=403)
        
        car = get_object_or_404(Car, pk=pk)

        data = request.data.copy()

        if 'imagem' not in data:
            car_antigo = CarDetailView.get(self, request, pk=pk)
            data['imagem'] = car_antigo.data['imagem']
            
        serializer = CarSerializer(car, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Carro atualizado com sucesso!'}, status=200)
        print("Erros de validaçao: ", serializer.errors)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        print("entrou no delete")
        print(self.get_permissions())
        if not self.get_permissions():  # Verifica a permissão de deletar
            return Response({'message': 'Você não tem permissão para realizar esta ação!'}, status=403)
        print("passou da verificação de permissão")
        car = get_object_or_404(Car, pk=pk)
        car.delete()
        return Response({'message': 'Carro deletado com sucesso!'}, status=200)


class CarDetailView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'GET':
            # Permitir acesso a qualquer usuário para GET
            return [permissions.AllowAny()]
        
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CarReservationViewSet(viewsets.ModelViewSet):
    serializer_class = CarReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Funcionários veem todas as reservas, clientes veem apenas as próprias
        if self.request.user.isfuncionario:
            return CarReservation.objects.all()
        return CarReservation.objects.filter(cliente=self.request.user)

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

    
class AvailableCarsView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            # Permitir acesso a qualquer usuário para GET
            return [permissions.AllowAny()]
        
    def get(self, request):
        # Filtra os carros disponíveis (is_disponivel=True)
        available_cars = Car.objects.all().filter(is_disponivel=True)
        serializer = CarListSerializer(available_cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)