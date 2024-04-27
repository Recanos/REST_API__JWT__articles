from rest_framework import permissions
from datetime import timedelta
from django.utils import timezone

# Любые пользователи могут читать любые статьи, но редактировать и удалять - только авторизированные,
# причём собственные статьи и только в течение одного дня после создания статьи
class IsAuthenticatedAndOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Позволить GET запросы для всех пользователей
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для всех других типов запросов требуем авторизацию
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Проверка на безопасные методы и на то, является ли пользователь владельцем объекта
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, является ли пользователь владельцем статьи
        is_owner = obj.user == request.user

        # Рассчитываем, прошло ли больше одного дня с момента создания статьи
        one_day_passed = timezone.now() - obj.created_at > timedelta(days=1)

        # Разрешить создание и изменение в течение первых суток после создания статьи только владельцем статьи
        can_edit = is_owner and not one_day_passed

        return can_edit