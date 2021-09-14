from backtrader.indicators import crossover
import numpy
import backtrader

class macdRsi(backtrader.Strategy):
    def __init__(self):
        print('Initializing indicators')
        self.macd = backtrader.indicators.MACD(self.data)
        self.macd_crossover = backtrader.indicators.CrossOver(self.macd.macd, self.macd.signal)

        self.setsizer(backtrader.sizers.AllInSizer(percents=90))

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = backtrader.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    # def notify_order(self, order):
    #     if order.status in [order.Submitted]:
    #         # Buy/Sell order submitted/accepted to/by broker - Nothing to do
    #         self.log('ORDER SUBMITTED', dt=order.created.dt)
    #         self.order = order
    #         return

    #     if order.status in [order.Accepted]:
    #         # Buy/Sell order submitted/accepted to/by broker - Nothing to do
    #         self.log('ORDER ACCEPTED', dt=order.created.dt)
    #         self.order = order
    #         return

    #     if order.status in [order.Expired]:
    #         self.log('BUY EXPIRED')

    #     elif order.status in [order.Completed]:
    #         if order.isbuy():
    #             self.log(
    #                 'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
    #                 (order.executed.price,
    #                  order.executed.value,
    #                  order.executed.comm))

    #         else:  # Sell
    #             self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
    #                      (order.executed.price,
    #                       order.executed.price * order.executed.size *-1,
    #                       order.executed.comm))
                

    #     elif order.status in [order.Canceled]:
    #         self.log('Order Canceled')
    #     elif order.status in [order.Rejected]:
    #         self.log('Order rejected')
    #     elif order.status in [order.Margin]:
    #         self.log(f'Margin call @{order.executed.price*order.size}, portfolio balance: {self.broker.getcash()}')

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        if self.macd_crossover > 0:
            # if self.macd.macd > 0 and self.position:
            buy_order = self.close()  # enter long
        elif self.macd_crossover < 0:
            # if self.macd.macd < 0 and not self.position:
            sell_order = self.buy()  # close long position