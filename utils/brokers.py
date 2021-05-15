
from utils.event.engine import EventEngine
from getaway.binance_http import BinanceFutureHttp
from getaway.binance_ws import BinanceDataWebsocket

class Broker(object):

    def __init__(self, engine: EventEngine, key=None, secret=None, symbol=None):
        self.event_engine = engine
        self.binance_http = BinanceFutureHttp(key=key, secret=secret)
        self.binance_data_ws = BinanceDataWebsocket(broker=self)
        self.binance_data_ws.subscribe(symbol)
        self.event_engine.start()
        self.strategies_dict = {}

    def add_strategy(self, strategy_class, symbol, min_volume):
        self.strategies_dict[strategy_class.__name__] = strategy_class(self, symbol, min_volume)

