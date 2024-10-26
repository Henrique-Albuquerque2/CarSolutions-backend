from carSolutions.models import User, Profile

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "full_name", "cpf", "celular",
                   "nacionalidade", "cep", "numero", "complemento", "cidade", 
                   "estado", "rua", "bairro", "isfuncionario",'genero']

class MyTokenObtainPairSerializer (TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email
        token["isfuncionario"] = user.isfuncionario
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
        token["genero"] = user.genero

        return token

    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2", "full_name", "cpf", "celular", "nacionalidade", "cep", "numero", "complemento", "cidade", "estado", "rua", "bairro", "isfuncionario", "genero"]
    

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            cpf=validated_data["cpf"],
            celular=validated_data["celular"],
            nacionalidade=validated_data["nacionalidade"],
            cep=validated_data["cep"],
            numero=validated_data["numero"],
            complemento=validated_data["complemento"],
            cidade=validated_data["cidade"],
            estado=validated_data["estado"],
            rua=validated_data["rua"],
            bairro=validated_data["bairro"],
            isfuncionario=validated_data["isfuncionario"],
            genero=validated_data["genero"]
        )
        user.set_password(validated_data["password"])
        user.save()

        return user
    
def validate_password(self, attrs):
    if attrs["password"] != attrs["password2"]:
        raise serializers.ValidationError({"password": "Senhas não são iguais."})
    return attrs