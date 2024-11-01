from django.urls import path
from . import views

urlpatterns = [
    # Gerenciamento de carros e reservas
    path("cars/", views.CarViewSet.as_view(), name="car-list-create"),
    path("cars/<int:pk>/", views.CarViewSet.as_view(), name="car-detail"),
    path('cars/dados/<int:pk>/', views.CarDetailView.as_view(), name='car-id'),  # Endpoint para obter um carro específico
    path('available/', views.AvailableCarsView.as_view(), name='available_cars'),  # Nova URL para carros disponíveis
    path("available-by-date/", views.AvailableCarsByDateView.as_view(), name="available_cars_by_date"),

    path("reservations/", views.CarReservationViewSet.as_view({'get': 'list', 'post': 'create'}), name="reservation-list-create"),
    path("reservations/<int:pk>/", views.CarReservationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="reservation-detail"),
    path("reservations/<int:pk>/status/", views.CarReservationViewSet.as_view({'patch': 'update_status'}), name="reservation-update-status"),
    path("user/reservations/", views.UserReservationsView.as_view(), name="user-reservations"),
    path("all/reservations/", views.AllReservationsView.as_view(), name="all-reservations"),
]
