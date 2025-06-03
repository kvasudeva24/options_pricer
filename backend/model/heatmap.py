import yfinance as yf
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pricer import (call_option, put_option)

data = yf.Ticker("TSLA")
all_dates = data.options[:5]  # first 5 expiry dates (or more if you want)

results = []

for expiry in all_dates:
    chain = data.option_chain(expiry)
    calls = chain.calls

    # You already have this from earlier:
    curr_price = data.history(period="1d")["Close"].iloc[-1]
    lower_bound = 0.8 * curr_price
    upper_bound = 1.2 * curr_price

    for _, row in calls.iterrows():
        strike = row['strike']
        if not (lower_bound < strike < upper_bound):
            continue

        # Days to expiry
        days_to_expiry = (pd.to_datetime(expiry) - pd.Timestamp.now()).days

        listed_price = (row['bid'] + row['ask']) / 2
        calc_price = call_option("TSLA", 5, 20, days_to_expiry, strike)  # use your model

        diff = calc_price - listed_price
        results.append((strike, days_to_expiry, diff))


df = pd.DataFrame(results, columns=["Strike", "Days", "Diff"])
heatmap_df = df.pivot_table(index="Days", columns="Strike", values="Diff", fill_value=np.nan)

plt.figure(figsize=(10, 6))  # Increase figure size (bigger actual heatmap grid)

sns.heatmap(
    heatmap_df,
    cmap="coolwarm",
    center=0,
    cbar=True,
    annot=True,
    fmt=".2f",
    annot_kws={"size": 4},   # 👈 smaller font inside squares
    linewidths=0.3,
    linecolor="gray",
    square=False             # 👈 allow rectangular cells to fill space better
)

plt.xlabel("Strike Price", fontsize=12)
plt.ylabel("Days to Expiry", fontsize=12)
plt.title("Model vs Market Option Price Difference", fontsize=14)

plt.xticks(rotation=45, ha="right", fontsize=8)
plt.yticks(fontsize=8)

plt.tight_layout()
plt.show()


