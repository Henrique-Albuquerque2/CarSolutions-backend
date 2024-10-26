from django.shortcuts import render

# Create your views here.
from carSolutions.models import User, Profile
from carSolutions.serializers import UserSerializer, RegisterSerializer, MyTokenObtainPairSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

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
    