from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls")),
    path("accounts/", include("accounts.urls")),
    path("", RedirectView.as_view(pattern_name="chat:index"), name="root"),
]
