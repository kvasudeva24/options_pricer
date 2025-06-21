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

def get_greeks(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output):
    data = yf.Ticker(ticker)
    hist = data.history(period="1d")
    stock_price = hist["Close"].iloc[-1]
    output = {
        'Delta': get_delta(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output, stock_price),
        'Gamma': get_gamma(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output, stock_price),
        'Theta': get_theta(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output, stock_price),
        'Rho': get_rho(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output, stock_price)
    }
    return output


def get_delta(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output, stock_price):
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

    return (new_option_price - output)

def get_gamma(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output, stock_price):
    curr_delta = get_delta(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output, stock_price)
    new_delta = get_delta(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output, stock_price+1)
    return (new_delta-curr_delta)

def get_theta(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output, stock_price):
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

    # Convert time to years
    adjusted_T = period_opt / 252.0
    new_adjusted_T = adjusted_T - (1/252)

    # Black-Scholes-Merton calculation
    d1 = (np.log(stock_price / strike_price) + (risk_free_rate + 0.5 * vol ** 2) * new_adjusted_T) / (vol * np.sqrt(new_adjusted_T))
    d2 = d1 - vol * np.sqrt(new_adjusted_T)

    if(opt_type == 0):
        new_option_price = stock_price * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * new_adjusted_T) * norm.cdf(d2)
    else:
        new_option_price = strike_price * np.exp(-risk_free_rate * new_adjusted_T) * norm.cdf(-d2) - stock_price * norm.cdf(-d1)

    return (new_option_price - output)/(-1)

def get_rho(opt_type, ticker, strike_price ,option_vol, period_vol, period_opt, output, stock_price):
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

    # Convert time to years
    adjusted_T = period_opt / 252.0

    #new rfir
    new_risk_free_rate = risk_free_rate + 0.01

    # Black-Scholes-Merton calculation
    d1 = (np.log(stock_price / strike_price) + (new_risk_free_rate + 0.5 * vol ** 2) * adjusted_T) / (vol * np.sqrt(adjusted_T))
    d2 = d1 - vol * np.sqrt(adjusted_T)

    if(opt_type == 0):
        new_option_price = stock_price * norm.cdf(d1) - strike_price * np.exp(-new_risk_free_rate * adjusted_T) * norm.cdf(d2)
    else:
        new_option_price = strike_price * np.exp(-new_risk_free_rate * adjusted_T) * norm.cdf(-d2) - stock_price * norm.cdf(-d1)

    return (new_option_price - output)/(0.01)