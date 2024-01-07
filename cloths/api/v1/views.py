from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from accounts.models import Profile
from cloths.models import Cloth, Comment
from .serializers import ClothSerializer, CommentSerializer
from .paginations import DefaultPagination
from .permissions import IsOwnerOrReadOnlyForProfile, IsOwnerOrReadOnlyForUser


class ClothModelViewSet(viewsets.ModelViewSet):
    serializer_class = ClothSerializer
    queryset = Cloth.objects.filter(active=True)
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyForProfile]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "author": ["exact", "in"],
    }
    search_fields = ["title", "description"]
    ordering_fields = ["datetime_created"]


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        cloth_id = self.kwargs.get("cloth_id")
        cloth = get_object_or_404(Cloth, id=cloth_id)
        return Comment.objects.filter(cloth=cloth)

    def perform_create(self, serializer):
        cloth_id = self.kwargs.get("cloth_id")
        cloth = get_object_or_404(Cloth, id=cloth_id)
        if Comment.objects.filter(cloth=cloth, author=self.request.user).exists():
            raise serializers.ValidationError(
                {"Message": "You have already added comment on this blog"}
            )
        serializer.save(author=self.request.user, cloth=cloth)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnlyForUser]

    def get_object(self):
        comment_id = self.kwargs.get("comment_id")
        comment = get_object_or_404(Comment, id=comment_id)

        cloth_id = self.kwargs.get("cloth_id")
        if comment.cloth.id != cloth_id:
            raise serializers.ValidationError(
                {"Message": "This comment is not related to the requested blog"}
            )
        return comment

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author.id != request.user.id:
            return Response(
                {"Message": "You are not authorized to perform this action"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author.id != request.user.id:
            return Response(
                {"Message": "You are not authorized to perform this action"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().put(request, *args, **kwargs)
