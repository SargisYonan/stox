import json
import requests
import pandas as pd
import datetime

import threading
import time
from math_tools import get_buffer_derivative

class CurrencyScraper:
	def __init__(self, symbol, exchange_currency='usd', exchange='gdax'):
		self.exchange_currency = exchange_currency
		self.symbol = symbol
		self.exchange = exchange

		self.price_pair = symbol.lower() + exchange_currency.lower()
		self.url = 'https://api.cryptowat.ch/markets/' + self.exchange.lower() + '/' + self.price_pair + '/price'
	
	def get_current_price(self):
		page = requests.get(self.url)
		data = page.json()
		return float(data['result']['price'])

	def hourly_price_historical(self, limit, aggregate):
		url = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&limit={}&aggregate={}'.format(self.symbol.upper(), self.exchange_currency.upper(), limit, aggregate)
		if self.exchange:
			url += '&e={}'.format(self.exchange)
		page = requests.get(url)
		data = page.json()['Data']
		df = pd.DataFrame(data)
		df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
		return df

class RingBuffer:
	def __init__(self, size):
		self.data = [None for i in xrange(size)]

	def append(self, x):
		self.data.pop(0)
		self.data.append(x)

	def get(self):
		return self.data

class PriceWatcher(threading.Thread, CurrencyScraper, RingBuffer):
	def __init__(self, currency, exchange_currency, exchange='GDAX', delta_t=10, savepoints=1000, live_print=False):
		self.currency = currency
		self.exchange = exchange
		self.exchange_currency = exchange_currency
		self.savepoints = savepoints
		self.delta_t = delta_t
		self.live_print = live_print

		self.buffer = RingBuffer(savepoints) # store the last points in the ring buffer
		self.diff_buffer = RingBuffer(savepoints) # stores computed derivatives

		self.price_watch_thread = threading.Thread(target=self.store_prices)

		self.scraper = CurrencyScraper(currency, exchange_currency, exchange)
		# setting self's get price func ptr to the currency
		# classes price getter
		self.get_current_price = self.scraper.get_current_price
		self.current_price = self.get_current_price()
		self.deriv = None

		threading.Thread.__init__(self)

	def get_price(self):
		return self.current_price

	# meant to be run in a separte thread
	def store_prices(self):
		while(True):
			time.sleep(self.delta_t)
			self.current_price = self.get_current_price()
			self.buffer.append(self.current_price)

			self.get_derivative()

	def print_pair(self):
		print 'Current Price: ' + str(self.get_price()) + ' ' + self.exchange_currency + ' - Derivative: ' + str(self.deriv)

	def get_derivative(self):
		self.deriv = get_buffer_derivative(self.buffer.get())
		self.diff_buffer.append(self.deriv)

		if self.live_print:
			self.print_pair()

	def start_price_watcher(self):
		self.price_watch_thread.start()

