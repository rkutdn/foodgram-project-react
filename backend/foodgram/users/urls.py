from rest_framework import routers
from django.urls import include, path

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
