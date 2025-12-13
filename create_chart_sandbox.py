# Create a chart using plotly to compare RHI's stock price (use fetch_stock_data_db function for stock data) vs the 10 year treasury yield (import this data from csv)

from turtle import color
import plotly.graph_objects as go
import pandas as pd
import sqlite3
from datetime import datetime
from stock_history import fetch_stock_data_db

ticker_df = fetch_stock_data_db("CROX")

ten_year_df = pd.read_csv('10Y_Treasury_Data.csv')
ten_year_df['Date'] = pd.to_datetime(ten_year_df['Date'])
ticker_df = ticker_df.resample('W').last()  # weekly stock prices
ten_year_df = ten_year_df.resample('W', on='Date').last()  # weekly 10Y yields
print(ticker_df.head())
#Plot the series on the same chart as lines, use left y-axis for stock price, right y-axis for treasury yield
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=ticker_df.index,
    y=ticker_df['Close'],
    mode='lines',
    name='CROX Stock Price',
    line=dict(color='green', width=3)
))
fig.add_trace(go.Scatter(
    x=ten_year_df.index,
    y=ten_year_df['Yield'],
    mode='lines',
    name='10Y Treasury Yield',
    line=dict(color='blue', width=2),
    yaxis='y2'
))

fig.update_layout(
    title="RHI Stock Price vs 10-Year Treasury Yield",
    xaxis_title='Date',
    yaxis=dict(title='RHI Stock Price ($)', showgrid=True, gridcolor='LightGray'),
    yaxis2=dict(title='10Y Treasury Yield (%)', overlaying='y', side='right'),
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0)', bordercolor='Black', borderwidth=1)
)
fig.update_layout(template='ggplot2')
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray', showline=True, linewidth=1, linecolor='Black')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray', showline=True, linewidth=1, linecolor='Black')
fig.update_layout(
    legend=dict(
        x=0.01,  # left/right position (0=left, 1=right)
        y=0.99,  # top/bottom position (0=bottom, 1=top)
        bgcolor='rgba(255,255,255,0.8)',  # semi-transparent background
        bordercolor='Black',
        borderwidth=1,
        font=dict(size=16)
    )
)
fig.update_traces(
    marker=dict(size=12),   # mostly affects scatter points
    selector=dict(mode='lines+markers')
)
# Make the axis labels bigger
fig.update_layout(
    xaxis=dict(tickfont=dict(size=16)),
    yaxis=dict(tickfont=dict(size=16)),
    yaxis2=dict(tickfont=dict(size=16))
)

#Make the axis titles bigger
fig.update_layout(
    title=dict(font=dict(size=20)),
    xaxis_title_text="Date",
    xaxis_title_font_size=18,
    yaxis_title_text="RHI Stock Price ($)",
    yaxis_title_font_size=18,
    yaxis2_title_text="10Y Treasury Yield (%)",
    yaxis2_title_font_size=18
)
# Add annotations/markers on the 10Y treasury line for March 16th 2022, May 4th 2022, June 15th 2022, July 27th 2022, September 21st 2022, November 2nd 2022, December 14th 2022, July 26th 2023 as dates on which the Federal Reserve announced interest rate increases
dates = [datetime(2022, 3, 16), datetime(2022, 5, 4), datetime(2022, 6, 15), datetime(2022, 7, 27), datetime(2022, 9, 21), datetime(2022, 11, 2), datetime(2022, 12, 14), datetime(2023, 7, 26)]
for date in dates:
    nearest_idx = ticker_df.index.get_indexer(pd.Index([date]), method='nearest')[0]
    y_val = ticker_df.iloc[nearest_idx]['Close']

    fig.add_trace(
    go.Scatter(
        x=[ticker_df.index[nearest_idx]],
        y=[y_val],
        mode='markers',
        marker=dict(
            size=10,
            color='red',
            symbol='circle'
        ),
        name='Fed Rate Increase',
        showlegend=False  # set True if you want it once
    )
)

print("Figure successfully created")

#Save it to the visualizations folder
fig.write_html("Visualizations/CROX_vs_10Y_Treasury.html")

BIRK_df = fetch_stock_data_db("BIRK")
NKE_df = fetch_stock_data_db("NKE")
DECK_df = fetch_stock_data_db("DECK")
LULU_df = fetch_stock_data_db("LULU")
SPY_df = fetch_stock_data_db("SPY")
BIRK_df = BIRK_df.resample('W').last()  # weekly stock prices
NKE_df = NKE_df.resample('W').last()  # weekly stock prices
DECK_df = DECK_df.resample('W').last()  # weekly stock prices
BIRK_df['Close'] = BIRK_df['Close']/BIRK_df['Close'].iloc[0] * 100
NKE_df['Close'] = NKE_df['Close']/NKE_df['Close'].iloc[0] * 100
DECK_df['Close'] = DECK_df['Close']/DECK_df['Close'].iloc[0] * 100
ticker_df['Close'] = ticker_df['Close']/ticker_df['Close'].iloc[0] * 100
LULU_df = LULU_df.resample('W').last()  # weekly stock prices
LULU_df['Close'] = LULU_df['Close']/LULU_df['Close'].iloc[0] * 100
SPY_df = SPY_df.resample('W').last()  # weekly stock prices
SPY_df['Close'] = SPY_df['Close']/SPY_df['Close'].iloc[0] * 100
#Create a chart showing lines for all four stocks.
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=BIRK_df.index,
    y=BIRK_df['Close'],
    mode='lines',
    name='BIRK',
    line=dict(width=1),
    marker=dict(color='purple')
))
fig1.add_trace(go.Scatter(
    x=NKE_df.index,
    y=NKE_df['Close'],
    mode='lines',
    name='NKE',
    line=dict(width=1),
    marker=dict(color='blue')
))
fig1.add_trace(go.Scatter(
    x=DECK_df.index,
    y=DECK_df['Close'],
    mode='lines',
    name='DECK',
    line=dict(width=1),
    marker=dict(color='orange')
))
fig1.add_trace(go.Scatter(
    x=LULU_df.index,
    y=LULU_df['Close'],
    mode='lines',
    name='LULU',
    line=dict(width=1),
    marker=dict(color='teal')
))
fig1.add_trace(go.Scatter(
    x = ticker_df.index,
    y = ticker_df['Close'],
    mode='lines',
    name='CROX',
    line=dict(width=3),
    marker=dict(color='red')
))
fig1.add_trace(go.Scatter(
    x=SPY_df.index,
    y=SPY_df['Close'],
    mode='lines',
    name='SPY',
    line=dict(width=3),
    marker=dict(color='green')
))

fig1.update_layout(
    title="How $100 Invested in CROX, Competitors, and SPY Would Have Performed Over 5 Years",
    xaxis_title='Date',
    yaxis=dict(title='Value ($)', showgrid=True, gridcolor='LightGray'),
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0)', bordercolor='Black', borderwidth=1)
)
fig1.update_layout(template='ggplot2')

# Make the axis labels bigger
fig1.update_layout(
    xaxis=dict(tickfont=dict(size=16)),
    yaxis=dict(tickfont=dict(size=16))
)
#Make the axis titles bigger
fig1.update_layout(
    title=dict(font=dict(size=20)),
    xaxis_title_text="Date",
    xaxis_title_font_size=18,
    yaxis_title_text="Value ($)",
    yaxis_title_font_size=18
)
# Put a marker on the final data point for each stock with the value
for df, name in [(BIRK_df, 'BIRK'), (NKE_df, 'NKE'), (DECK_df, 'DECK'), (LULU_df, 'LULU'), (ticker_df, 'CROX'), (SPY_df, 'SPY')]:
    fig1.add_trace(
        go.Scatter(
            x=[df.index[-1]],
            y=[df['Close'].iloc[-1]],
            mode='markers+text',
            marker=dict(
                size=10,
                color='black',
                symbol='circle'
            ),
            text=[f"{name} ${df['Close'].iloc[-1]:.2f}"],
            textposition="top center",
            name=f'{name} Final Value',
            showlegend=False
        )
    )
# Make the lines smoother
fig1.update_traces(line_shape='spline')
# Save it to the visualizations folder
fig1.write_html("Visualizations/CROX_Competitors_vs_SPY.html")