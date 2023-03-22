from django.urls import include, path
from rest_framework import routers

from .views import BlogViewSet, CommentViewSet, PostViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'blogs', BlogViewSet)
router.register('users', UserViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
