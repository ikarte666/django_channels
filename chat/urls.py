from django.urls import path
from chat import views

app_name = "chat"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.room_new, name="room_new"),
    path("<int:room_pk>/", views.room_chat, name="room_chat"),
]