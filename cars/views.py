from django.shortcuts import render

# Create your views here.
# cars/views.py
from rest_framework import viewsets, permissions, filters
from .models import Car, CarReservation
from .serializers import CarSerializer, CarListSerializer, CarReservationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsFuncionario  # Importa a permissão personalizada

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsFuncionario()]  # Usa a permissão personalizada
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CarListSerializer if not self.request.user.is_staff else CarSerializer
        return CarSerializer

class CarReservationViewSet(viewsets.ModelViewSet):
    queryset = CarReservation.objects.all()
    serializer_class = CarReservationSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]  # Somente usuários autenticados podem reservar
        return [permissions.AllowAny()]
    
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['marca', 'categoria', 'tipo_de_produto', 'is_disponivel']
    search_fields = ['modelo', 'marca']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CarListSerializer if self.request.user.is_authenticated and not self.request.user.is_staff else CarSerializer
        return CarSerializer
