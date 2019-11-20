import pandas as pd
import requests
import json
from pyti.smoothed_moving_average import smoothed_moving_average as sma
import plotly.graph_objs as go
from plotly.offline import plot

class TradingBot:
    def __init__(self, symbol):
        self.symbol = symbol
        self.df = self.getData()

    def getData(self):

        base = 'https://api.binance.com'
        endpoint = '/api/v1/klines'
        params = '?&symbol='+self.symbol+'&interval=1d'

        url = base + endpoint + params

        #JSON LOADS AND DOWNLOAD DATA
        data = requests.get(url)
        dictionary = json.loads(data.text)

        #PUT IN DATAFRAME AND CLEAN UP
        df = pd.DataFrame.from_dict(dictionary)
        df = df.drop(range(6, 12), axis=1)

        #NAMING COLUMNS
        typeOfcol = ['time', 'open', 'high', 'low', 'close', 'volume']
        df.columns = typeOfcol

        for col in typeOfcol:
            df[col] =df[col].astype(float)


        valueONE = 10
        valueTWO = 21
        valueTHREE = 50
        valueFOUR = 200

        #ADDING SMA'S
        df['first_sma'] = sma(df['close'].tolist(), valueONE)
        df['second_sma'] = sma(df['close'].tolist(), valueTWO)
        df['third_sma'] = sma(df['close'].tolist(), valueTHREE)
        df['fourth_sma'] = sma(df['close'].tolist(), valueFOUR)

        return df

#buy_signals = false
    def plotData(self):
        df = self.df

        #CANDLESTICKS CHART
        candle = go.Candlestick(
        x = df['time'],
        open = df['open'],
        close = df['close'],
        high = df['high'],
        low = df['low'],
        name = "Candlesticks")

		# plot MAs
        first_sma = go.Scatter(
        x = df['time'],
        y = df['first_sma'],
        name = "10 SMA",
        line = dict(color = ('rgba(102, 207, 255, 50)')))

        sec_sma = go.Scatter(
        x = df['time'],
        y = df['second_sma'],
        name = "21 SMA",
        line = dict(color = ('rgba(255, 207, 102, 50)')))

        third_sma = go.Scatter(
        x = df['time'],
        y = df['third_sma'],
        name = "50 SMA",
        line = dict(color = ('rgba(110, 220, 255, 50)')))

        fourth_sma = go.Scatter(
        x = df['time'],
        y = df['fourth_sma'],
        name = "200 SMA",
        line = dict(color = ('rgba(255, 0, 0, 50)')))

        #GRAB DATA AND PRINT
        data = [candle, first_sma, sec_sma, third_sma, fourth_sma]

        # LAYOUT OF THE GRAPH
        layout = go.Layout(title = self.symbol)
        fig = go.Figure(data = data, layout = layout)
        plot(fig, filename=self.symbol)

def Run():
    symbol = "ADABTC"
    TradingChart = TradingBot(symbol)
    TradingChart.plotData()
    #tradeChart.strategy()

if __name__ == '__main__':
    Run()
