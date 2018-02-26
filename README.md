# stox
Various stock/crypto trading tools I've written and used in the past

# nyse
A pure C web-scraper for gathering data on a ticker. It is fast and very lightweight. Use your own API keys.

#crypto 
Scrapes any of the major exchanges (set to GDAX by default : prices.py:24) -- prices.py is the main driver
  - You can modify which coin to examine, the exchange currency, and the statistical parameters to consider in the same file
  - Running prices.py will gather historical data, run several analytical function on, and make decisions on the ticker.
    - currently a singular value decompostion and rolling derivative are computing and plotted. I found that this information
      is highly valuable during bull runs and sets of bull runs. I found that the SVD revealed information about peak buy/sell
      times. The derivative information tells you when the price is falling/rising, and the SVD of the derivative tells you
      about what time of the day this occurs.
      
  - You can tie your GDAX/Coinbase account to the analyzer by placing your API keys in the access directory for automated
    buying and selling.
    
    
Good luck and have fun. 

NOTE: I am not responsible for your financial situation after using these programs. Use at your own risk/benefit/failure. 
