from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Crypto Diagnostic API",
        default_version='v1',
        description="API for search differents in crypto exchange",
        terms_of_service="",
        contact=openapi.Contact(email="shvachko319@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-schema'),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/exchanges/', include('exchanges.urls')),
]
