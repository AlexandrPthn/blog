from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import AuthorsPost, Blog, Post, Tag, User


class CreateUserSerializers(serializers.ModelSerializer):
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
        return super(CreateUserSerializers, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class PostCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Post
        fields = ('id',
                  'author',
                  'title',
                  'body',
                  'created_at',
                  'likes',
                  'views',
                  'tags',
                  )

    def validate_tags(self, data):
        tags = data
        if not tags:
            raise serializers.ValidationError(
                'В рецепте должен быть хотя бы один тег'
            )
        validated_tags = []
        for tag in tags:
            if tag in validated_tags:
                raise serializers.ValidationError({
                    'tags': 'Теги должны быть уникальными!'
                })
            validated_tags.append(tag)
        return data
    
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.save()
        return instance


class PostReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id',
                  'author',
                  'title',
                  'body',
                  'created_at',
                  'likes',
                  'views',
                  'tags',
                  )


class AuthorsPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = AuthorsPost
        fields = ('id',)


class BlogCreateSerializer(serializers.ModelSerializer):
    authors = AuthorsPostSerializer(many=True)
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

    def authors_create(self, authors, blog):
        authors_list = [
            AuthorsPost(
                user=User.objects.get(id=author['id']),
                blog=blog
            ) for author in authors
        ]
        AuthorsPost.objects.bulk_create(authors_list)

    def create(self, validated_data):
        authors = validated_data.pop('authors')
        blog = Blog.objects.create(owner=self.context['request'].user,
                                   **validated_data)
        self.authors_create(
            authors=authors,
            blog=blog
        )
        return blog

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors')
        instance = super().update(instance, validated_data)
        instance.authors.clear()
        self.authors_create(authors, instance)
        instance.save()
        return instance


class BlogReadSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
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

    def get_authors(self, obj):
        blog = obj
        return blog.authors.values(
            'id',
            'email',
            'username',
        )
