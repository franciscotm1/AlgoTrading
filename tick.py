from backtesting import evaluateTick
from strategy import Strategy
from order import Order
from event import Event
import os
import random
import numpy as np


# Francisco e Gabriel
class MACDRSI(Strategy):

    OVERBOUGHT = 65
    OVERSOLD = 30
    SIZE = 14
    # SIZE = 5

    def __init__(self):
        self.prices = []
        self.signal = 0
        self.sizeq = 12
        self.sizes = 26
        self.sizemamacd = 9
        # self.sizemamacd = 5
        self.state = 1
        self.lmacd = []

    def _get_rs(self):
        slice_prices = self.prices
        if len(self.prices) > self.SIZE:
            slice_prices = self.prices[-self.SIZE:]
        highs = []
        lows = []
        for i in range(1, len(slice_prices)):
            ret = slice_prices[i]
            if slice_prices[i] > slice_prices[i - 1]:
                highs.append(ret)
            else:
                lows.append(ret)
        avg_high = sum(highs) / len(slice_prices) if len(slice_prices) else 0
        avg_low = sum(lows) / len(slice_prices) if len(slice_prices) else 1
        return avg_high / avg_low if avg_low else 0

    def _calculate_rsi(self):
        rs = self._get_rs()
        rsi = 100 - 100 / (1 + rs)
        return rsi


    def push(self, event):
        orders = []
        if event.type == Event.TRADE:
            price = event.price
            self.prices.append(price)
            rsi = self._calculate_rsi()

            if len(self.prices) >= self.sizeq:
                maq = sum(self.prices[-self.sizeq:])/self.sizeq

            if len(self.prices) == self.sizes:
                mas = sum(self.prices)/self.sizes
                macd = maq - mas
                self.lmacd.append(macd)
                

                if len(self.lmacd) >= self.sizemamacd:
                    mamacd = sum(self.lmacd[-self.sizemamacd:])/self.sizemamacd
                    if macd > mamacd and rsi < self.OVERSOLD:
                        if self.state == 0:
                            if self.signal == -1:
                                orders.append(Order(event.instrument, 100, 0))
                                orders.append(Order(event.instrument, 100, 0))
                            if self.signal == 0:
                                orders.append(Order(event.instrument, 100, 0))
                            self.signal = 1
                            self.state = 1
                    elif macd < mamacd or rsi > self.OVERBOUGHT:
                        if self.state == 1:
                            if self.signal == 1:
                                orders.append(Order(event.instrument, -100, 0))
                                orders.append(Order(event.instrument, -100, 0))
                            if self.signal == 0:
                                orders.append(Order(event.instrument, -100, 0))
                            self.signal = -1
                            self.state = 0
                del self.prices[0]
        return orders

# Francisco e Gabriel
class MACD(Strategy):
    def __init__(self):
        self.prices = []
        self.signal = 0
        self.sizeq = 12
        self.sizes = 26
        self.sizemamacd = 9
        self.state = 1
        self.lmacd = []

    def push(self, event):
        orders = []
        if event.type == Event.TRADE:
            price = event.price
            self.prices.append(price)

            if len(self.prices) >= self.sizeq:
                maq = sum(self.prices[-self.sizeq:])/self.sizeq

            if len(self.prices) == self.sizes:
                mas = sum(self.prices)/self.sizes
                macd = maq - mas
                self.lmacd.append(macd)
                

                if len(self.lmacd) >= self.sizemamacd:
                    mamacd = sum(self.lmacd[-self.sizemamacd:])/self.sizemamacd
                    if macd > mamacd:
                        if self.state == 0:
                            if self.signal == -1:
                                orders.append(Order(event.instrument, 100, 0))
                                orders.append(Order(event.instrument, 100, 0))
                            if self.signal == 0:
                                orders.append(Order(event.instrument, 100, 0))
                            self.signal = 1
                            self.state = 1
                    elif macd < mamacd:
                        if self.state == 1:
                            if self.signal == 1:
                                orders.append(Order(event.instrument, -100, 0))
                                orders.append(Order(event.instrument, -100, 0))
                            if self.signal == 0:
                                orders.append(Order(event.instrument, -100, 0))
                            self.signal = -1
                            self.state = 0
                del self.prices[0]
        return orders

files = os.listdir('./PETR4-2018-08')
for file in files:
    print(evaluateTick(MACDRSI(), {'PETR4': f'./PETR4-2018-08/{file}'}))
    print(evaluateTick(MACD(), {'PETR4': f'./PETR4-2018-08/{file}'}))
