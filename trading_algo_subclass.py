# Algorithm sub-class for first implementation and subsequent implementations

# Author: Navesh Kumar
# Date: 19 oct 2024
# version : 2024.10.19.01.01

from algorithm_parentclass import general_algo_framework
import pandas as pd

class momentumalgo(general_algo_framework):
    
    def DataSetup(self):
        self.SetContext("Backtest")
        self.SetDataLocation('D:/vpi/output_parquet')

    def TimeContext(self):
        self.SetAlgoObservationStart([2024,10,20,6,0,0]) # date
        self.SetAlgoObservationEnd([2024,10,20,8,0,0]) #date
        self.SetProductObservationStart(40) # minutes
        self.SetProductObservationEnd(20) # minutes
        # these are the intrnal product nomenclature
        self.SetProducts(
            {
                'HH':[1,2,3,4,5,6,7,8,9,10,11,12,
                    13,14,15,16,17,18,19,20,21,22,23,24,
                    25,26,27,28,29,30,31,32,33,34,35,36,
                    37,38,39,40,41,42,43,44,45,46,47,48]
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
        
        if not self.algo_memory['open']:
            time_now = GC - onData['timestamp'].max()
            time_now = time_now.total_seconds() / 60
            if 36 < time_now <= 40:
                calibrate_moment_t0_spread = (onData['bid'].max() + onData['offer'].min())/2
                self.algo_memory['calibrate_moment_t0'] = calibrate_moment_t0_spread
            elif 35 >= time_now > 31:
                calibrate_moment_t1_spread = (onData['bid'].max() + onData['offer'].min())/2
                self.algo_memory['calibrate_moment_t1'] = calibrate_moment_t1_spread

            if (self.algo_memory['calibrate_moment_t0'] is not None) and (self.algo_memory['calibrate_moment_t1'] is not None):
                momentum_direction = self.algo_memory['calibrate_moment_t1'] - self.algo_memory['calibrate_moment_t0']

                if momentum_direction <= 0:
                    Trade_value = onData['bid'].max()
                    Trade_direction = "BUY"
                    append_PnL_book = {
                                    'Product':current_product, 
                                    'Trade_value':Trade_value, 
                                    'Trade_direction':Trade_direction, 
                                    'NOP':current_nop, 
                                    'VWABid':None,
                                    'VWAOffer':None
                    }
                    append_PnL_book = pd.DataFrame([append_PnL_book])
                    self.PnLBook = pd.concat([self.PnLBook, append_PnL_book], ignore_index=True)
                    self.algo_memory['open'] = True
                    self.algo_memory['close'] = True
                    self.algo_memory['momentum_direction_close'] = 'SELL'
                else:
                    Trade_value = onData['offer'].min()
                    Trade_direction = "SELL"
                    append_PnL_book = {
                                    'Product':current_product, 
                                    'Trade_value':Trade_value, 
                                    'Trade_direction':Trade_direction, 
                                    'NOP':current_nop, 
                                    'VWABid':None,
                                    'VWAOffer':None
                    }
                    append_PnL_book = pd.DataFrame([append_PnL_book])
                    self.PnLBook = pd.concat([self.PnLBook, append_PnL_book], ignore_index=True)
                    self.algo_memory['open'] = True
                    self.algo_memory['close'] = True
                    self.algo_memory['momentum_direction_close'] = 'BUY'

        if self.algo_memory['close']:
            time_now = GC - onData['timestamp'].max()
            time_now = time_now.total_seconds() / 60
            if 5 < time_now <= 35:
                if self.algo_memory['momentum_direction_close'] == 'BUY':
                    Trade_value = onData['bid'].max()
                    Trade_direction = "BUY"
                    append_PnL_book = {
                                        'Product':current_product, 
                                        'Trade_value':Trade_value, 
                                        'Trade_direction':Trade_direction, 
                                        'NOP':current_nop, 
                                        'VWABid':None,
                                        'VWAOffer':None
                        }
                    append_PnL_book = pd.DataFrame([append_PnL_book])
                    self.PnLBook = pd.concat([self.PnLBook, append_PnL_book], ignore_index=True)
                    self.algo_memory['close'] = False
                else:
                    Trade_value = onData['offer'].min()
                    Trade_direction = "SELL"
                    append_PnL_book = {
                                        'Product':current_product, 
                                        'Trade_value':Trade_value, 
                                        'Trade_direction':Trade_direction, 
                                        'NOP':current_nop, 
                                        'VWABid':None,
                                        'VWAOffer':None
                        }
                    append_PnL_book = pd.DataFrame([append_PnL_book])
                    self.PnLBook = pd.concat([self.PnLBook, append_PnL_book], ignore_index=True)
                    self.algo_memory['close'] = False