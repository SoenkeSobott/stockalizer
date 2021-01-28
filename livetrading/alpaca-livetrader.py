import backtrader as bt
import backtrader.analyzers as btanalyzers
import pytz
import pandas as pd
from datetime import datetime
import alpaca_backtrader_api


ticker = 'NFLX'
is_paper = True
is_backtesting = False

#to start multiple backtesting runs which try to optimize the strategy parameters
param_optimization = False

from_date = datetime(2019, 12, 1)
to_date = datetime(2020, 12, 1)

#LIVE TRADING URLS
news_live_data_url = '{"sentiment_score":{"15/01/2021 14:00":"0.9"}}'
tweet_live_data_url = '{"sentiment_score":{"15/01/2021 14:00":"0.9"}}'

class SentimentStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2), ('low_bound', 0.5), ('high_bound', 0.5), ('tweet_leverage', 5),
              ('news_leverage', 5))

    def __init__(self):
        self.live_bars = False
        self.date = self.data.datetime
        self.order = None
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        print(f'Params: low_bound: {self.params.low_bound}, high_bound: {self.params.high_bound}, '
              f'tweet: {self.params.tweet_leverage}, news: {self.params.news_leverage}')

    def notify_data(self, data, status, *args, **kwargs):
        super().notify_data(data, status, *args, **kwargs)
        print('*' * 5, 'LIVE DATA STATUS:', data._getstatusname(status), *args)
        if data._getstatusname(status) == "LIVE":
            self.live_bars = True

    def next(self):
        if not self.live_bars and not is_backtesting:
            # skip if no live data yet available and we are not backtesting
            return
        """
        if datetime.time(self.datas[0].datetime) < datetime.time(9, 45) or datetime.time(self.datas[0].datetime) > datetime.time(16, 0):
            # don't operate until the market has been running 15 minutes or is closed again
            return  #
        """
        # Check for open orders
        if self.order:
            return
        news_sentiment = self.datas[1].sentiment_score
        tweet_sentiment = self.datas[2].sentiment_score
        # tweet_sentiment = -1
        self.stock_price = self.datas[0].close
        if news_sentiment == -1 and tweet_sentiment == -1:
            return
        elif news_sentiment == -1:
            self.sentiment = tweet_sentiment[0]
        elif tweet_sentiment == -1:
            self.sentiment = news_sentiment[0]
        else:
            self.sentiment = (news_sentiment[0] * self.params.news_leverage + tweet_sentiment[
                0] * self.params.tweet_leverage) / (self.params.news_leverage + self.params.tweet_leverage)
        if self.position:
            if (self.trade_type == 'buy' and self.sentiment < (self.params.low_bound)):
                # We are in the market, we will close the existing trade
                self.log(f'Sentiment Value: {self.sentiment:.2f}')
                self.log(f'CLOSE BUY {self.stock_price[0]:.2f}')
                self.order = self.close()
            if (self.trade_type == 'sell' and self.sentiment > (self.params.high_bound)):
                # We are in the market, we will close the existing trade
                self.log(f'Sentiment Value: {self.sentiment:.2f}')
                self.log(f'CLOSE SELL {self.stock_price[0]:.2f}')
                self.order = self.close()
        if self.sentiment > self.params.high_bound and not self.position:
            if abs(self.stock_price - self.boll.lines.top) > abs(self.stock_price - self.boll.lines.mid):
                self.log(f'High Sentiment Value: {self.sentiment:.2f}')
                # We are not in the market, we will open a trade
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        elif self.sentiment < self.params.low_bound and not self.position:
            if abs(self.stock_price - self.boll.lines.bot) > abs(self.stock_price - self.boll.lines.mid):
                self.log(f'Low Sentiment Value: {self.sentiment:.2f}')
                # We are not in the market, we will open a trade
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

    def notify_order(self, order):  # helper class for logging
        if order.status in [order.Submitted, order.Accepted]:
            # Existing order - Nothing to do
            return
            # Check if an order has been completed
            # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.trade_type = 'buy'
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.trade_type = 'sell'
                self.oreder_created = self.datas[0].datetime.datetime(0)
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin,
                              order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None

    def log(self, txt, dt=None):  # Helper log function
        dt = dt or self.datas[0].datetime.datetime(0)
        print(f'{dt.isoformat()} {txt}')

    def notify_trade(self, trade):  # Helper log function
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def stop(self):
        print('==================================================')
        print('Starting Value: %.2f' % self.broker.startingcash)
        print('Ending   Value: %.2f' % self.broker.getvalue())
        print('Profit/Loss: %.2f' % (self.broker.getvalue() - self.broker.startingcash))
        print('==================================================')


# Helper Class for adding a CSV with sentiment scores
class SentimentCSV(bt.feeds.GenericCSVData):
    # Add a 'pe' line to the inherited ones from the base class
    lines = ('sentiment_score',)

    # openinterest in GenericCSVData has index 7 ... add 1
    # add the parameter to the parameters inherited from the base class
    params = (('sentiment_score', 8),)


class PandasData(bt.feeds.PandasData):
    lines = ('sentiment_score',)

    params = (
        ('sentiment_score', 7),
    )


class SentimentSizer(bt.Sizer):
    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if position.size:
            return
        else:
            stake = self.broker.getvalue() / data.close[0]
            sentiment_score = self.strategy.sentiment
            if isbuy:
                if sentiment_score > 0.6:
                    return stake * 0.4
                elif sentiment_score > 0.75:
                    return stake * 0.6
                elif sentiment_score > 0.9:
                    return stake * 0.8
            else:
                if sentiment_score < 0.4:
                    return stake * -0.4
                elif sentiment_score < 0.25:
                    return stake * -0.6
                elif sentiment_score < 0.1:
                    return stake * -0.8


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)

    store = alpaca_backtrader_api.AlpacaStore(
        key_id=API_KEY,
        secret_key=API_SECRET_KEY,
        paper=is_paper
    )
    DataFactory = store.getdata
    data1 = None
    data2 = None
    if is_backtesting:
        print("wrong")

    else:  # live/paper trading
        broker = store.getbroker()  # or just alpaca_backtrader_api.AlpacaBroker()
        cerebro.setbroker(broker)
        cerebro.addsizer(SentimentSizer)
        data_timeframe = bt.TimeFrame.Minutes
        data_compression = 1
        data_timezone = pytz.timezone('America/Vancouver')
        # Add data
        data0 = DataFactory(
            dataname=ticker,
            timeframe=data_timeframe,
            compression=data_compression
        )

        if news_live_data_url != '':

            df_news = pd.read_json(news_live_data_url)
            print(df_news.tail())

            news_sentiment_data = "../data/files/{0}/{1}_news_with_scores.csv".format(ticker, ticker.lower())
            data1 = SentimentCSV(
                dataname=news_sentiment_data,
                nullvalue=-1,
                dtformat=('%d/%m/%Y %H:%M'),
                datetime=0,
                time=-1,
                high=-1,
                low=-1,
                open=-1,
                close=-1,
                volume=-1,
                openinterest=-1,
                sentiment_score=1)

        if tweet_live_data_url != '':
            tweet_sentiment_data = "../data/files/{0}/{1}_tweets_with_scores.csv".format(ticker, ticker.lower())
            data1 = SentimentCSV(
                dataname=tweet_sentiment_data,
                nullvalue=-1,
                dtformat=('%d/%m/%Y %H:%M'),
                datetime=0,
                time=-1,
                high=-1,
                low=-1,
                open=-1,
                close=-1,
                volume=-1,
                openinterest=-1,
                sentiment_score=1)


    cerebro.adddata(data0)
    if data1 is not None:
        cerebro.adddata(data1)
    if data2 is not None:
        cerebro.adddata(data2)

    if param_optimization == False:
        """ For running single Test"""
        cerebro.addstrategy(SentimentStrategy)
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.plot(subplot=True, plotabove=True)
    else:
        # Param optimization
        cerebro.addsizer(bt.sizers.PercentSizer, percents=10)
        cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
        cerebro.addanalyzer(btanalyzers.DrawDown, _name="drawdown")
        cerebro.addanalyzer(btanalyzers.Returns, _name="returns")
        strats = cerebro.optstrategy(SentimentStrategy, low_bound=[x * 0.1 for x in range(0, 5)],
                                     high_bound=[x * 0.1 for x in range(5, 10)])

        runs = cerebro.run(maxcpus=1)

        par_list = [[x[0].params.low_bound,
                     x[0].params.high_bound,
                     x[0].analyzers.returns.get_analysis()['rnorm100'],
                     x[0].analyzers.drawdown.get_analysis()['max']['drawdown'],
                     x[0].analyzers.sharpe.get_analysis()['sharperatio']
                     ] for x in runs]
        par_df = pd.DataFrame(par_list, columns=['low', 'high', 'return', 'dd', 'sharpe'])
        par_df.sort_values(by=['sharpe'], inplace=True, ascending=False)
        print(par_df)
