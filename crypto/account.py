from coinbase.wallet.client import Client
import json

class CoinbaseAccount():
	client = None
	accounts = None

	def __init__(self, key_directory, perms=None):
		api_key_file = key_directory + 'api_key'
		api_secret_file = key_directory + 'api_secret_key'
		try:
			try:
				api_key_fp = open(api_key_file, 'r')
				api_key = api_key_fp.readline()
				if (api_key == ''):
					raise ValueError ('Error: API Key File: ' + api_key_file + ' is empty.')
				api_key_fp.close()
			except:
				raise ValueError('Error opening the API Key File: ' + api_key_file)
			try:
				api_secret_fp = open(api_secret_file, 'r')
				api_secret = api_secret_fp.readline()
				if (api_secret == ''):
					raise ValueError ('Error: Secret Key File: ' + api_secret_file + ' is empty.')
				api_secret_fp.close()
			except:
				raise ValueError('Error opening the API Key File: ' + api_secret_file)
		except ValueError as err:
			print(err.args)
			quit() # end program on bad key reads

		self.client = Client(api_key, api_secret)
		self.accounts = self.client.get_accounts()

		try:
			assert (self.accounts.warnings is None) or isinstance(self.accounts.warnings, list)
		except AssertionError as err:
			print(err.args)
			quit()

	def get_current_price(self, symbol):
		table = self.client.get_exchange_rates()
		return 1.0 / table["rates"][symbol]

	def get_exchange_cur(self):
		table = self.client.get_exchange_rates()
		return table["rates"]

