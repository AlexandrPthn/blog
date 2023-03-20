from rest_framework import viewsets

from .models import Blog, Post, Tag, User
from .serializers import (BlogCreateSerializer, BlogReadSerializer,
                          PostCreateSerializer, PostReadSerializer,
                          TagSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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
