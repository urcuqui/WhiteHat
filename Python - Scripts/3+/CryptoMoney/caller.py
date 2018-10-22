# author: Christian Urcuqui
# Date: 22 october 2018
# this code allows us to use APIs from different sources in order to know the value of the different crypto monies
import requests
from coinmarketcap import Market

coinmarketcap = Market()

print(coinmarketcap.stats())

print(coinmarketcap.ticker("steem"))