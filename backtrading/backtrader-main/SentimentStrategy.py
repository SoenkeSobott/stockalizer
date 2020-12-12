import backtrader as bt


class SentimentStrategy(bt.Strategy):
    params = (('period', 10), ('lowBound', 0.1), ('highBound', 0.9))

    def __init__(self):
        self.news_sentiment = self.datas[1].close
        # self.tweet_sentiment = self.datas[2].close
        self.date = self.data.datetime
        self.stock_price = self.datas[0].close
        self.order = None

    def next(self):

        # Check for open orders
        if self.order:
            return

        if self.news_sentiment > self.params.highBound and not self.position:
            self.log(f'Sentiment Value: {self.news_sentiment[0]:.2f}')
            # We are not in the market, we will open a trade
            self.log(f'***BUY CREATE {self.stock_price[0]:.2f}')
            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy()
        elif self.news_sentiment < self.params.lowBound and not self.position:
            self.log(f'Sentiment Value: {self.news_sentiment[0]:.2f}')
            # We are not in the market, we will open a trade
            self.log(f'***SELL CREATE {self.stock_price[0]:.2f}')
            # Keep track of the created order to avoid a 2nd order
            self.order = self.sell()
        else:
            if self.position:
                # We are in the market, we will close the existing trade
                self.log(f'Sentiment Value: {self.news_sentiment[0]:.2f}')
                self.log(f'CLOSE CREATE {self.stock_price[0]:.2f}')
                self.order = self.close()

    def notify_order(self, order):  # helper class for logging
        if order.status in [order.Submitted, order.Accepted]:
            # Existing order - Nothing to do
            return
            # Check if an order has been completed
            # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin,
                              order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None

    def log(self, txt, dt=None):  # Helper log function
        dt = dt or self.datas[0].datetime.date(0)
        #  print(f'{dt.isoformat()} {txt}')

    def notify_trade(self, trade):  # Helper log function
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def stop(self):  # Helper log function
        self.log('(MA Period %2d) Ending Value %.2f Difference: %.3f' %
                 (self.params.period, self.broker.getvalue(), self.broker.getvalue() - 100000))