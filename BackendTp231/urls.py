"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

# from account.views import SendMail

from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


schema_view = get_schema_view(
    openapi.Info(
        title="Episyche Technologies",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),


)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
        path("app/",include("app.urls")),
        # path('store/',include('store.urls')),
        # path('send-mail/',SendMail.as_view(),name='send_mail'),
        # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        # path('api-auth/', include('rest_framework.urls')),
        path('swagger/', get_swagger_view(title="Episyche Technologies"),name='schema-swagger'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)