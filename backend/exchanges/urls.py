from django.urls import path
from .exchanges.binance.binance import BinanceConsumer

websocket_urlpatterns = [
    path('ws/binance/', BinanceConsumer.as_asgi()),
]
