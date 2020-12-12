import backtrader as bt
import pytz
from datetime import datetime

"""
import alpaca_backtrader_api
from alpaca_keys import alpaca_paper
"""

from SentimentStrategy import SentimentStrategy

"""
ALPACA_KEY_ID = alpaca_paper['api_key']
ALPACA_SECRET_KEY = alpaca_paper['api_secret']
ALPACA_PAPER = True

tickers = ['AMZN']
timeframes = {
    '15Min':15,
    '30Min':30,
    '1H':60,
}

store = Alpaca.AlpacaStore(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER
)

DataFactory = store.getdata

for timeframe, minutes in timeframes.items():
        print(f'Adding ticker {ticker} using {timeframe} timeframe at {minutes} minutes.')

        d = DataFactory(
            dataname=ticker,
            timeframe=bt.TimeFrame.Minutes,
            compression=minutes,
            fromdate=fromdate,
            todate=todate,
            historical=True)

        cerebro.adddata(d) # Add this data instead of Yahoo data
"""

cerebro = bt.Cerebro(optreturn=False)
cerebro.broker.setcash(100000)


class TweetSentimentData(bt.feeds.GenericCSVData):
    lines = (tuple('sentiment'))
    params = (
        ('dtformat', '%Y-%m-%d'),
        ('date', 0),
        ('sentiment', 1),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
    )


if __name__ == '__main__':
    news_sentiment_data = "datasets/news-sentiment.csv"
    tweet_sentiment_data = "datasets/tweet_sentiment.csv"

    price_data = bt.feeds.YahooFinanceData(dataname='AMZN', fromdate=datetime(2017, 12, 1),
                                           todate=datetime(2020, 12, 1))
    cerebro.adddata(price_data)
    cerebro.adddata(bt.feeds.GenericCSVData(
        dataname=news_sentiment_data,
        fromdate=datetime(2017, 12, 1),
        todate=datetime(2020, 12, 1),
        nullvalue=0.0,
        dtformat=('%d/%m/%Y %H:%M'),
        datetime=0,
        time=-1,
        high=-1,
        low=-1,
        open=-1,
        close=1,
        volume=-1,
        openinterest=-1,
        timeframe=bt.TimeFrame.Days))
    # cerebro.adddata(TweetSentimentData(dataname=tweet_senitment_data)
    """ For running single Test
    cerebro.addstrategy(SentimentStrategy)
    cerebro.run()
    """

    # Add strategy to Cerebro
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
    cerebro.optstrategy(SentimentStrategy, lowBound=[x * 0.1 for x in range(0, 5)],
                        highBound=[x * 0.1 for x in range(5, 10)])

    # Default position size
    cerebro.addsizer(bt.sizers.SizerFix, stake=3)

    optimized_runs = cerebro.run(stdstats=False)

    final_results_list = []
    for run in optimized_runs:
        for strategy in run:
            PnL = round(strategy.broker.getvalue() - 100000, 2)
            sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
            final_results_list.append([strategy.params.lowBound,
                                       strategy.params.highBound, PnL, sharpe['sharperatio']])

    sort_by_sharpe = sorted(final_results_list, key=lambda x: x[3],
                            reverse=True)
    for line in sort_by_sharpe[:5]:
        print(line)
