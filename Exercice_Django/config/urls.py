from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/<version>/", include("medical.urls")),  # versioned
    path("", include("medical.urls")),  # legacy — to be deprecated
]
