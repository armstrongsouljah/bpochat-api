from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chat.consumers import (
    ChatMessageConsumer,
)
from chatterbox.consumers import ChatterboxConsumer


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
         path('<username>/chat', ChatMessageConsumer),
         path('messages/<username>/send', ChatterboxConsumer)
        ])
    )
})