import backtrader as bt
import alpaca_backtrader_api
from ssh.keys import API_KEY, API_SECRET_KEY
from datetime import datetime

import backtrader as bt
import backtrader.strategies as btstrats
ticker = 'NFLX'
from_date = datetime(2019, 12, 1)
to_date = datetime(2020, 12, 1)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)

    store = alpaca_backtrader_api.AlpacaStore(
        key_id=API_KEY,
        secret_key=API_SECRET_KEY,
        paper=True
    )
    DataFactory = store.getdata
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.0)
    cerebro.broker.set_coc(True)
    # Add Data
    data_timeframe = bt.TimeFrame.Minutes
    data_compression = 60
    data0 = DataFactory(
        dataname=ticker,
        timeframe=data_timeframe,
        compression=data_compression,
        fromdate=from_date,
        todate=to_date,
        historical=True)
    cerebro.adddata(data0)

    # strategy
    cerebro.addstrategy(btstrats.SMA_CrossOver)
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(subplot=True, plotabove=True)
