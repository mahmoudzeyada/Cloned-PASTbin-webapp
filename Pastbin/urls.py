from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter

from api.views import DocumentViewSet
from shortner.views import UrlRedirectView

router = DefaultRouter()
router.register("documents", DocumentViewSet, base_name="documents")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'(?P<short_code>[\w-]+)/$', UrlRedirectView.as_view()),
]
