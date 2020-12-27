import backtrader as bt
import backtrader.analyzers as btanalyzers
import pytz
import pandas as pd
from datetime import datetime
import alpaca_backtrader_api
from ssh.keys import API_KEY, API_SECRET_KEY

from SentimentStrategy import SentimentStrategy

if __name__ == '__main__':

    ticker = 'AMZN'
    is_live = False

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)

    store = alpaca_backtrader_api.AlpacaStore(
        key_id=API_KEY,
        secret_key=API_SECRET_KEY,
        paper=True
    )
    if is_live:
        broker = store.getbroker()  # or just alpaca_backtrader_api.AlpacaBroker()
        cerebro.setbroker(broker)
    else:
        cerebro.broker.setcash(100000)
        cerebro.broker.setcommission(commission=0.0)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=20)

    DataFactory = store.getdata

    if is_live:
        data0 = DataFactory(
            dataname=ticker,
            timeframe=bt.TimeFrame.Days,
        )
    else:
        data0 = DataFactory(
            dataname=ticker,
            timeframe=bt.TimeFrame.Days,
            fromdate=pd.Timestamp('2017-12-1'),
            todate=pd.Timestamp('2020-12-1'),
            historical=True)
    cerebro.adddata(data0)

    news_sentiment_data = "../../data/files/news_with_scores.csv"
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
    """
    tweet_sentiment_data = "../../data/files/twitter-news_with_scores.csv"
    cerebro.adddata(bt.feeds.GenericCSVData(
        dataname=tweet_sentiment_data,
        fromdate=datetime(2017, 12, 1),
        todate=datetime(2020, 12, 1),
        nullvalue=0.0,
        dtformat=('%Y-%m-%d %H:%M:%S'),
        datetime=0,
        time=-1,
        high=-1,
        low=-1,
        open=-1,
        close=1,
        volume=-1,
        openinterest=-1,
        timeframe=bt.TimeFrame.Days))
    """

    """ For running single Test """
    cerebro.addstrategy(SentimentStrategy)
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
    """

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
    par_df = pd.DataFrame(par_list, columns=['low_bound', 'high_bound', 'return', 'dd', 'sharpe'])
    par_df.sort_values(by=['sharpe'], inplace=True, ascending=False)
    print(par_df)
    """