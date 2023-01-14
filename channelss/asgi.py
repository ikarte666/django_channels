import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import app.routing
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channelss.settings")

django_asgi_app = get_asgi_application()

# http요청은 장고에서 처리, ws요청은 라우터를 통해 channels에서 처리
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(
            app.routing.websocket_urlpatterns + chat.routing.websocket_urlpatterns
        ),
    }
)
