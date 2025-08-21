from django.urls import path
from employee.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/<uuid:department_id>/", ChatConsumer.as_asgi()),
]
