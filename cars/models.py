from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Car(models.Model):
    CATEGORY_CHOICES = [
        ('SUV', 'SUV'),
        ('SEDAN', 'Sedan'),
        ('CAMINHONETES', 'Caminhonetes'),
        ('OUTROS', 'Outros'),
    ]

    AVAILABILITY_CHOICES = [
        ('Aluguel', 'Somente para Aluguel'),
        ('Venda', 'Somente para Venda'),
        ('Aluguel e Venda', 'Para Aluguel e Venda'),
    ]

    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.PositiveIntegerField()
    categoria = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preco_diaria = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    tipo_de_produto = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='Aluguel e Venda')
    imagem = models.ImageField(upload_to='car_images/')  # Diretório para armazenamento das imagens
    cambio = models.CharField(max_length=20)
    combustivel = models.CharField(max_length=20)
    cor = models.CharField(max_length=20)
    placa = models.CharField(max_length=7)
    is_disponivel = models.BooleanField(default=True)

    data_publicado = models.DateTimeField(auto_now_add=True)
    data_atualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.marca} {self.model} ({self.ano})"

class CarReservation(models.Model):

    LOCATION_CHOICES = [
        ('Congonhas', 'Aeroporto de congonhas (CGH)'),
        ('Guarulhos', 'Aeroporto de Guarulhos (GRU)'),
    ]

    STATUS_CHOICES = [
        ('em_breve', 'Em Breve'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_reservations')
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_reservations')
    data_retirada = models.DateField()
    hora_retirada = models.TimeField()  # Hora de retirada
    data_devolucao = models.DateField()
    hora_devolucao = models.TimeField()  # Hora de devolução
    local_retirada = models.CharField(max_length=100, choices= LOCATION_CHOICES)  # Local de retirada
    local_devolucao = models.CharField(max_length=100, choices= LOCATION_CHOICES)  # Local de devolução
    is_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_breve')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.cliente} - {self.car}"

    def save(self, *args, **kwargs):
        if not self.is_completed:
            self.car.is_available = False
            self.car.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.car.is_disponivel = True
        self.car.save()
        super().delete(*args, **kwargs)


