from rest_framework import generics, status
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Ad, Comment
from .serializers import (AdCreateSerializer, AdListSerializer,
                          CommentCreateSerializer)


class AdCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer


class AdDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdListSerializer

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def create(self, request, *args, **kwargs):

        comments_by_user = Comment.objects.filter(author=self.request.user).exists()

        if comments_by_user:
            return Response(
                {"detail": "you cannot post comments more than once"}, 
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
