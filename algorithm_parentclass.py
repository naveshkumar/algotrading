# Parent class code which is also the orchestrator for trading all the products specified

# Author: Navesh Kumar
# date : 19 october 2024
# Version 1

from import_data import GetData
from datetime import datetime

class general_algo_framework():
    
    def SetContext(self,context):
        try:
            self.context = context
        except Exception as e:
            print("Error in SetContext {e}")
            return
    
    def SetDataLocation(self,filepath):
        try:
            if self.context == "Backtest":
                #filepath is a location with parquet files are
                self.filepath = filepath
            elif self.context == "Live":
                print("Build Ingress Stream Here")
        except Exception as e:
            print("Error in SetDataLocation {e}")
    
    def SetAlgoObservationStart(self,OriginDate):
        try:
            string_Origin = OriginDate
            self.Origin = datetime.strptime(string_Origin,'%Y-%m-%d')
        except Exception as e:
            print("Error in SetAlgoObservationStart {e}")

    def SetAlgoObservationEnd(self,EndDate):
        try:
            string_End = EndDate
            self.End = datetime.strptime(string_End,'%Y-%m-%d')
            check_logical_delta = self.End - self.Origin
            if check_logical_delta.days <0:
                raise ValueError("End date is before Start")
        except Exception as e:
            print("Error in SetAlgoObservationStart {e}")

    def SetProductObservationStart(self,AOS):
        try:
            string_AOS = AOS
            self.AOS = float(string_AOS)
        except Exception as e:
            print("Error in SetAlgoObservationStart {e}")

    def SetProductObservationEnd(self,AOE):
        try:
            string_AOE = AOE
            self.AOE = float(string_AOE)
            check_logical_delta = self.AOS - self.AOE
            if check_logical_delta <0:
                raise ValueError("End date is before Start")
        except Exception as e:
            print("Error in SetAlgoObservationStart {e}")

    def SetProducts(self,products):
        try:
            product_dict = products
            self.products = product_dict['HH']
        except Exception as e:
            print("Error in SetProducts {e}")
    
    def SetAlgoMemory(self,algo_memory):
        try:
            self.algo_memory = algo_memory
        except Exception as e:
            print("Error in SetProducts {e}")


    def process_product(self):
        try:
        # loop through the data
            for current_product in self.products:
                # initate the memory
                self.algo_memory['open'] = False
                self.algo_memory['close'] = False

                #collect the full data for current_product
                # w.r.t Origin,End, AOS, AOE
                foundation_data = GetData(current_product,
                                          self.Origin,
                                          self.End,
                                          self.AOS,
                                          self.AOE,
                                          self.context)
                print(f'for {current_product} data is {foundation_data}')

        except Exception as e:
            print("Error in implementing algorithm {e}")
        

