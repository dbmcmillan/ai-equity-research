# Create charts of stock price vs SPY over time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from stock_history import fetch_stock_data_db

ticker = "CROX"
ticker_df = fetch_stock_data_db(ticker)
spy_df = fetch_stock_data_db("SPY")

def create_stock_vs_spy_chart(ticker_df, spy_df, ticker):
    #Filter data for the ticker and SPY
    stock_df = ticker_df.reset_index()
    stock_df["Close"] = stock_df["Close"]/stock_df["Close"].iloc[0] * 100  # Normalize to 100 at the start date
    colors = ['green' if c>=o else 'red' for o,c in zip(stock_df['Open'], stock_df['Close'])]
    spy_df = spy_df.reset_index()
    spy_df["Close"] = spy_df["Close"]/spy_df["Close"].iloc[0] * 100  # Normalize to 100 at the start date
    #Merge data on Date
    #Create a candlestick chart without wicks for the stock and line chart for SPY, using the color scheme defined above
    fig= go.Figure()
    # fig.add_trace(go.Bar(x=stock_df['Date'], y=stock_df['Close'] - stock_df['Open'], base=stock_df['Open'], marker_color=colors, name=ticker))
    fig.add_trace(go.Scatter(x=stock_df['Date'], y=stock_df['Close'], mode='lines',line=dict(color='orange'), name=f'{ticker} Close Price'))

    #Create a line chart for SPY close price with secondary y-axis
    fig.add_trace(go.Scatter(x=spy_df['Date'], y=spy_df['Close'], mode='lines', name='SPY', line=dict(color='blue')))
    # Create axis objects
    fig.update_layout(
        title=f"How $100 invested in {ticker} vs SPY would have performed",
        yaxis_title=f"{ticker} Stock Price",
        yaxis2=dict(
            title="SPY Close Price",
            overlaying='y',
            side='right'
        ),
        xaxis_rangeslider_visible=False
    )
    return fig
#Display the chart
fig = create_stock_vs_spy_chart(ticker_df, spy_df, ticker)
#Save the chart as HTML
fig.write_html(f"reports/{ticker}_vs_SPY_chart.html")
print(f"Stock vs SPY chart saved to: reports/{ticker}_vs_SPY_chart.html")
