import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm

# Volatility models
from backend.volatility import (
    historical_log_volatility,
    parkinsons_volatility,
    garman_klass_volatility,
    rogers_satchell_volatility,
    yang_zhang_volatility
)

# Global risk-free rate
risk_free_rate = 0.041

def call_option(ticker, option_vol, period_vol, period_opt, strike_price):
    """
    Calculate the BSM call option price for a given stock.

    Parameters: 
    ticker (str): Stock ticker symbol (e.g., 'AAPL')
    option_vol (int): Selector for volatility model (1=historical, ..., 5=yang-zhang)
    period_vol (int): Trading days used for volatility calculation
    period_opt (int): Trading days remaining until option expiration
    strike_price (float): Strike price of the option

    Returns:
    float: Call option price using the Black-Scholes-Merton model
    """

    if option_vol == 1:
        vol = historical_log_volatility(ticker, period_vol)
    elif option_vol == 2:
        vol = parkinsons_volatility(ticker, period_vol)
    elif option_vol == 3:
        vol = garman_klass_volatility(ticker, period_vol)
    elif option_vol == 4:
        vol = rogers_satchell_volatility(ticker, period_vol)
    else:
        vol = yang_zhang_volatility(ticker, period_vol)

    # Fetch current stock price
    data = yf.Ticker(ticker)
    hist = data.history(period="1d")
    stock_price = hist["Close"].iloc[-1]

    # Convert time to years
    adjusted_T = period_opt / 252.0

    # Black-Scholes-Merton calculation
    d1 = (np.log(stock_price / strike_price) + (risk_free_rate + 0.5 * vol ** 2) * adjusted_T) / (vol * np.sqrt(adjusted_T))
    d2 = d1 - vol * np.sqrt(adjusted_T)

    call_price = stock_price * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * adjusted_T) * norm.cdf(d2)
    return call_price


def put_option(ticker, option_vol, period_vol, period_opt, strike_price):
    """
    Calculate the BSM put option price for a given stock.

    Parameters: 
    ticker (str): Stock ticker symbol (e.g., 'AAPL')
    option_vol (int): Selector for volatility model (1=historical, ..., 5=yang-zhang)
    period_vol (int): Trading days used for volatility calculation
    period_opt (int): Trading days remaining until option expiration
    strike_price (float): Strike price of the option

    Returns:
    float: Put option price using the Black-Scholes-Merton model
    """

    if option_vol == 1:
        vol = historical_log_volatility(ticker, period_vol)
    elif option_vol == 2:
        vol = parkinsons_volatility(ticker, period_vol)
    elif option_vol == 3:
        vol = garman_klass_volatility(ticker, period_vol)
    elif option_vol == 4:
        vol = rogers_satchell_volatility(ticker, period_vol)
    else:
        vol = yang_zhang_volatility(ticker, period_vol)

    # Fetch current stock price
    data = yf.Ticker(ticker)
    hist = data.history(period="1d")
    stock_price = hist["Close"].iloc[-1]

    # Convert time to years
    adjusted_T = period_opt / 252.0

    # Black-Scholes-Merton calculation
    d1 = (np.log(stock_price / strike_price) + (risk_free_rate + 0.5 * vol ** 2) * adjusted_T) / (vol * np.sqrt(adjusted_T))
    d2 = d1 - vol * np.sqrt(adjusted_T)

    put_price = strike_price * np.exp(-risk_free_rate * adjusted_T) * norm.cdf(-d2) - stock_price * norm.cdf(-d1)
    return put_price