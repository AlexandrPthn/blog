from django.urls import include, path
from rest_framework import routers

from .views import BlogViewSet, PostViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('blogs', BlogViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
