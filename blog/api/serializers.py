from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Blog, Comment, Follow, Post, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'Пароль', 'placeholder': 'Пароль'}
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Blog.objects.all(),
        many=True
    )
    created_at = serializers.DateTimeField(default=None)

    class Meta:
        model = Post
        fields = ('id',
                  'author',
                  'title',
                  'body',
                  'is_published',
                  'created_at',
                  'likes',
                  'views',
                  'tags',
                  )

    def validate_tags(self, data):
        tags = data
        if not tags:
            raise serializers.ValidationError(
                {'errors': 'В посте должен быть хотя бы один тэг'}
                )
        validated_tags = []
        for tag in tags:
            if tag in validated_tags:
                raise serializers.ValidationError(
                    {'errors': 'Теги должны быть уникальными!'}
                    )
            validated_tags.append(tag)
        return data


class BlogCreateSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ('id',
                  'title',
                  'description',
                  'created_at',
                  'updated_at',
                  'authors',
                  'owner',
                  )

    def validate_authors(self, data):
        authors = data
        if not authors:
            raise serializers.ValidationError(
                {'errors': 'Добавьте хотя бы одного автора в блог'}
                )
        validated_authors = []
        for author in authors:
            if author in validated_authors:
                raise serializers.ValidationError(
                    {'errors': 'Авторы должны быть уникальными.'}
                    )
            validated_authors.append(author)
        return data

    def create(self, validated_data):
        authors = validated_data.pop('authors')
        blog = Blog.objects.create(owner=self.context['request'].user,
                                   **validated_data)
        blog.authors.set(authors)
        return blog


class BlogReadSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Blog
        fields = ('id',
                  'title',
                  'description',
                  'created_at',
                  'updated_at',
                  'authors',
                  'owner',
                  )

    def get_authors(self, obj):
        blog = obj
        return blog.authors.values(
            'id',
            'email',
            'username',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )

    class Meta:
        model = Comment
        fields = ('id',
                  'post',
                  'author',
                  'body',
                  'created_at',
                  )
        read_only_fields = ('post',)


class FollowSerializer(UserSerializer):
    id = serializers.ReadOnlyField(source='blog.id')
    title = serializers.ReadOnlyField(source='blog.title')

    class Meta:
        model = Follow
        fields = ('id', 'title',)
