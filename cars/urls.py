from django.urls import path
from . import views

urlpatterns = [
    # Gerenciamento de carros e reservas
    path("cars/", views.CarViewSet.as_view({'get': 'list', 'post': 'create'}), name="car-list-create"),
    path("cars/<int:pk>/", views.CarViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="car-detail"),
    
    path("reservations/", views.CarReservationViewSet.as_view({'get': 'list', 'post': 'create'}), name="reservation-list-create"),
    path("reservations/<int:pk>/", views.CarReservationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="reservation-detail"),
]
