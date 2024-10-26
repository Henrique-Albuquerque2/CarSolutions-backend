from carSolutions.models import User, Profile

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "full_name", "cpf", "celular",
                   "nacionalidade", "cep", "numero", "complemento", "cidade", 
                   "estado", "rua", "bairro", "isfuncionario",'genero']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adiciona todas as informações do usuário ao token
        token["username"] = user.username
        token["email"] = user.email
        token["full_name"] = user.full_name
        token["cpf"] = user.cpf
        token["celular"] = user.celular
        token["nacionalidade"] = user.nacionalidade
        token["cep"] = user.cep
        token["numero"] = user.numero
        token["complemento"] = user.complemento
        token["cidade"] = user.cidade
        token["estado"] = user.estado
        token["rua"] = user.rua
        token["bairro"] = user.bairro
        token["isfuncionario"] = user.isfuncionario
        token["genero"] = user.genero

        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2", 
                  "full_name", "cpf", "celular", "nacionalidade", 
                  "cep", "numero", "complemento", "cidade", "estado",
                    "rua", "bairro", "isfuncionario", "genero"]
    
    def validate(self, attrs):
        # Verifica se as senhas são iguais
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Senhas não são iguais."})
        return attrs

    def create(self, validated_data):
        # Remove password2, pois não é necessário para criar o usuário
        validated_data.pop("password2")
        
        # Criação do usuário com a senha validada
        user = User.objects.create_user(**validated_data)
        
        # Define a senha usando set_password
        user.set_password(validated_data["password"])
        user.save()

        return user

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.refresh_token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.refresh_token)
            token.blacklist()  # Adiciona o token na lista negra
        except Exception as e:
            raise serializers.ValidationError("Token inválido ou já expirado.")
