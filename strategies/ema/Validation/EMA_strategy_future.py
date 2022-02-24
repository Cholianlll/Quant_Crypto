# Backtrader tut
#! Author: Cholian Li
# Contact: 
#! cholianli970518@gmail.com
# Created at 20211228

'''
############################## Possible BUG ##########################################
#! Bug: the matplotlib has crash to the backtrader
#? method 1: 
# degrade the matplotlib to 3.2.2:
# pip install matplotlib==3.2.2

#? method 2 (could not install matplotlib==3.2.2 with python 3.9):
# pip uninstall backtrader
# pip install git+https://github.com/mementum/backtrader.git@0fa63ef4a35dc53cc7320813f8b15480c8f85517#egg=backtrader

# refer: https://stackoverflow.com/questions/63471764/importerror-cannot-import-name-warnings-from-matplotlib-dates
########################################################################
'''


############################ body ####################################


import backtrader as bt
import pandas as pd
import talib as ta

# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('line_a', None),
        ('line_b',None),
    )

    def log(self, txt, dt=None):
        
        pass
    
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt, txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        
        # To keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        # Add a EMA indicator
        self.ema_a = bt.talib.EMA(self.dataclose, timeperiod=self.params.line_a,plotname = 'ema_a',)
        self.ema_b = bt.talib.EMA(self.dataclose, timeperiod=self.params.line_b,plotname = 'ema_b',)
        
        
    def notify_order(self, order):
        
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                
            elif order.issell() : # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            elif order.isclose():
                self.log('Order closed EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None
        
   
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))     

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        self.log(f'EMA_a: {self.ema_a[0]},EMA_b: {self.ema_b[0]},')
        
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        
        # If the Fast line cross over the slow line
        if self.ema_a[0] > self.ema_b[0]:
            
            # If there is already an order in a position
            if self.position:
                
                # If is has an short order, we should transfer the short position to the long position
                if self.position.size < 0:
                    # close the previous position, e.g: long
                    self.buy()
                    # buyin a new long position
                    self.buy()
                    self.log('Short --> Long  CREATE, %.2f' % self.dataclose[0])
                    
            # if there is no order in a position, we should order the position 
            # according to the current EMA singal, here we assumed the long position
            else:
                self.buy()
                self.log('Long CREATE, %.2f' % self.dataclose[0])
             
        #    Opposite to above
        elif self.ema_a[0] < self.ema_b[0]:
            
            if self.position:
                if self.position.size > 0:
                    self.sell()
                    self.sell()
                    self.log('Long --> Short  CREATE, %.2f' % self.dataclose[0])
                    
            else:
                self.sell()
                self.log('Short CREATE, %.2f' % self.dataclose[0])
                
                
def runstart(line_a,line_b,datapath):
    
    cerebro = bt.Cerebro()

    # self-define the observers
    # cerebro = bt.Cerebro(stdstats=False)
    
    # TODO // Add observers
    # cerebro.addobserver(bt.observers.Broker)
    
    Myown_result = []
    
    # TODO // Add a Data
    # train_data
    # datapath = ('data/BTC_6h_test.csv')
    
    # test_data
    # datapath = ('data/BTC_1hr_test.csv')
    dataframe = pd.read_csv(datapath,
                                # nrows=1000,
                                # skiprows = range(1,1500),
                                parse_dates=True,
                                index_col=0)
    
    # print('--------------------------------------------------')
    # print(dataframe.head(5))
    # print(dataframe.info())
    # print('--------------------------------------------------')
    
    # Pass it to the backtrader datafeed and add it to the cerebro
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)
    
    # TODO // Add a strategy
    cerebro.addstrategy(TestStrategy,line_a = line_a,line_b=line_b)
    
    # TODO // Analyzer
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
    # cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
    # cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
    # cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name='TimeDrawDown')
    # cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='TimeReturn')
    
    
    # cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    
    # TODO // Cash
    cerebro.broker.setcash(1000.0)

    # TODO // Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=.02)
    
    # TODO // Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.0004)

    # TODO // Run over everything
    # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    Myown_result.append(cerebro.broker.getvalue())
    results = cerebro.run()
    # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    Myown_result.append(cerebro.broker.getvalue())
    
    Myown_result.append(Myown_result[1]/Myown_result[0]-1)

    # TODO // Plot the result
    cerebro.plot()
    
    # TODO // result
    strat = results[0]
    
    # SharpeRatio = strat.analyzers.SharpeRatio.get_analysis()
    # print('Sharpe Ratio:', SharpeRatio)
    # or
    # SharpeRatio = strat.analyzers.getbyname('SharpeRatio')
    # print('Sharpe Ratio:', SharpeRatio.get_analysis()['SharpeRatio'])
    # print('Sharpe Ratio:', SharpeRatio.get_analysis())
    
    SharpeRatio = strat.analyzers.getbyname('SharpeRatio')
    Myown_result.append(SharpeRatio.get_analysis()['sharperatio'])
    
    # AnnualReturn = strat.analyzers.getbyname('AnnualReturn')
    # Myown_result.append(AnnualReturn.get_analysis())
    
    # DrawDown = strat.analyzers.getbyname('DrawDown')
    # print(DrawDown.get_analysis())
    # Myown_result.append(DrawDown.get_analysis())
    
    # TimeDrawDown = strat.analyzers.getbyname('TimeDrawDown')
    # print(TimeDrawDown.get_analysis())
    
    # TimeReturn = strat.analyzers.getbyname('TimeReturn')
    # print(TimeReturn.get_analysis())
    
    ################################################################################################
    ############################# pyfolio module api for performance ###############################
    ################################################################################################
    '''
    # ref
    # http://quantopian.github.io/pyfolio/notebooks/single_stock_example/
    # https://www.backtrader.com/docu/analyzers/pyfolio-integration/pyfolio-integration/
    '''
    # pyfoliozer = strat.analyzers.getbyname('pyfolio')
    # returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    
    # import pyfolio as pf
    # pf.create_full_tear_sheet(
    #     returns,
    #     positions=positions,
    #     transactions=transactions,
    #     gross_lev=gross_lev,
    #     live_start_date='2018-05-01',  # This date is sample specific
    #     round_trips=True)
    ###################################################################################################
    
    Myown_result.append(line_a)
    Myown_result.append(line_b)
    
    print(Myown_result)
    
    return Myown_result

def validation_runstart(datapath):
    
    column_names = [
        "starting cash", 
        "ending cash", 
        "return",
        'sharp ratio',
        # 'annual return'
        'line_a',
        'line_b'
        ]
    
    # result_table = pd.DataFrame(columns=column_names)
    result_table = []
    
    for i in range(10,100):
        for j in range(i,100):
            if i != j:
                res = runstart(i,j,datapath)
                result_table.append(res)
                print(i,j,'finished')
    
    result_table = pd.DataFrame(result_table,columns = column_names)
    result_table.to_csv('Validation_future_6h_train.csv',encoding='utf-8')
    

if __name__ == '__main__':

    datapath = ('data/BTC_6h_test.csv')
    # validation_runstart(datapath)
    runstart(36,60,datapath)
            