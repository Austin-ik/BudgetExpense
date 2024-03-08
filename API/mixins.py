from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response


class UserOwnedQuerysetMixin:

    def dispatch(self, request, *args, **kwargs):
        self.queryset = self.get_queryset()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            # Return an empty queryset if user is not authenticated
            return self.model.objects.none()
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset



