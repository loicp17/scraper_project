import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime

app = dash.Dash(__name__)
app.title = "USD/CHF Live Dashboard"

def get_latest_price():
    try:
        with open('price.txt', 'r') as f:
            lines = f.readlines()
            if lines:
                parts = lines[-1].strip().split(" - USD/CHF Price: ")
                if len(parts) == 2:
                    return parts
    except FileNotFoundError:
        pass
    return None, None

def get_price_history():
    try:
        with open('price.txt', 'r') as f:
            lines = f.readlines()
            timestamps, prices = [], []
            for line in lines:
                parts = line.strip().split(" - USD/CHF Price: ")
                if len(parts) != 2:
                    continue
                timestamp, price_str = parts
                try:
                    price = float(price_str)
                    timestamps.append(timestamp)
                    prices.append(price)
                except ValueError:
                    continue
            return pd.DataFrame({'Timestamp': pd.to_datetime(timestamps), 'Price': prices})
    except FileNotFoundError:
        return pd.DataFrame(columns=['Timestamp', 'Price'])

def calculate_daily_report():
    df = get_price_history()
    if df.empty:
        return None

    df['Date'] = df['Timestamp'].dt.date
    today = datetime.datetime.now().date()
    today_df = df[df['Date'] == today]

    if today_df.shape[0] < 2:
        return None

    open_price = today_df.iloc[0]['Price']
    close_price = today_df.iloc[-1]['Price']
    volatility = np.std(today_df['Price'])
    change = close_price - open_price
    evolution = (change / open_price) * 100

    return {
        'date': today,
        'open': open_price,
        'close': close_price,
        'volatility': volatility,
        'change': change,
        'evolution': evolution
    }

def calculate_weekly_report():
    df = get_price_history()
    if df.empty:
        return None

    df['Date'] = df['Timestamp'].dt.date
    today = datetime.datetime.now().date()
    week_ago = today - datetime.timedelta(days=7)
    week_df = df[(df['Date'] > week_ago) & (df['Date'] <= today)]

    if week_df.shape[0] < 2:
        return None

    open_price = week_df.iloc[0]['Price']
    close_price = week_df.iloc[-1]['Price']
    volatility = np.std(week_df['Price'])
    change = close_price - open_price
    evolution = (change / open_price) * 100

    return {
        'open': open_price,
        'close': close_price,
        'volatility': volatility,
        'change': change,
        'evolution': evolution
    }

app.layout = html.Div(style={'backgroundColor': '#0e1a2b', 'color': '#ffffff', 'padding': '20px'}, children=[

    html.H1("USD/CHF - Live Scraping", style={'textAlign': 'left', 'fontSize': '40px'}),

    html.Div([
        html.Div([
            html.Div("Last Price", style={'fontSize': '20px'}),
            html.Div(id="latest-price", style={'fontSize': '40px', 'fontWeight': 'bold'})
        ], style={'backgroundColor': '#2c3e50', 'padding': '20px', 'borderRadius': '10px', 'width': '30%'}),

        html.Div([
            html.Div("Change (Last 7 Days)", style={'fontSize': '20px'}),
            html.Div(id="change", style={'fontSize': '40px', 'fontWeight': 'bold'})
        ], style={'backgroundColor': '#2c3e50', 'padding': '20px', 'borderRadius': '10px', 'width': '30%'}),

        html.Div([
            html.Div("Volatility (Last 7 Days)", style={'fontSize': '20px'}),
            html.Div(id="volatility", style={'fontSize': '40px', 'fontWeight': 'bold', 'color': '#ff6f61'})
        ], style={'backgroundColor': '#1e1e1e', 'padding': '20px', 'borderRadius': '10px', 'width': '30%'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '30px'}),

    html.Div([
        html.H3("Live Price", style={'marginBottom': '10px'}),
        dcc.Graph(id='price-graph')
    ]),

    html.Div([
        html.H2("Daily report", style={'marginTop': '40px'}),
        html.Pre(id='daily-report', style={'fontSize': '20px'})
    ]),

    dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0)  # refresh every 5 minutes
])

@app.callback(
    [Output("latest-price", "children"),
     Output("change", "children"),
     Output("volatility", "children"),
     Output("price-graph", "figure"),
     Output("daily-report", "children")],
    Input("interval-component", "n_intervals")
)
def update_dashboard(n):
    timestamp, latest_price_str = get_latest_price()
    df = get_price_history()

    if not df.empty:
        df_sorted = df.sort_values('Timestamp')
        figure = {
            'data': [
                go.Scatter(
                    x=df_sorted['Timestamp'],
                    y=df_sorted['Price'],
                    mode='lines+markers',
                    name='USD/CHF',
                    line=dict(color='#00ffc8')  # Aqua green line
                )
            ],
            'layout': go.Layout(
                paper_bgcolor='#0e1a2b',
                plot_bgcolor='#0e1a2b',
                font=dict(color='#ffffff'),
                xaxis=dict(title='Time'),
                yaxis=dict(title='Price (USD/CHF)'),
                margin=dict(l=40, r=20, t=30, b=40)
            )
        }
    else:
        figure = {}

    report = calculate_daily_report()
    weekly_report = calculate_weekly_report()

    if weekly_report:
        change_display = f"{weekly_report['change']:+.4f}"
        vol_display = f"{weekly_report['volatility']:.4f}"
    else:
        change_display = "N/A"
        vol_display = "N/A"

    if report:
        report_text = (
            f"Report of {report['date']} :\n"
            f"- Open : {report['open']:.4f}\n"
            f"- Close : {report['close']:.4f}\n"
            f"- Volatility : {report['volatility']:.4f}\n"
            f"- Evolution : {report['evolution']:.2f}%"
        )
    else:
        report_text = "No daily report available."

    if timestamp and latest_price_str:
        latest_display = f"{latest_price_str} at {timestamp}"
    else:
        latest_display = "No latest price available."

    return latest_display, change_display, vol_display, figure, report_text


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
