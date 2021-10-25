from django.urls import re_path

from sockets import consumers

websocket_urlpatterns = [
    re_path(r'channel/$', consumers.Chanel.as_asgi()),
]