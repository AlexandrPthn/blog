from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    ROLE_CHOICES = [(USER, 'Пользователь'),
                    (ADMIN, 'Администратор')]

    username = models.CharField(
        verbose_name='Логин пользователя',
        max_length=150,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    role = models.CharField(
        verbose_name='Статус',
        choices=ROLE_CHOICES,
        default=USER,
        max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username']

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == User.ADMIN

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Blog(models.Model):
    title = models.CharField(
        verbose_name='Заголовок блога',
        max_length=100
        )
    description = models.TextField(
        verbose_name='Описание блога'
        )
    created_at = models.DateTimeField(
        verbose_name='Дата создания публикации',
        auto_now_add=True
        )
    updated_at = models.DateTimeField(
        verbose_name='Дата обновления публикации',
        auto_now_add=True
        )
    authors = models.ManyToManyField(
        User,
        verbose_name='Автор публикации',
        through='AuthorsPost',
        related_name="authorsposts"
        )
    owner = models.ForeignKey(
        User,
        verbose_name="Автор блога",
        on_delete=models.CASCADE,
        )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return self.title


class AuthorsPost(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        )
    blog = models.ForeignKey(
        Blog,
        verbose_name='Наименование блога',
        on_delete=models.CASCADE
        )

    class Meta:
        verbose_name = 'Автор публикации в блоге'
        verbose_name_plural = 'Автор публикации в блоге'

    def __str__(self):
        return f'Автор публикации: {self.user} (Блог: {self.blog})'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
        unique=True
        )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=50,
        unique=True
        )
    slug = models.SlugField(
        verbose_name='Слуг',
        max_length=50,
        unique=True
        )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэг'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор поста"
        )
    title = models.CharField(
        verbose_name='Заголовок поста',
        max_length=100
        )
    body = models.TextField(
        verbose_name="Текст поста"
        )
    created_at = models.DateTimeField(
        verbose_name="Дата публикации"
        )
    likes = models.PositiveIntegerField(
        verbose_name="Счётчик оценок",
        default=0
        )
    views = models.PositiveIntegerField(
        verbose_name="Счётчик просмотров",
        default=0
        )
    tags = models.ManyToManyField(
        Tag,
        related_name='posts',
        verbose_name='Тэги постов'
        )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост"
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария"
        )
    body = models.TextField(
        verbose_name="Текст комментария"
        )
    created_at = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True
        )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.body


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='Подписчик'
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="blog",
        verbose_name='Блог'
    )

    class Meta:
        verbose_name = 'Подписки на блог'
        verbose_name_plural = 'Подписки на блоги'
        constraints = [
            UniqueConstraint(fields=['user', 'blog'],
                             name='unique_follow')
        ]
