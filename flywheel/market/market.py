import yfinance as yf
import json

from datetime import date

market_date = date.today()

def set_date(date):
    global market_date
    market_date = date

def get_price_on_date(ticker, date):
    # test data
    if ticker == 'GOOG':
        return 100
    if ticker == 'PINS':
        return 50
    return 0

def get_price(ticker):
    print("Get price for {} on {}".format(ticker, market_date))

    with open('stock_data.json', 'r') as json_file:
        stock_data = json.load(json_file)
        if ticker not in stock_data or market_date not in stock_data[ticker]:
            return update_stock_data(stock_data, ticker, market_date)
        else:
            return stock_data[ticker][market_date]


def update_stock_data(stock_data, ticker, market_date):
    stock = yf.Ticker(ticker)
    stock_history_price_dict = crawl_stock_history_price(stock, "100d", "60m")

    # overwrites ticker history price data, updates the stock data and stores as json file
    stock_data[ticker] = stock_history_price_dict
    with open('stock_data.json', 'w') as json_file:
        json.dump(stock_data, json_file)
    return stock_data[ticker][market_date]


def crawl_stock_history_price(stock_ticker, period="100d", interval="60m"):
    # TODO
    return 100