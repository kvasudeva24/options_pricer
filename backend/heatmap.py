import yfinance as yf
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io 
import base64
from backend.pricer import (call_option, put_option)

def call_option_heatmap(ticker, option_vol, period_vol):
    data = yf.Ticker(ticker)
    all_dates = data.options[:5]  # first 5 expiry dates

    results = []

    curr_price = data.history(period="1d")["Close"].iloc[-1]
    lower_bound = 0.8 * curr_price
    upper_bound = 1.2 * curr_price

    for expiry in all_dates:
        chain = data.option_chain(expiry)
        calls = chain.calls

        for _, row in calls.iterrows():
            strike = row['strike']
            if not (lower_bound < strike < upper_bound):
                continue

            # Days to expiry
            days_to_expiry = math.ceil((pd.to_datetime(expiry) - pd.Timestamp.now()).total_seconds() / 86400)
            if days_to_expiry <= 0:
                continue

            bid = row['bid']
            ask = row['ask']

            listed_price = (bid + ask) / 2
            try:
                calc_price = call_option(ticker, option_vol, period_vol, days_to_expiry, strike)
                if np.isnan(calc_price):
                    continue
            except Exception:
                continue

            diff = calc_price - listed_price
            results.append((strike, days_to_expiry, diff))

    df = pd.DataFrame(results, columns=["Strike", "Days", "Diff"])
    heatmap_df = df.pivot_table(index="Days", columns="Strike", values="Diff", fill_value=np.nan)

    plt.figure(figsize=(12, 7))
    sns.heatmap(
        heatmap_df,
        cmap="coolwarm",
        center=0,
        cbar=True,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 4},
        linewidths=0.3,
        linecolor="gray",
        square=False
    )

    plt.xlabel("Strike Price", fontsize=12)
    plt.ylabel("Days to Expiry", fontsize=12)
    plt.title(f"{ticker} - Model vs Market Call Option Price Difference", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close() 
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def put_option_heatmap(ticker, option_vol, period_vol):
    data = yf.Ticker(ticker)
    all_dates = data.options[:5]  # first 5 expiry dates

    results = []

    curr_price = data.history(period="1d")["Close"].iloc[-1]
    lower_bound = 0.8 * curr_price
    upper_bound = 1.2 * curr_price

    for expiry in all_dates:
        chain = data.option_chain(expiry)
        puts = chain.puts

        for _, row in puts.iterrows():
            strike = row['strike']
            if not (lower_bound < strike < upper_bound):
                continue

            # Days to expiry
            days_to_expiry = math.ceil((pd.to_datetime(expiry) - pd.Timestamp.now()).total_seconds() / 86400)
            if days_to_expiry <= 0:
                continue

            listed_price = (row['bid'] + row['ask']) / 2
            try:
                calc_price = put_option(ticker, option_vol, period_vol, days_to_expiry, strike)
                if np.isnan(calc_price):
                    continue
            except Exception:
                continue

            diff = calc_price - listed_price
            results.append((strike, days_to_expiry, diff))

    df = pd.DataFrame(results, columns=["Strike", "Days", "Diff"])
    heatmap_df = df.pivot_table(index="Days", columns="Strike", values="Diff", fill_value=np.nan)

    plt.figure(figsize=(12, 7))
    sns.heatmap(
        heatmap_df,
        cmap="coolwarm",
        center=0,
        cbar=True,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 4},
        linewidths=0.3,
        linecolor="gray",
        square=False
    )

    plt.xlabel("Strike Price", fontsize=12)
    plt.ylabel("Days to Expiry", fontsize=12)
    plt.title(f"{ticker} - Model vs Market Put Option Price Difference", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close() 
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64