# command line layer for implementation of the intraday trading algorithm
# Author : Navesh Kumar
# Date : 19 oct 2024
# Version 1

import inspect
import sys
import os
import trading_algo_subclass
from algorithm_parentclass import general_algo_framework

if __name__ == "__main__":
    current_working_directory = os.getcwd()
    parent_dir = os.path.dirname(current_working_directory)
    grand_parent_dir = os.path.dirname(parent_dir)

    for name,obj in inspect.getmembers(trading_algo_subclass):
        if inspect.isclass(obj):
            if issubclass(obj,general_algo_framework) and obj is not general_algo_framework:
                subclass_instance = obj()

                if hasattr(subclass_instance,'DataSetup'):
                    subclass_instance.DataSetup()
                if hasattr(subclass_instance,'TimeContext'):
                    subclass_instance.TimeContext()
                if hasattr(subclass_instance,'AlgoMemory'):
                    subclass_instance.AlgoMemory()
                if hasattr(subclass_instance,'process_product'):
                    subclass_instance.process_product()