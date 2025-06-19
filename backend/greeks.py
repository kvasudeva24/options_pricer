import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm
from volatility import (
    historical_log_volatility,
    parkinsons_volatility,
    garman_klass_volatility,
    rogers_satchell_volatility,
    yang_zhang_volatility
)

risk_free_rate = 0.041

def get_greeks(strike, vol, output):
    return False


def get_delta(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output):
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

    data = yf.Ticker(ticker)
    hist = data.history(period="1d")
    stock_price = hist["Close"].iloc[-1]
    new_stock_price = stock_price + 1

    # Convert time to years
    adjusted_T = period_opt / 252.0

    # Black-Scholes-Merton calculation
    d1 = (np.log(new_stock_price / strike_price) + (risk_free_rate + 0.5 * vol ** 2) * adjusted_T) / (vol * np.sqrt(adjusted_T))
    d2 = d1 - vol * np.sqrt(adjusted_T)

    if(opt_type == 0):
        new_option_price = new_stock_price * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * adjusted_T) * norm.cdf(d2)
    else:
        new_option_price = strike_price * np.exp(-risk_free_rate * adjusted_T) * norm.cdf(-d2) - new_stock_price * norm.cdf(-d1)

    return (new_option_price - output)/(new_stock_price - stock_price)
