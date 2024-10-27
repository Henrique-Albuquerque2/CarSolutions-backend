from django.db import models
from cars.models import Car
from django.conf import settings

# Create your models here.
# transactions/models.py
class CarTransaction(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('SALE', 'Venda'), ('RENT', 'Aluguel')])
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('COMPLETED', 'Concluído'), ('PENDING', 'Pendente')])

class CarReservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='transaction_car_reservations')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transaction_customer_reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.customer} - {self.car}"

    def save(self, *args, **kwargs):
        if not self.is_completed:
            self.car.is_available = False
            self.car.save()
        super().save(*args, **kwargs)
