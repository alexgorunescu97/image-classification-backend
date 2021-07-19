from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from . import serializers

CustomUser = get_user_model()


class CustomUserModelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CustomUserSerializer
    queryset = CustomUser.objects.all()
    http_method_names = ['get', 'put', 'patch', 'post', 'head', 'options', 'trace', 'delete',]

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        elif self.action in ['create']:
            self.permission_classes = [permissions.AllowAny, ]
        return super().get_permissions()

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('password') == None:
            return super().update(request, *args, **kwargs)
        else:
            old_pass = request.data['old_pass']
            old_pass_database = instance.__dict__['password']
            if (check_password(old_pass, old_pass_database)):
                request._full_data = {'password': request.data['password']}
                return super().update(request, *args, **kwargs)
            else:
                raise ValueError(_('Wrong password'))

    def perform_update(self, serializer):
        if self.request.data.get('password') == None:
            serializer.save()
        else:
            instance = serializer.save()
            instance.set_password(instance.password)
            instance.save()

    
    