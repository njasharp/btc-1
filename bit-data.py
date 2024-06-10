import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import cryptocompare

cryptocompare.cryptocompare._set_api_key_parameter('YOUR_CRYPTOCOMPARE_API_KEY')  # Replace with your CryptoCompare API key



def get_crypto_data(symbol, currency='USD', days=30):
    hist = cryptocompare.get_historical_price_day(symbol, currency=currency, limit=delta)
    df = pd.DataFrame(hist)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

def find_peaks(series):
    peaks = argrelextrema(series.values, np.greater)[0]
    troughs = argrelextrema(series.values, np.less)[0]
    return peaks, troughs

def fibonacci_retracement_and_extensions(series):
    max_price = series.max()
    min_price = series.min()
    
    diff = max_price - min_price
    
    levels = {
        '0.0%': max_price,
        '23.6%': max_price - 0.236 * diff,
        '38.2%': max_price - 0.382 * diff,
        '50.0%': max_price - 0.5 * diff,
        '61.8%': max_price - 0.618 * diff,
        '100.0%': min_price,
        '161.8%': min_price - 0.618 * diff,
        '261.8%': min_price - 1.618 * diff
    }
    
    return levels

def calculate_trend_lines(series, peaks, troughs):
    trend_lines = []
    for i in range(len(peaks) - 1):
        x1, y1 = peaks[i], series[peaks[i]]
        x2, y2 = peaks[i + 1], series[peaks[i + 1]]
        trend_lines.append(((x1, y1), (x2, y2)))
    
    for i in range(len(troughs) - 1):
        x1, y1 = troughs[i], series[troughs[i]]
        x2, y2 = troughs[i + 1], series[troughs[i + 1]]
        trend_lines.append(((x1, y1), (x2, y2)))
    
    return trend_lines

def calculate_risk_management(win_rate, risk_reward_ratio):
    profitability = []
    for win_percentage in np.linspace(0.1, 1, 10):
        expected_value = win_percentage * risk_reward_ratio - (1 - win_percentage)
        profitability.append((win_percentage, expected_value))
    
    return profitability

def calculate_trade_parameters(entry_price, stop_loss, take_profit, account_balance, risk_per_trade):
    risk_amount = account_balance * (risk_per_trade / 100)
    position_size = risk_amount / abs(entry_price - stop_loss)
    return position_size, risk_amount

def plot_psychological_trend_analysis():
    phases = ['Accumulation', 'Markup', 'Distribution', 'Decline']
    emotions = ['Disbelief', 'Hope', 'Optimism', 'Belief', 'Thrill', 'Euphoria', 
                'Anxiety', 'Denial', 'Panic', 'Capitulation', 'Anger', 'Depression']
    price = [1, 2, 4, 8, 16, 32, 20, 18, 15, 10, 5, 3, 2]
    
    colors = ['skyblue', 'lightgreen', 'khaki', 'lightcoral']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i in range(len(phases)):
        ax.axvspan(i * 3, (i + 1) * 3, color=colors[i], alpha=0.5, label=phases[i])
    
    ax.plot(range(len(price)), price, color='black', marker='o')
    
    for i, emotion in enumerate(emotions):
        ax.text(i, price[i] + 0.5, emotion, horizontalalignment='center')
    
    ax.set_title("Psychological Trend Analysis")
    ax.set_xlabel("Market Phases")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    ax.grid(True)
    
    st.pyplot(fig)

def plot_crypto(symbol):
    hist = get_crypto_data(symbol)
    hist['Date'] = hist.index

    peaks, troughs = find_peaks(hist['close'])
    
    fig, ax = plt.subplots(5, 1, figsize=(10, 30))
    
    # Plot Close Price with Peaks and Troughs
    ax[0].plot(hist['Date'], hist['close'], label="Close Price")
    ax[0].scatter(hist['Date'].values[peaks], hist['close'].values[peaks], color='green', label='Peaks')
    ax[0].scatter(hist['Date'].values[troughs], hist['close'].values[troughs], color='red', label='Troughs')
    ax[0].legend()
    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Close Price')
    ax[0].set_title(f'Crypto Price and Peaks for {symbol}')
    
    # Plot Fibonacci Retracement and Extensions
    levels = fibonacci_retracement_and_extensions(hist['close'])
    
    for level in levels:
        ax[1].axhline(y=levels[level], linestyle='--', label=level)
    
    ax[1].plot(hist['Date'], hist['close'], label="Close Price")
    ax[1].legend()
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel('Close Price')
    ax[1].set_title(f'Fibonacci Retracement and Extensions for {symbol}')
    
    # Plot Trend Lines and Channels
    trend_lines = calculate_trend_lines(hist['close'], peaks, troughs)
    
    ax[2].plot(hist['Date'], hist['close'], label="Close Price")
    
    for line in trend_lines:
        (x1, y1), (x2, y2) = line
        ax[2].plot([hist['Date'][x1], hist['Date'][x2]], [y1, y2], linestyle='--')
    
    ax[2].legend()
    ax[2].set_xlabel('Date')
    ax[2].set_ylabel('Close Price')
    ax[2].set_title(f'Trend Lines and Channels for {symbol}')
    
    # Plot Risk Management and Pro Trading Math
    win_rate = 0.5  # Example win rate
    risk_reward_ratio = 2  # Example risk-reward ratio
    profitability = calculate_risk_management(win_rate, risk_reward_ratio)
    
    win_rates, expected_values = zip(*profitability)
    
    ax[3].plot(win_rates, expected_values, label="Expected Value")
    ax[3].axhline(0, color='red', linestyle='--', label='Breakeven Line')
    ax[3].legend()
    ax[3].set_xlabel('Winning Percentage')
    ax[3].set_ylabel('Expected Value')
    ax[3].set_title(f'Risk Management and Pro Trading Math (R:R={risk_reward_ratio})')

    # Calculator Tool
    st.sidebar.title("Trade Calculator")
    entry_price = st.sidebar.number_input("Entry Price", value=100.0)
    stop_loss = st.sidebar.number_input("Stop Loss Price", value=95.0)
    take_profit = st.sidebar.number_input("Take Profit Price", value=110.0)
    account_balance = st.sidebar.number_input("Account Balance", value=10000.0)
    risk_per_trade = st.sidebar.slider("Risk per Trade (%)", min_value=0.5, max_value=10.0, value=1.0)
    
    if st.sidebar.button("Calculate"):
        position_size, risk_amount = calculate_trade_parameters(entry_price, stop_loss, take_profit, account_balance, risk_per_trade)
        
        ax[4].bar(['Position Size', 'Risk Amount'], [position_size, risk_amount], color=['blue', 'orange'])
        ax[4].set_title("Trade Parameters")
        ax[4].set_ylabel("Value")
    
    st.pyplot(fig)
    plot_psychological_trend_analysis()

st.title("Cryptocurrency Price Analysis")
crypto_symbol = st.selectbox("Select Cryptocurrency Symbol", options=["BTC", "ETH", "LTC", "XRP", "ADA"])
st.divider()

# Set up a Streamlit slider for selecting the number of days
delta = st.slider('Select number of days', 1, 365, value=30)


if crypto_symbol:
    plot_crypto(crypto_symbol)

st.info("built by dw")    