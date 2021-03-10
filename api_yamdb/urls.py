from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'),
         name='redoc'),

    # Логин и логаут для более удобной работы с browsable API
    path('api-auth/', include('rest_framework.urls')),

    # Эндпоинты
    path('api/', include('users_api_app.urls')),
    path('api/', include('title_api_app.urls')),
]

urlpatterns += staticfiles_urlpatterns()
