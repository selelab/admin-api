import logging
import uuid

import django_filters
from django.shortcuts import render
from rest_framework import decorators, filters, permissions, response, viewsets

from accounting.models import Project
from web import settings

from .models import User
from .serializer import UserCreationSerializer, UserDetailSerializer, UserSerializer, UserUpdateSerializer


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class ReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.method in permissions.SAFE_METHODS


class OwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'pk' not in view.kwargs:
            return False

        if not request.user:
            return False

        if request.method in {'DELETE'}:
            return False

        # データベース参照は最後の手段
        owner = User.objects.get(pk=view.kwargs['pk'])
        if request.user != owner:
            return False

        return True


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed_perm_classes = [
            AdminPermission, ReadOnlyPermission, OwnerPermission
        ]
        return any(perm_class().has_permission(request, view)
                   for perm_class in allowed_perm_classes)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = settings.DEFAULT_HTTP_METHOD_NAMES
    permission_classes = (UserPermission, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserCreationSerializer
        elif self.action == 'partial_update':
            return UserUpdateSerializer
        return self.serializer_class
