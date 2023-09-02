"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import tomllib

from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

with open(f"pyproject.toml", "rb") as f:
    DRF_PROJECT_CONTENT = tomllib.load(f)["tool"]["poetry"]

schema_view = get_schema_view(
    openapi.Info(
        title=DRF_PROJECT_CONTENT["name"],
        default_version=DRF_PROJECT_CONTENT["version"],
        description=DRF_PROJECT_CONTENT["description"],
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="moroz070688@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # docs urls
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # add local app urls
    path("api/v1/store/", include("src.store.urls")),
]
