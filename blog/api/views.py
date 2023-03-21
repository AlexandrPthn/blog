from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Blog, Post, User
from .serializers import (BlogCreateSerializer, BlogReadSerializer,
                          CommentSerializer, PostCreateSerializer,
                          PostReadSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return PostCreateSerializer
        return PostReadSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateSerializer

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return BlogCreateSerializer
        return BlogReadSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
