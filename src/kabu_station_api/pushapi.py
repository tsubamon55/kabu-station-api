import asyncio
import json

import websockets
import pandas as pd


async def connect():
    tmp = {}
    async with websockets.connect('ws://localhost:18080/kabusapi/websocket') as ws:
        data = await ws.recv()
        info = Info(json.loads(data))
        if info.symbol in tmp:
            prev = tmp[info.symbol]
            info.order_volume = info.trading_volume - prev.trading_volume
            info.order_price = (info.trading_value - prev.trading_value) / info.order_volume
            if info.order_price != prev.asks.best_price and info.order_price != prev.bids.best_price:
                raise ValueError('invalid order price')
        tmp[info.symbol] = info
        yield info


class Info(object):
    def __init__(self, json_data):
        self.symbol = json_data.get('symbol')
        self.symbol_name = json_data.get('symbol_name')
        self.exchange = json_data.get('exchange')
        self.exchange_name = json_data.get('exchange_name')
        self.current_price = json_data.get('current_price')
        self.current_price_time = json_data.get('current_price_time')
        self.current_price_change_status = json_data.get('current_price_change_status')
        self.current_price_status = json_data.get('current_price_status')
        self.calc_price = json_data.get('calc_price')
        self.previous_close = json_data.get('previous_close')
        self.previous_close_time = json_data.get('previous_close_time')
        self.change_previous_close = json_data.get('change_previous_close')
        self.change_change_close_per = json_data.get('change_change_close_per')
        self.opening_price = json_data.get('opening_price')
        self.opening_price_time = json_data.get('opening_price_time')
        self.high_price = json_data.get('high_price')
        self.high_price_time = json_data.get('high_price_time')
        self.low_price = json_data.get('low_price')
        self.low_price_time = json_data.get('low_price_time')
        self.trading_volume = json_data.get('trading_volume')
        self.trading_volume_time = json_data.get('trading_volume_time')
        self.vwap = json_data.get('vwap')
        self.trading_value = json_data.get('trading_value')
        self.bid_time = json_data.get('bid_time')
        self.bid_sign = json_data.get('bid_sign')
        self.market_order_sell_qty = json_data.get('market_order_sell_qty')
        self.ask_time = json_data.get('ask_time')
        self.ask_sign = json_data.get('ask_sign')
        self.market_order_buy_qty = json_data.get('market_order_buy_qty')
        self.over_sell_qty = json_data.get('over_sell_qty')
        self.over_buy_qty = json_data.get('over_buy_qty')
        self.total_market_value = json_data.get('total_market_value')
        self.security_type = json_data.get('security_type')
        self.asks = OrderBook(*[json_data.get(f'Sell{i}') for i in range(10)])
        self.bids = OrderBook(*[json_data.get(f'Buy{i}') for i in range(10)])
        self.order_volume = 0
        self.order_value = 0


class OrderBook(object):
    def __init__(self, *quotes):
        self._quotes = pd.DataFrame(quotes)

    def __str__(self):
        return str(self._quotes)

    @property
    def json(self):
        return self._quotes.to_json()

    @property
    def best_price(self):
        return self._quotes.to_json()

    @property
    def best_size(self):
        return self._quotes.to_json()


if __name__ == '__main__':
    async def main():
        async for data in connect():
            print(data)
    asyncio.run(main())
