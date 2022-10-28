"""
ASGI config for Messenger project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import Messenger.room.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Messenger.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            Messenger.room.routing.websocket_urlpatterns
        )
    )
})
