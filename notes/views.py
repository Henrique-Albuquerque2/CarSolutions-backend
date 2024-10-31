from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lembrete
from .serializers import LembreteSerializer

class LembreteViewSet(viewsets.ModelViewSet):
    queryset = Lembrete.objects.all()
    serializer_class = LembreteSerializer

    def perform_create(self, serializer):
        nome_completo = f"{self.request.user.full_name}"
        serializer.save(criador=nome_completo)

    @action(detail=True, methods=['patch'], url_path='ok')
    def mark_as_ok(self, request, pk=None):
        lembrete = self.get_object()
        lembrete.status_ok = True
        lembrete.save()
        return Response({'status': 'lembrete marcado como OK'})
