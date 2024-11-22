import pandas as pd
import numpy as np
import json
from datetime import datetime

# Load historical data from JSON
def load_historical_data(symbol):
    with open(f"{symbol}_historical_data.json", "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)

# Backtest the Bollinger Bands strategy
def backtest_bollinger_bands(df, window=20, num_std_dev=2, initial_balance=100000):
    df['Middle Band'] = df['Close'].rolling(window=window).mean()
    df['Upper Band'] = df['Middle Band'] + (df['Close'].rolling(window=window).std() * num_std_dev)
    df['Lower Band'] = df['Middle Band'] - (df['Close'].rolling(window=window).std() * num_std_dev)

    df['Signal'] = 0
    df.loc[window:, 'Signal'] = np.where(df['Close'][window:] < df['Lower Band'][window:], 1, 0)  # Buy signal
    df.loc[window:, 'Signal'] = np.where(df['Close'][window:] > df['Upper Band'][window:], -1, df['Signal'][window:])  # Sell signal
    df['Position'] = df['Signal'].diff()

    balance = initial_balance
    shares = 0
    trade_log = []

    for index, row in df.iterrows():
        if row['Position'] == 1:  # Buy signal
            shares_to_buy = balance // row['Close']
            balance -= shares_to_buy * row['Close']
            trade_log.append({'Date': row['Date'], 'Action': 'BUY', 'Price': row['Close'], 'Shares': shares_to_buy, 'Balance': balance})
            shares += shares_to_buy
        elif row['Position'] == -1 and shares > 0:  # Sell signal
            balance += shares * row['Close']
            trade_log.append({'Date': row['Date'], 'Action': 'SELL', 'Price': row['Close'], 'Shares': shares, 'Balance': balance})
            shares = 0

    if shares > 0:  # Sell remaining shares
        balance += shares * df['Close'].iloc[-1]
        trade_log.append({'Date': df['Date'].iloc[-1], 'Action': 'SELL (EOD)', 'Price': df['Close'].iloc[-1], 'Shares': shares, 'Balance': balance})

    trade_log_df = pd.DataFrame(trade_log)
    total_gain_loss = balance - initial_balance
    total_return = (balance / initial_balance - 1) * 100
    trading_days = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days
    annual_return = (1 + (total_return / 100)) ** (365 / trading_days) - 1
    annual_return *= 100

    trade_log_df.to_csv('bollinger_trade_log.csv', index=False)
    print(f"Bollinger Bands - Total Gain/Loss: ${total_gain_loss:.2f}, Total Return: {total_return:.2f}%, Annual Return: {annual_return:.2f}%")

# Backtest the MACD strategy
def backtest_macd(df, short_window=12, long_window=26, signal_window=9, initial_balance=100000):
    df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()

    df['Signal'] = 0
    df.loc[1:, 'Signal'] = np.where(df['MACD'][1:] > df['Signal Line'][1:], 1, 0)  # Buy signal
    df.loc[1:, 'Signal'] = np.where(df['MACD'][1:] < df['Signal Line'][1:], -1, df['Signal'][1:])  # Sell signal
    df['Position'] = df['Signal'].diff()

    balance = initial_balance
    shares = 0
    trade_log = []

    for index, row in df.iterrows():
        if row['Position'] == 1:  # Buy signal
            shares_to_buy = balance // row['Close']
            balance -= shares_to_buy * row['Close']
            trade_log.append({'Date': row['Date'], 'Action': 'BUY', 'Price': row['Close'], 'Shares': shares_to_buy, 'Balance': balance})
            shares += shares_to_buy
        elif row['Position'] == -1 and shares > 0:  # Sell signal
            balance += shares * row['Close']
            trade_log.append({'Date': row['Date'], 'Action': 'SELL', 'Price': row['Close'], 'Shares': shares, 'Balance': balance})
            shares = 0

    if shares > 0:  # Sell remaining shares
        balance += shares * df['Close'].iloc[-1]
        trade_log.append({'Date': df['Date'].iloc[-1], 'Action': 'SELL (EOD)', 'Price': df['Close'].iloc[-1], 'Shares': shares, 'Balance': balance})

    trade_log_df = pd.DataFrame(trade_log)
    total_gain_loss = balance - initial_balance
    total_return = (balance / initial_balance - 1) * 100
    trading_days = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days
    annual_return = (1 + (total_return / 100)) ** (365 / trading_days) - 1
    annual_return *= 100

    trade_log_df.to_csv('macd_trade_log.csv', index=False)
    print(f"MACD - Total Gain/Loss: ${total_gain_loss:.2f}, Total Return: {total_return:.2f}%, Annual Return: {annual_return:.2f}%")

# Backtest the SMA strategy
def backtest_sma(df, short_window=50, long_window=200, initial_balance=100000):
    df['SMA50'] = df['Close'].rolling(window=short_window).mean()
    df['SMA200'] = df['Close'].rolling(window=long_window).mean()

    df['Signal'] = 0
    df.loc[short_window:, 'Signal'] = np.where(df['SMA50'][short_window:] > df['SMA200'][short_window:], 1, 0)  # Buy signal
    df['Position'] = df['Signal'].diff()

    balance = initial_balance
    shares = 0
    trade_log = []

    for index, row in df.iterrows():
        if row['Position'] == 1:  # Buy signal
            shares_to_buy = balance // row['Close']
            balance -= shares_to_buy * row['Close']
            trade_log.append({'Date': row['Date'], 'Action': 'BUY', 'Price': row['Close'], 'Shares': shares_to_buy, 'Balance': balance})
            shares += shares_to_buy
        elif row['Position'] == -1 and shares > 0:  # Sell signal
            balance += shares * row['Close']
            trade_log.append({'Date': row['Date'], 'Action': 'SELL', 'Price': row['Close'], 'Shares': shares, 'Balance': balance})
            shares = 0

    if shares > 0:  # Sell remaining shares
        balance += shares * df['Close'].iloc[-1]
        trade_log.append({'Date': df['Date'].iloc[-1], 'Action': 'SELL (EOD)', 'Price': df['Close'].iloc[-1], 'Shares': shares, 'Balance': balance})

    trade_log_df = pd.DataFrame(trade_log)
    total_gain_loss = balance - initial_balance
    total_return = (balance / initial_balance - 1) * 100
    trading_days = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days
    annual_return = (1 + (total_return / 100)) ** (365 / trading_days) - 1
    annual_return *= 100

    trade_log_df.to_csv('sma_trade_log.csv', index=False)
    print(f"SMA - Total Gain/Loss: ${total_gain_loss:.2f}, Total Return: {total_return:.2f}%, Annual Return: {annual_return:.2f}%")

# Main execution
if __name__ == "__main__":
    symbol = 'FNGU'
    df = load_historical_data(symbol)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)

    # Backtest all strategies
    backtest_bollinger_bands(df)
    backtest_macd(df)
    backtest_sma(df)
