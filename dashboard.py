import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import datetime
import numpy as np

app = dash.Dash(__name__)
app.title = "USD/CHF Live Dashboard"

def get_latest_price():
    try:
        with open('price.txt', 'r') as f:
            lines = f.readlines()
            if lines:
                return lines[-1].strip().split(" - USD/CHF Price: ")
    except FileNotFoundError:
        return None, None
    return None, None

def get_price_history():
    try:
        with open('price.txt', 'r') as f:
            lines = f.readlines()
            timestamps, prices = [], []
            for line in lines:
                timestamp, price = line.strip().split(" - USD/CHF Price: ")
                timestamps.append(timestamp)
                prices.append(float(price))
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

    if today_df.empty:
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

app.layout = html.Div(style={'backgroundColor': '#0e1a2b', 'color': '#ffffff', 'padding': '20px'}, children=[

    html.H1("USD/CHF - Live Scraping", style={'textAlign': 'left', 'fontSize': '40px'}),

    html.Div([
        html.Div([
            html.Div("Last Price", style={'fontSize': '20px'}),
            html.Div(id="latest-price", style={'fontSize': '40px', 'fontWeight': 'bold'})
        ], style={'backgroundColor': '#2c3e50', 'padding': '20px', 'borderRadius': '10px', 'width': '30%'}),

        html.Div([
            html.Div("Change", style={'fontSize': '20px'}),
            html.Div(id="change", style={'fontSize': '40px', 'fontWeight': 'bold'})
        ], style={'backgroundColor': '#2c3e50', 'padding': '20px', 'borderRadius': '10px', 'width': '30%'}),

        html.Div([
            html.Div("Volatility", style={'fontSize': '20px'}),
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

    dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0)
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
    if report:
        change_display = f"{report['change']:+.4f}"
        vol_display = f"{report['volatility']:.2f}"
        report_text = (
            f"Report of {report['date']} :\n"
            f"- Open : {report['open']:.4f}\n"
            f"- Close : {report['close']:.4f}\n"
            f"- Volatility : {report['volatility']:.2f}\n"
            f"- Evolution : {report['evolution']:.2f}%"
        )
    else:
        change_display = "N/A"
        vol_display = "N/A"
        report_text = "No daily report available."

    return f"{latest_price_str} at {timestamp}", change_display, vol_display, figure, report_text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)

