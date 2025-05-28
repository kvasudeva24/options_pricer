import yfinance as yf
import pandas as pd
import numpy as np


ticker = "AAPL"
data = yf.Ticker(ticker)
hist = data.history(period="1y")
print(hist)


