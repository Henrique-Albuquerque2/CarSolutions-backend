from django.shortcuts import render

# Create your views here.
from carSolutions.models import User, Profile
from carSolutions.serializers import RegisterSerializer, MyTokenObtainPairSerializer, LogoutSerializer
from carSolutions.serializers import UserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Obtem o usuário autenticado a partir dos dados validados
        user = serializer.user

        # Gera o token e obtém a resposta padrão com os tokens
        response = super().post(request, *args, **kwargs)

        # Adiciona informações adicionais ao corpo da resposta JSON
        response.data.update({
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "cpf": user.cpf,
            "celular": user.celular,
            "nacionalidade": user.nacionalidade,
            "cep":user.cep,
            "numero":user.numero,
            "complemento": user.complemento,
            "cidade": user.cidade,
            "estado": user.estado,
            "rua": user.rua,
            "bairro": user.bairro,
            "isfuncionario": user.isfuncionario,
            "genero": user.genero
        })
        return response
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


@api_view(["GET", 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == "GET":
        response = f'Hello, {request.user.username}!, GET'
        return Response({'response': response}, status=status.HTTP_200_OK)
    if request.method == "POST":   
        text = request.POST.get('text')
        response = f'Hello, {request.user.username}! POST, You said: {text}'
        return Response({'response': response}, status=status.HTTP_200_OK)
    
    return Response({'response': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Logout realizado com sucesso!"}, status=status.HTTP_205_RESET_CONTENT)
    
class PasswordResetRequestView(generics.CreateAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]  # Permite acesso sem autenticação
    queryset = User.objects.all()  # Define queryset para evitar erro

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Função para obter os dados do usuário autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meusdados(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)