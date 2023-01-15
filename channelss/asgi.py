import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channelss.settings")

django_asgi_app = get_asgi_application()

# http 요청은 view에서 처리, 웹소켓 요청은 URLRouter에서 처리
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # AuthMiddlewareStack 적용 시 scope로 user, cookie, session에 접근 가능
        "websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
    }
)
