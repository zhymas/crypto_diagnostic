from abc import ABC, abstractmethod

class Exchange(ABC):

    @abstractmethod
    def connect_to_exchange(self):
        pass
    
    @abstractmethod
    def get_coin_price(self, coin: str):
        pass

class ExchangeConnector(Exchange):
    def __init__(self, exchange_name: str):
        self.exchange_name = exchange_name
    