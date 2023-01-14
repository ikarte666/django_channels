from django.urls import path
from chat import consumers

websocket_urlpatterns = [
    path("ws/chat/<int:room_pk>/", consumers.ChatConsumer.as_asgi()),
]
