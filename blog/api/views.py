import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Blog, Post, User
from .serializers import (BlogCreateSerializer, BlogReadSerializer,
                          CommentSerializer, PostSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def update_blog_update_at(self, ids, update_at):
        for id in ids:
            blog = Blog.objects.filter(id=id)
            blog.update(updated_at=update_at)

    def perform_create(self, serializer):
        is_published = self.request.data.get('is_published')
        if is_published:
            created_at = datetime.datetime.now()
            tags = self.request.data.get('tags')
            self.update_blog_update_at(tags, created_at)
        else:
            created_at = "1000-01-01T00:00:00Z"
        serializer.save(author=self.request.user, created_at=created_at)

    def perform_update(self, serializer):
        is_published = self.request.data.get('is_published')
        if is_published:
            serializer.instance.created_at = datetime.datetime.now()
            tags = self.request.data.get('tags')
            self.update_blog_update_at(tags, serializer.instance.created_at)
        else:
            serializer.instance.created_at = "1000-01-01T00:00:00Z"
        serializer.save()


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
