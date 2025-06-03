import yfinance as yf
import numpy as np
import pandas as pd
from pricer import (call_option, put_option)

ticker = "TSLA"
data = yf.Ticker(ticker)
hist = data.history(period="1d")
all_dates = data.options #dynamically get the option dates 
print(all_dates) 


opt_chain = data.option_chain("2025-06-06")
call_opt = opt_chain.calls
# put_opt = opt_chain.puts

curr_price = hist["Close"].iloc[-1]
lower_bound = 0.8 * curr_price
upper_bound = 1.2 * curr_price

filtered_rows = []

for i, row in call_opt.iterrows():
    if lower_bound < row['strike'] < upper_bound:
        filtered_rows.append(row)

filtered = pd.DataFrame(filtered_rows)
print(filtered) #getting all the prices within 20% of an option 

data_array = [[]]


print(type(call_opt)) #it is a pandas dataframe