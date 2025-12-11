# Create charts of stock price vs SPY over time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from stock_history import fetch_stock_data_db
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

# Create a chart showing prior values of Revenue, EBIT, Net Income, and Free Cash Flow, and the projected values from the forecast table over time
import pandas as pd
from download_financials import download_financials_db
from forecast_from_projections import create_forecast_table
ticker = "CROX"
all_financials = download_financials_db(ticker)
#Load projections table from csv file
projections_table = pd.read_csv(f"reports/{ticker}_Projections_Table.csv", index_col=0)
# Only keep rows where "Case" column is "Base"
projections_table = projections_table[projections_table['Case'] == 'Base']
projections_table = projections_table.drop(columns=['Case'])
projections_table = projections_table[projections_table.index != 'TV']
forecast_table = create_forecast_table(projections_table, all_financials)
def create_financials_forecast_chart(all_financials: pd.DataFrame, forecast_table: pd.DataFrame, ticker: str):
    #Get historical data
    # ...existing code...

    # use DatetimeIndex so the type-checker recognizes .year
    historical_years = pd.DatetimeIndex(all_financials.index).year.tolist()
    revenue_hist = all_financials['Total Revenue'].round(2).tolist()
    ebit_hist = all_financials['EBIT'].round(2).tolist()
    net_income_hist = all_financials['Net Income'].round(2).tolist()
    fcf_hist = all_financials['Free Cash Flow'].round(2).tolist()
    #Get forecast data
    forecast_table.index = forecast_table.index.astype(int)
    last_hist_year = all_financials.index.year.max()
    forecast_years = last_hist_year + forecast_table.index
    forecast_table.index = forecast_years
    revenue_forecast = forecast_table['Total Revenue'].round(2).tolist()
    ebit_forecast = forecast_table['EBIT'].round(2).tolist()
    net_income_forecast = forecast_table['Net Income'].round(2).tolist()
    fcf_forecast = forecast_table['Free Cash Flow'].round(2).tolist()
    #Create the chart
    fig = go.Figure()
    fig.update_layout(
    yaxis=dict(
        title='EBIT / Net Income / FCF'
    ),
    yaxis2=dict(
        title='Revenue',
        overlaying='y',
        side='right'
    ),
    barmode='group'  # optional: makes bars group instead of stacking
    )
    fig.add_trace(go.Bar(x=historical_years, y=revenue_hist,yaxis='y2', name='Revenue (Historical)', marker_color='darkblue', offsetgroup=1, text=revenue_hist, textposition='auto'))
    fig.add_trace(go.Bar(x=forecast_years, y=revenue_forecast,yaxis='y2', name='Revenue (Forecast)', marker_color='blue', offsetgroup=1, text=revenue_forecast, textposition='auto'))
    # EBIT
    fig.add_trace(go.Bar(x=historical_years, y=ebit_hist, name='EBIT (Historical)', marker_color='darkorange', opacity=1.0, offsetgroup=2, text=ebit_hist, textposition='auto'))
    fig.add_trace(go.Bar(x=forecast_years, y=ebit_forecast, name='EBIT (Forecast)', marker_color='orange', opacity=1.0, offsetgroup=2, text=ebit_forecast, textposition='auto'))
    # Net Income
    fig.add_trace(go.Bar(x=historical_years, y=net_income_hist, name='Net Income (Historical)', marker_color='darkgreen', offsetgroup=3, text=net_income_hist, textposition='auto'))
    fig.add_trace(go.Bar(x=forecast_years, y=net_income_forecast, name='Net Income (Forecast)', marker_color='green', offsetgroup=3, text=net_income_forecast, textposition='auto'))
    # Free Cash Flow
    fig.add_trace(go.Bar(x=historical_years, y=fcf_hist, name='Free Cash Flow (Historical)', marker_color='maroon', offsetgroup=4, text=fcf_hist, textposition='auto'))
    fig.add_trace(go.Bar(x=forecast_years, y=fcf_forecast, name='Free Cash Flow (Forecast)', marker_color='indianred', offsetgroup=4, text=fcf_forecast, textposition='auto'))
    return fig
#Display the chart
create_financials_forecast_chart(all_financials, forecast_table, ticker).show()
#Save the chart as HTML
create_financials_forecast_chart(all_financials, forecast_table, ticker).write_html(f"reports/{ticker}_Financials_Forecast_chart.html")
print(f"Financials forecast chart saved to: reports/{ticker}_Financials_Forecast_chart.html")