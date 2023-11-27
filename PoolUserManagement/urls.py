from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Управління користувачами басейну",
        default_version="1.0.0",
        description="За допомогою цього API адміністратори можуть керувати доступом людей до басейнів. "
                    "Кожен з відвідувачів може мати декілька унікальних підписок "
                    "(щоб мати можливість приходити декілька разів на день)"
                    "Коли відвідувач купляє підписку, вона видається йому назавжди.",
    ),
    public=True,
    url='http://127.0.0.1:8000/api/'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema')
]
