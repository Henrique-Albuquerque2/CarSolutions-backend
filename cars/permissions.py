# cars/permissions.py

from rest_framework import permissions

class IsFuncionario(permissions.BasePermission):
    """
    Permissão personalizada que permite acesso apenas a usuários com `isfuncionario = True`.
    """

    def has_permission(self, request, view):
        # Permitir acesso se o usuário está autenticado e tem `isfuncionario` marcado como True
        return bool(request.user and request.user.is_authenticated and request.user.isfuncionario)
