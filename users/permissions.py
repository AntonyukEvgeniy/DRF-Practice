from environs import env
from rest_framework import permissions


class ModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешаем GET запросы всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, является ли пользователь модератором
        if request.user.groups.filter(name="moderators").exists():
            # Разрешаем только PUT и PATCH запросы для модераторов
            return request.method in ["PUT", "PATCH"]

        return False


class IsOwnerOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Модераторы имеют полный доступ
        env.str("MODERATORS_GROUP")
        if request.user.groups.filter(name="moderators").exists():
            return True
        # Владельцы могут просматривать и редактировать свои курсы
        return obj.owner == request.user
