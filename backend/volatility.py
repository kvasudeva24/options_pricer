import yfinance as yf
import pandas as pd
import numpy as np



def historical_log_volatility(ticker, period):
    """
    Calculate annualized historical volatility using log returns.
    
    Parameters: 
    ticker: Stock ticker
    period: Number of trading days

    Returns: Annualized historical volatility (float)
    """
    data = yf.Ticker(ticker)
    hist = data.history(period=f"{period}d")
    closing_prices = np.array(hist["Close"])
    
    # Log returns
    log_returns = np.log(closing_prices[1:] / closing_prices[:-1])
    
    # Daily std dev of log returns, then annualize
    daily_vol = np.std(log_returns, ddof=1)  # ddof=1 for sample std
    return daily_vol * np.sqrt(252)

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
    low_prices = np.array(hist["Low"]) #get data

    log_hl_squared = np.log(high_prices/low_prices) ** 2
    term1 = 0.5 * log_hl_squared #term 1

    log_co_squared = np.log(close_prices/open_prices)**2
    term2 = (2*np.log(2) - 1) * log_co_squared #term 2

    diff = term1-term2 #calculate diff
    return np.sqrt(np.mean(diff)) * np.sqrt(252) #return annulaized 


def rogers_satchell_volatility(ticker, period):
    """
    Calculate Rogers-Satchell volatility of a stock in a given period.
    

    Parameters: 
    ticker: Stock ticker
    period: Period in trading days to calculate volatility

    Returns: Annualized Rogers-Satchell volatility as a float

    """

    data = yf.Ticker(ticker)
    hist = data.history(period=f"{period}d")
    open_prices = np.array(hist["Open"])
    close_prices = np.array(hist["Close"])
    high_prices = np.array(hist["High"])
    low_prices = np.array(hist["Low"]) #get the data

    term1 = np.log(high_prices/close_prices)
    term2 = np.log(high_prices/open_prices)
    term3 = np.log(low_prices/close_prices)
    term4 = np.log(low_prices/open_prices) #find the terms

    t12 = term1 * term2
    t34 = term3*term4
    summ = t12 + t34 #math
    return np.sqrt(np.mean(summ)) * np.sqrt(252) #return annulaized volatility


def yang_zhang_volatility(ticker, period):
    """
    Calculate Yang-Zhang volatility of a stock in a given period.
    

    Parameters: 
    ticker: Stock ticker
    period: Period in trading days to calculate volatility

    Returns: Annualized Yang-Zhang volatility as a float

    """

    data = yf.Ticker(ticker)
    hist = data.history(period=f"{period}d")
    open_prices = np.array(hist["Open"])
    close_prices = np.array(hist["Close"])
    high_prices = np.array(hist["High"])
    low_prices = np.array(hist["Low"]) #get the data

    log_cc_returns = np.log(close_prices[1:]/close_prices[:-1])
    close_close_variance = np.var(log_cc_returns, ddof=1)

    log_overnight_returns = np.log(open_prices[1:]/close_prices[:-1])
    overnight_variance = np.var(log_overnight_returns, ddof=1)

    term1 = np.log(high_prices/close_prices)
    term2 = np.log(high_prices/open_prices)
    term3 = np.log(low_prices/close_prices)
    term4 = np.log(low_prices/open_prices) #find the terms

    t12 = term1 * term2
    t34 = term3*term4
    summ = t12 + t34 #math
    rs_variance = np.mean(summ)

    k = 0.34/(1.34 + ((period+1)/(period-1)))

    return np.sqrt((k*overnight_variance) + (1-k)*close_close_variance + rs_variance) * np.sqrt(252)

