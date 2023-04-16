from drf_yasg import openapi
from rest_framework import permissions

from django.conf.urls import url
from django.urls import path, include
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="Blog API",
        license=openapi.License(name="BSD License"),
    ),
    patterns=[path('api/', include('api.urls')), ],
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
