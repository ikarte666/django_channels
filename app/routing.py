from django.urls import path
from app.consumers import EchoConsumer, LiveblogConsumer

# urls.py와 비슷한 역할
# 매칭되는 주소로 요청이 오면 해당 consumer를 호출하는듯
# as_asgi는 비동기화 시켜주는 역할인듯 보임, as_view 사용하는 느낌
websocket_urlpatterns = [
    path("ws/echo/", EchoConsumer.as_asgi()),
    path("ws/liveblog/", LiveblogConsumer.as_asgi()),
]
