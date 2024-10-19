# Algorithm sub-class for first implementation and subsequent implementations

# Author: Navesh Kumar
# Date: 19 oct 2024
# version : 2024.10.19.01.01

from algorithm_parentclass import general_algo_framework

class momentumalgo(general_algo_framework):
    
    def DataSetup(self):
        self.SetContext("Backtest")
        self.SetDataLocation("filepath")

    def TimeContext(self):
        self.SetAlgoObservationStart('2024-10-01') # date
        self.SetAlgoObservationEnd('2024-10-10') #date
        self.SetProductObservationStart(40) # minutes
        self.SetProductObservationEnd(20) # minutes
        self.SetProducts(
            {
                'HH':[1,2,3,4,5,6,7,8,9,10,11,12,
                    13,14,15,16,17,18,19,20,21,22,23,24,
                    25,26,27,28,29,30,31,32,33,34,35,36,
                    37,38,39,40,41,42,43,44,45,46,47,48]
            }
                        )
        
    def AlgoMemory(self):
        self.SetAlgoMemory(
            {
            'open': False,
            'close':False
            }
        )
    
    def Algorithm(self):
        pass