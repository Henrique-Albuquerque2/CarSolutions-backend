from django.urls import path

from . import views

urlpatterns = [
    path('lembretes/', views.LembreteViewSet.as_view({'get': 'list', 'post': 'create'}), name='lembretes'), # GET e POST
    path('lembretes/<int:pk>/', views.LembreteViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='lembrete-detail'), # GET, PATCH e DELETE
    path('lembretes/<int:pk>/ok/', views.LembreteViewSet.as_view({'patch': 'mark_as_ok'}), name='lembrete-mark-as-ok'), # PATCH
]