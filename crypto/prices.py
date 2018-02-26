'''
Crypto-Currency Market Analyzer
Written by Sargis S Yonan
December 2017

Using various mathematical decompositons (QR, SVD)
as well as some calculus let's try to make some money by
finding trends and slopes in a given crypto-ticker
'''

######################################################################
############################# PARAMETERS #############################
######################################################################

plot_results = True # true for drawing figures to image and window
draw_plot = True # just for drawing window 
## -- both plot_results and draw_plot must be true for drawing to window

use_account = False
key_dir = 'access/'

currency = 'ETH'
exchange_cur = 'USD' # currency to show results in
exchange = 'GDAX'

day_history = 4 # number of days to consider
significance = 3 # number of sigmas to consider

# if the currency only fluctuates within +/- of
# this threshold, we will call it stable in the
# sub-domains where this is true in our volatility
# calculations
stability_criterion = 10 # units in \exchange_cur previously defined

######################################################################

# my coinbase account API
# lets me buy/sell from the script
# and look at coinbase exchange prices
import account 

# the apis I use reference prices in unix time
# so we're going to need to convert those
import datetime 

if plot_results:
	# for plotting results and legends on those results
	import matplotlib.pyplot as plt
	import matplotlib.patches as mpatches

# sucks but i had to make a custom scraper for each currency
# because the free APIs are delayed and don't allow higher
# frequency data grabbing
import currency_scraper as scrape
scraper = scrape.CurrencyScraper(currency, exchange_cur, exchange)

watcher = scrape.PriceWatcher(currency, exchange_cur, exchange, live_print=True) # separate thread -- needs to be started 
watcher.start_price_watcher() # runs in a separate thread to collect instantaneous derivative

# for math
from math_tools import disc_diff # my custom made differentiator
import numpy as np
from numpy.linalg import svd

if use_account:
	coinbase = account.CoinbaseAccount(key_dir)

# print the current price of the currency for account
print '\nCurreny: ' + currency
current_price = scraper.get_current_price()
print '\nCurrent Price: ' + str(current_price) + ' ' + exchange_cur

# printing the last couple of hours of the currency's opening prices
last_couple_of_hours = 6 # six hours
print '\nLast ' + str(last_couple_of_hours) + ' Hours:\n'
last_hours_prices = scraper.hourly_price_historical(last_couple_of_hours, 1)

prices = last_hours_prices['open']
times = last_hours_prices['time']
for i in range(0, len(prices)):
	time_stamp = datetime.datetime.fromtimestamp(int(times[i])).strftime('%H:%M')
	print time_stamp + ': ' + str(prices[i]) + ' ' + exchange_cur

time_delta = 1 # time step -- we're going to use hours for now
data_limit = 24 * day_history # number of hours to look back into
hr_df = scraper.hourly_price_historical(data_limit, time_delta)

opening_prices = list(hr_df['open'])

# collect all time stamps and convert them from epoch time
# to something I can actually read and understand
unix_times = hr_df['time']
time_hours = []
time_days = []
for unix_time in unix_times:
	time_days.append(datetime.datetime.fromtimestamp(int(unix_time)).strftime('%d'))
	time_hours.append(datetime.datetime.fromtimestamp(int(unix_time)).strftime('%H'))

######################################################################################
# I want to start my matrix rows off at a time of 0:00:00 (beginning of the day)
# to do this, I need to grab additional hours from the API and restore the times
# and prices
#
# To do this, I just calculate the residual hours from the initial pull, and request the
# excess remaining and restore everything
# 
# Do it this way, because we don't want to repeat the same number (day of the month)
# if you just search for occurences of this day, the data will be wrong if several
# months of data are pulled

initial_day = time_days[0]
initial_day_counter = 0
for day in time_days:
	if day == initial_day:
		initial_day_counter += 1

threshold_to_collect_more_hours = 20
if initial_day_counter > threshold_to_collect_more_hours:
	additional_hours = 24 - initial_day_counter
	hr_df = scraper.hourly_price_historical(data_limit + additional_hours, time_delta)
	opening_prices = list(hr_df['open'])
	# collect all time stamps and convert them from epoch time
	# to something I can actually read and understand
	unix_times = hr_df['time']
	time_hours = []
	time_days = []
	for unix_time in unix_times:
		time_days.append(datetime.datetime.fromtimestamp(int(unix_time)).strftime('%d'))
		time_hours.append(datetime.datetime.fromtimestamp(int(unix_time)).strftime('%H'))

######################################################################################

# I now need to find where the last day ends so I can get a consistant number of rows
last_day = time_days[-1]
last_day_counter = 1
for day in reversed(time_days):
	if day == last_day:
		last_day_counter += 1

# and then we'll remove the excess hours from the list if they don't add up to a full day
if last_day_counter < 24:
	for i in range(1, last_day_counter):
		del time_days[-1] # removes the last element from the list
		del time_hours[-1]
		del opening_prices[-1]

######################################################################################
# we can now construct our price/day matrix
total_days = len(time_days) / 24
price_mat = np.zeros([total_days, 24], dtype=np.float64)
	
if plot_results:
	plt.close()


	plt.ion()
	plt.show()

	plt.figure('Price Table Figure', figsize=(16, 12), facecolor='w', edgecolor='k')

	plt.subplot(411)

	plt.title('Hourly Opening ' + currency + ' Price')
	plt.ylabel('Price (' + exchange_cur + ')')

if plot_results:
	i = 0
for row in range(0, total_days):
	for col in range(0, 24):
		price_mat[row, col] = opening_prices[i]

		if plot_results:
			i += 1

	if plot_results:
		plt.plot(range(0,24),price_mat[row, :], label=str(time_days[i-1]))
		if draw_plot:
			plt.draw()
			plt.pause(0.001)

if plot_results:
	plt.legend(bbox_to_anchor=(.9, 1), loc=2, borderaxespad=2.0)
	plt.grid(color='k', linestyle='-', linewidth=.2)

######################################################################################
# lets compute our SVD and plot it
U,S,V = svd(price_mat, compute_uv=True)

if plot_results:
	# bottom half of the subplot
	plt.subplot(412)
	plt.title('Price SVD')

total_svd = 0.0 

for i in range(0, significance - 1):
	# can't compute more significance than whats given
	if (i < len(S)):
		# only focusing on the V matrix because its our column space basis
		# which in our case represents hour significance
		total_svd += S[i]*V[:,i] 
		if plot_results:
			plt.plot(range(0,24), total_svd, label=(r'$\sigma$' + '=' + str(i + 1)))
			if draw_plot:
				plt.draw()
				plt.pause(0.001)

if plot_results:
	plt.legend(bbox_to_anchor=(.9, 1), loc=2, borderaxespad=2.0)
	plt.grid(color='k', linestyle='-', linewidth=.2)

######################################################################################
# lets compute some derivatives to get price slopes
price_deriv_mat = np.zeros([total_days, 24], dtype=np.float64)

if plot_results:
	plt.subplot(413)
	plt.title('Price Derivatives')
	plt.ylabel(r'$\Delta$' + ' Price')

if plot_results:
	i = 0
for r in range(0, price_mat.shape[0]):
	day_row = price_mat[r,:]
	for t in range(0, len(day_row)):
		derivative = disc_diff(day_row, t)
		if derivative is not None:
			price_deriv_mat[r, t] = derivative
		else:
			price_deriv_mat[r, t] = 0.0

		if plot_results:
			i += 1

	if plot_results:
		plt.plot(range(0,24), price_deriv_mat[r,:], label=str(time_days[i-1]))
		if draw_plot:
			plt.draw()
			plt.pause(0.001)

if plot_results:
	plt.legend(bbox_to_anchor=(.9, 1), loc=2, borderaxespad=2.0)
	plt.grid(color='k', linestyle='-', linewidth=.2)

######################################################################################

# lets analyze our discrete derivative matrix a bit more

# we can measure the volatility of the currency by checking
# the ratio at which its in our stability criterion
# this should correlate to some predictabilty measurment

stable_points = 0
for row in range(0, price_mat.shape[0]):
	day_row = price_mat[r,:]
	for col in range(0, len(day_row)):
		if abs(price_deriv_mat[row, col]) <= float(stability_criterion):
			stable_points += 1

if stable_points > 0:
	inv_volatility_ratio = float(stable_points) / float(total_days * 24)
else:
	inv_volatility_ratio = 0.0

volatility_ratio = 1.0 - inv_volatility_ratio
print('\nVolatility of ' + currency + ': ' + '{0:.2f}'.format(volatility_ratio * 100.0) + '%')

######################################################################################
# compute svd of the price gradient and plot it

dU,dS,dV = svd(price_deriv_mat, compute_uv=True)

if plot_results:
	# bottom half of the subplot
	plt.subplot(414)
	plt.title('Price Derivative SVD')

total_d_svd = 0.0 

for i in range(0, significance - 1):
	# can't compute more significance than whats given
	if (i < len(dS)):
		# only focusing on the V matrix because its our column space basis
		# which in our case represents hour significance
		total_d_svd += dS[i]*dV[:,i] 
		if plot_results:
			plt.plot(range(0,24), total_d_svd, label=(r'$d\sigma$' + '=' + str(i + 1)))
			if draw_plot:
				plt.draw()
				plt.pause(0.001)

if plot_results:
	plt.legend(bbox_to_anchor=(.9, 1), loc=2, borderaxespad=2.0)
	plt.grid(color='k', linestyle='-', linewidth=.2)

######################################################################################

if plot_results:
	# throw the hour label on the last subplot
	plt.xlabel('Hour')
	if draw_plot:
		plt.draw()
		plt.pause(0.001)
	plt.savefig('analysis.png')
######################################################################################

#factor both svds and derivatives for a given hour ... use inverted weighted sum to get nearby prices


