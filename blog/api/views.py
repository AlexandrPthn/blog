import datetime

from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .filters import BlogFilter, PostFilter
from .models import Blog, Follow, Post, User
from .pagination import LimitPagePagination
from .serializers import (BlogCreateSerializer, BlogReadSerializer,
                          CommentSerializer, FollowSerializer, PostSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitPagePagination

    @action(detail=False)
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitPagePagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = PostFilter
    search_fields = ('title', 'author__username')
    ordering_fields = ('title', 'created_at', 'likes')

    def retrieve(self, request, pk=None):
        if pk is not None:
            Post.objects.filter(id=pk).update(views=F("views") + 1)
        post = self.get_object()
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_blog_update_at(self, ids, update_at):
        for id in ids:
            Blog.objects.filter(id=id).update(updated_at=update_at)

    def check_autors_blog(self, blog, user):
        if (Blog.objects.filter(id=blog, authors=user).exists() or
                Blog.objects.filter(id=blog, owner=user).exists()):
            return True
        return False

    def perform_create(self, serializer):
        tags = self.request.data.get('tags')
        author_post = self.request.user
        for tag in tags:
            if not self.check_autors_blog(tag, author_post):
                raise APIException("Errors: 'Проверьте допуск к блокам!")
        is_published = self.request.data.get('is_published')
        if is_published:
            created_at = datetime.datetime.now()
            self.update_blog_update_at(tags, created_at)
        else:
            created_at = None
        serializer.save(author=author_post, created_at=created_at)

    def perform_update(self, serializer):
        tags = self.request.data.get('tags')
        author_post = serializer.instance.author
        if author_post != self.request.user:
            raise APIException("Errors: 'Вы не являетесь автором поста!")
        for tag in tags:
            if not self.check_autors_blog(tag, author_post):
                raise APIException("Errors: 'Проверьте допуск к блокам!")
        is_published = self.request.data.get('is_published')
        if is_published:
            serializer.instance.created_at = datetime.datetime.now()
            self.update_blog_update_at(tags, serializer.instance.created_at)
        else:
            serializer.instance.created_at = None
        serializer.save()

    @action(detail=True,
            methods=['POST', 'DELETE'])
    def likes(self, request, **kwargs):
        if request.method == 'POST':
            id = kwargs.get('pk')
            Post.objects.filter(id=id).update(likes=F("likes") + 1)
            post = self.get_object()
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            id = kwargs.get('pk')
            Post.objects.filter(id=id).update(likes=F("likes") - 1)
            post = self.get_object()
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Разрешены только POST и DELETE запросы',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateSerializer
    additional_serializer = FollowSerializer
    pagination_class = LimitPagePagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = BlogFilter
    search_fields = ('title', 'owner__username')
    ordering_fields = ('title', 'updated_at', 'likes')

    @action(methods=['POST', 'DELETE'], detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        blog = get_object_or_404(Blog, id=kwargs.get('pk'))
        if request.method == 'POST':
            if Follow.objects.filter(user=user, blog=blog).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данный блог'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscribe = Follow.objects.create(user=user, blog=blog)
            serializer = self.additional_serializer(
                subscribe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follow = Follow.objects.filter(user=user, blog=blog)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'У вас нет подписки на данный блог'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
