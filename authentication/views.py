from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import RegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
