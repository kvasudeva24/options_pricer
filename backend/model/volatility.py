import yfinance as yf
import pandas as pd
import numpy as np


ticker = "AAPL"
data = yf.Ticker(ticker)
hist = data.history(period="252d")
returns = hist["Close"]

def historical_volatility(ticker, period):
    """
    Calculate historical volatility (on closing prices) of a stock in a given period.
    
    Parameters:
    ticker: Stock ticker
    period: Period in days to calculate volatility

    Returns: Historical volatility as a float
    """
    data = yf.Ticker(ticker) #fetch data
    hist = data.history(period=f"{period}d") #get historical data 
    closing_prices = hist["Close"] 
    closing_prices = np.array(closing_prices) #get values as numpy array
    returns = np.zeros(closing_prices.shape[0]) #initialize returns
    for i in range(1, len(closing_prices)):
        returns[i] = ((closing_prices[i] - closing_prices[i-1])/closing_prices[i-1])
    returns = returns[1:] #remove first element 
    volatility = np.std(returns) #Std dev of returns
    return volatility * np.sqrt(252) #Annualize the volatility



