from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from .models import Car, CarReservation
from .serializers import CarSerializer, CarListSerializer, CarReservationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsFuncionario  # Importa a permissão personalizada
from django.db.models import Q
from django.shortcuts import get_object_or_404


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
            cars = Car.objects.all(is_disponivel=False)
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not self.get_permissions():  # Verifica a permissão de adicionar
            return Response({'message': 'Você não tem permissão para realizar esta ação!'}, status=403)
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Carro cadastrado com sucesso!'}, status=201)
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
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        print(self.get_permissions())
        if not self.get_permissions():  # Verifica a permissão de deletar
            return Response({'message': 'Você não tem permissão para realizar esta ação!'}, status=403)
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

class AvailableCarsByDateView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Obtém as datas e horas de retirada e devolução dos parâmetros da requisição
        data_retirada = self.request.query_params.get('dataRetirada')
        data_devolucao = self.request.query_params.get('dataDevolucao')
        hora_retirada = self.request.query_params.get('horaRetirada')
        hora_devolucao = self.request.query_params.get('horaDevolucao')

        # Filtra para exibir apenas carros disponíveis inicialmente
        queryset = Car.objects.filter(is_disponivel=False)

        # Exclui carros que estão reservados no período fornecido
        if data_retirada and data_devolucao:
            queryset = queryset.exclude(
                Q(car_reservations__data_retirada__lte=data_devolucao) &
                Q(car_reservations__data_devolucao__gte=data_retirada)
            )

        return queryset
class AvailableCarsView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]  # Permite acesso público a este endpoint

    def get_queryset(self):
        queryset = Car.objects.filter(is_disponivel=False)  # Começa com apenas carros disponíveis
        
        # Filtrar por marca, se fornecido
        marca = self.request.query_params.get('marca', None)
        if marca:
            queryset = queryset.filter(marca__icontains=marca)
        
        # Filtrar por tipos de produto (Aluguel, Venda, Aluguel e Venda), se fornecido
        tipos_produto = self.request.query_params.getlist('tipoProduto')
        if tipos_produto:
            queryset = queryset.filter(tipo_de_produto__in=tipos_produto)
        
        # Filtrar por categorias (SUV, Sedan, etc.), se fornecido
        categorias = self.request.query_params.getlist('categorias')
        if categorias:
            queryset = queryset.filter(categoria__in=categorias)
        
        # Filtrar por faixa de preço para aluguel
        preco_min_aluguel = self.request.query_params.get('precoMinAluguel', None)
        preco_max_aluguel = self.request.query_params.get('precoMaxAluguel', None)
        if preco_min_aluguel:
            queryset = queryset.filter(preco_diaria__gte=preco_min_aluguel)
        if preco_max_aluguel:
            queryset = queryset.filter(preco_diaria__lte=preco_max_aluguel)
        
        # Filtrar por faixa de preço para venda
        preco_min_venda = self.request.query_params.get('precoMinVenda', None)
        preco_max_venda = self.request.query_params.get('precoMaxVenda', None)
        if preco_min_venda:
            queryset = queryset.filter(preco_venda__gte=preco_min_venda)
        if preco_max_venda:
            queryset = queryset.filter(preco_venda__lte=preco_max_venda)
        
        return queryset
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        reservation = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(CarReservation.STATUS_CHOICES):
            reservation.status = new_status
            reservation.save()
            return Response({'status': 'Status atualizado com sucesso'}, status=status.HTTP_200_OK)
        return Response({'error': 'Status inválido'}, status=status.HTTP_400_BAD_REQUEST)
class UserReservationsView(generics.ListAPIView):
    serializer_class = CarReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CarReservation.objects.filter(cliente=self.request.user)

class AllReservationsView(generics.ListAPIView):
    serializer_class = CarReservationSerializer
    permission_classes = [IsFuncionario]

    def get_queryset(self):
        return CarReservation.objects.all()
