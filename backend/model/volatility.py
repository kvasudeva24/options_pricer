import yfinance as yf
import pandas as pd
import numpy as np


ticker = "AAPL"
data = yf.Ticker(ticker)
hist = data.history(period="1d")
print(hist)


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

def parkinsons_volatility(ticker, period):
    """
    Calculate parkinsons volatility of a stock in a given period.

    Parameters: 
    ticker: Stock ticker
    period: Period in trading days to calculate volatility

    Returns: Annualized Parkinsons volatility as a float

    """

    data = yf.Ticker(ticker)
    hist = data.history(period=f"{period}d")
    high_prices = np.array(hist["High"]) #high prices
    low_prices = np.array(hist["Low"]) #low prices
    prices_squared = np.log(high_prices/low_prices) ** 2 #ratio^^2
    parkinson_constant = 1/(4 * np.log(2)) #constant
    log_prices_squared = parkinson_constant * prices_squared #apply c to list 
    return np.sqrt(np.mean(log_prices_squared)) * np.sqrt(252) #find the averaqe


def garman_klass_volatility(ticker, period):
    """
    Calculate Garman-Klass volatility of a stock in a given period.

    Parameters: 
    ticker: Stock ticker
    period: Period in trading days to calculate volatility

    Returns: Annualized Garman-Klass volatility as a float

    """
    data = yf.Ticker(ticker)
    hist = data.history(period=f"{period}d")
    open_prices = np.array(hist["Open"])
    close_prices = np.array(hist["Close"])
    high_prices = np.array(hist["High"])
    low_prices = np.array(hist["Low"])

    log_hl_squared = np.log(high_prices/low_prices) ** 2
    term1 = 0.5 * log_hl_squared

    log_co_squared = np.log(close_prices/open_prices)**2
    term2 = (2*np.log(2) - 1) * log_co_squared

    diff = term1-term2
    return np.sqrt(np.mean(diff)) * np.sqrt(252)

print(garman_klass_volatility(ticker, 1))