from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chatterbox.consumers import ChatterboxConsumer


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
         path('messages/<username>/send', ChatterboxConsumer)
        ])
    )
})