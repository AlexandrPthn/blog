from django.contrib import admin

from .models import Blog, Comment, Follow, Post, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'description',
                    'created_at',
                    'updated_at',
                    'owner'
                    )
    search_fields = ('owner',)
    list_filter = ('updated_at',)
    empty_value_display = '-пусто-'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author',
                    'title',
                    'body',
                    'created_at',
                    'likes',
                    'views'
                    )
    search_fields = ('author',)
    list_filter = ('created_at',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'body', 'created_at',)
    search_fields = ('author',)
    list_filter = ('created_at',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog')
    search_fields = ('user',)
