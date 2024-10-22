# Algorithm sub-class for first implementation and subsequent implementations

# Author: Navesh Kumar
# Date: 19 oct 2024
# version : 2024.10.19.01.01

from algorithm_parentclass import general_algo_framework
import pandas as pd

class momentumalgo(general_algo_framework):
    
    def DataSetup(self):
        self.SetContext("Backtest")
        self.SetDataLocation('D:/vpi/intraday_orderbook_snapshots/intraday_orderbook_snapshots')
        self.SetOutputLocation('D:/vpi')

    def TimeContext(self):
        self.SetAlgoObservationStart([2023,5,1,0,0,0]) # date
        self.SetAlgoObservationEnd([2023,5,10,23,0,0]) #date
        self.SetProductObservationStart(120) # minutes
        self.SetProductObservationEnd(0) # minutes
        # these are the intrnal product nomenclature
        self.SetProducts(
            {
                'QH':[21,22,23,24,25,26,27,28,29,30,31]
            }
                        )
        
    def AlgoMemory(self):
        # this is where we will do pattern matching for dynamic number of strats
        self.Set_algo_memory(
            {
            'calibrate_moment_t0' : None,
            'calibrate_moment_t1' : None,
            'momentum_direction_close': None,
            'open': False,
            'close':False          
            }
        )
    
    def Algorithm(self,current_product,onData,GC,current_nop):
        current_nop = current_nop
        Best_Current_Bid = float(onData.loc[
                                    (onData['timestamp'] == onData['timestamp'].max())
                                    &
                                    (onData['Level'] == 1),
                                    'Bid'
                                    ])
            
        Best_Current_Bid_Volume = float(onData.loc[
                                    (onData['timestamp'] == onData['timestamp'].max())
                                    &
                                    (onData['Level'] == 1),
                                    'BQty'
                                    ])
            
        Best_Current_Offer = float(onData.loc[
                                    (onData['timestamp'] == onData['timestamp'].max())
                                    &
                                    (onData['Level'] == 5),
                                    'Ask'
                                    ])
            
        Best_Current_Offer_Volume = float(onData.loc[
                                    (onData['timestamp'] == onData['timestamp'].max())
                                    &
                                    (onData['Level'] == 1),
                                    'AQty'
                                    ])
        if not self.algo_memory['open']:
            time_now = GC - onData['timestamp'].max()
            time_now = time_now.total_seconds() / 60
            
            if 60 < time_now <= 65:
                calibrate_moment_t0_spread = (Best_Current_Bid + Best_Current_Offer)/2
                self.algo_memory['calibrate_moment_t0'] = calibrate_moment_t0_spread
            elif 45 >= time_now > 40:
                calibrate_moment_t1_spread = (Best_Current_Bid + Best_Current_Offer)/2
                self.algo_memory['calibrate_moment_t1'] = calibrate_moment_t1_spread

            if (self.algo_memory['calibrate_moment_t0'] is not None) and (self.algo_memory['calibrate_moment_t1'] is not None):
                momentum_direction = self.algo_memory['calibrate_moment_t1'] - self.algo_memory['calibrate_moment_t0']

                if momentum_direction <= 0:
                    Trade_value = Best_Current_Bid
                    Trade_direction = "BUY"
                    append_PnL_book = {
                                    'Product':current_product, 
                                    'Trade_value':Trade_value, 
                                    'Trade_direction':Trade_direction, 
                                    'NOP':Best_Current_Bid_Volume
                    }
                    append_PnL_book = pd.DataFrame([append_PnL_book])
                    self.PnLBook = pd.concat([self.PnLBook, append_PnL_book], ignore_index=True)
                    self.algo_memory['open'] = True
                    self.algo_memory['close'] = True
                    self.algo_memory['momentum_direction_close'] = 'SELL'
                else:
                    Trade_value = Best_Current_Offer
                    Trade_direction = "SELL"
                    append_PnL_book = {
                                    'Product':current_product, 
                                    'Trade_value':Trade_value, 
                                    'Trade_direction':Trade_direction, 
                                    'NOP':Best_Current_Offer_Volume
                    }
                    append_PnL_book = pd.DataFrame([append_PnL_book])
                    self.PnLBook = pd.concat([self.PnLBook, append_PnL_book], ignore_index=True)
                    self.algo_memory['open'] = True
                    self.algo_memory['close'] = True
                    self.algo_memory['momentum_direction_close'] = 'BUY'

        if self.algo_memory['close']:
            time_now = GC - onData['timestamp'].max()
            time_now = time_now.total_seconds() / 60
            if 30 < time_now <= 35:
                if self.algo_memory['momentum_direction_close'] == 'BUY':
                    Trade_value = Best_Current_Bid
                    Trade_direction = "BUY"
                    append_PnL_book = {
                                        'Product':current_product, 
                                        'Trade_value':Trade_value, 
                                        'Trade_direction':Trade_direction, 
                                        'NOP':Best_Current_Bid_Volume
                        }
                    append_PnL_book = pd.DataFrame([append_PnL_book])
                    self.PnLBook = pd.concat([self.PnLBook, append_PnL_book], ignore_index=True)
                    self.algo_memory['close'] = False
                else:
                    Trade_value = Best_Current_Offer
                    Trade_direction = "SELL"
                    append_PnL_book = {
                                        'Product':current_product, 
                                        'Trade_value':Trade_value, 
                                        'Trade_direction':Trade_direction, 
                                        'NOP':Best_Current_Offer_Volume
                        }
                    append_PnL_book = pd.DataFrame([append_PnL_book])
                    self.PnLBook = pd.concat([self.PnLBook, append_PnL_book], ignore_index=True)
                    self.algo_memory['close'] = False