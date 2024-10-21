# Parent class code which is also the orchestrator for trading all the products specified

# Author: Navesh Kumar
# date : 19 october 2024
# Version 1

from import_data import GetData
from datetime import datetime, timedelta
from product_gc_mapping import products_to_be_traded_generator
from net_open_position_source import GetNOP
from pnl import CreatePnLBook, CalculatePnL

class general_algo_framework():
    
    def SetContext(self,context):
        try:
            self.context = context
        except Exception as e:
            print(f"Error in SetContext {e}")
            return
    
    def SetDataLocation(self,filepath):
        try:
            if self.context == "Backtest":
                #filepath is a location with parquet files are
                self.filepath = filepath
            elif self.context == "Live":
                print("Build Ingress Stream Here")
        except Exception as e:
            print(f"Error in SetDataLocation {e}")

    def SetOutputLocation(self,outpath):
        try:
            if self.context == "Backtest":
                #filepath is a location with parquet files are
                self.outpath = outpath
            elif self.context == "Live":
                print("Build Ingress Stream Here")
        except Exception as e:
            print(f"Error in SetOutputLocation {e}")
    
    def SetAlgoObservationStart(self,OriginDate):
        try:
            self.Origin = datetime(*OriginDate)
        except Exception as e:
            print(f"Error in SetAlgoObservationStart {e}")

    def SetAlgoObservationEnd(self,EndDate):
        try:
            self.End = datetime(*EndDate)
            check_logical_delta = self.End - self.Origin
            if check_logical_delta.days <0:
                raise ValueError("End date is before Start")
        except Exception as e:
            print(f"Error in SetAlgoObservationEnd {e}")

    def SetProductObservationStart(self,POS):
        try:
            string_POS = POS
            self.POS = float(string_POS)
        except Exception as e:
            print(f"Error in SetAlgoObservationStart {e}")

    def SetProductObservationEnd(self,POE):
        try:
            string_POE = POE
            self.POE = float(string_POE)
            check_logical_delta = self.POS - self.POE
            if check_logical_delta <0:
                raise ValueError("End date is before Start")
        except Exception as e:
            print(f"Error in SetAlgoObservationStart {e}")

    def SetProducts(self,products):
        try:
            product_dict = products
            self.product_catogory =[*product_dict.keys()][0]
            _key_var = [*product_dict.keys()][0]
            self.products = product_dict[_key_var]
        except Exception as e:
            print(f"Error in SetProducts {e}")

    def DoCreateTradeSchdule(self):
        try:
           self.products_to_be_traded = products_to_be_traded_generator(self.products,
                                                                        self.product_catogory,
                                                                        self.Origin,
                                                                        self.End)
        except Exception as e:
            print(f"Error in DoCreateTradeSchdule {e}")
    
    def Set_algo_memory(self,algo_memory):
        try:
            self.algo_memory = algo_memory
        except Exception as e:
            print(f"Error in SetProducts {e}")
    
    def DoCreatePnLBook(self):
        try:
            self.PnLBook = CreatePnLBook()
        except Exception as e:
            print(f"Error in DoCreatePnLBook {e}")


    def process_product(self):
        try:
        # loop through the data
            for current_product in self.products_to_be_traded:
                self.AlgoMemory()
                #collect the data for current_product
                # w.r.t Origin,End, AOS, AOE
                foundation_data, GC = GetData(current_product,
                                          self.POS,
                                          self.POE,
                                          self.context,
                                          self.filepath)
                
                if self.context == "Backtest":
                    current_nop = GetNOP()

                    # in case of backtesting foundation_data will be a dataframe
                    simulator =  foundation_data['timestamp'].min()
                    simulation_end = foundation_data['timestamp'].max()

                    while simulator <= simulation_end:
                        foundation_data_slice = foundation_data[
                                                                foundation_data['timestamp'] <= simulator
                                                                ]
                        self.Algorithm(current_product,
                                       foundation_data_slice,
                                       GC,
                                       current_nop)
                        simulator = simulator + timedelta(seconds=5)
                else:
                    # in case of live foundation_data will be a connection
                    print("Live Trading ....")
            CalculatePnL(self.products_to_be_traded,self.PnLBook,self.filepath,self.outpath)
        except Exception as e:
            print(f"Error in product {current_product} implementing algorithm {e}")
        

