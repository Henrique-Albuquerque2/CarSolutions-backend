from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=300)
    cpf = models.CharField(max_length=11)
    celular = models.CharField(max_length=11)
    nacionalidade = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=50)
    genero = models.CharField(max_length=10, choices=[("M", "Masculino"), ("F", "Feminino"), ("O", "Outros")])
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    isfuncionario = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwags):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)