# import data from exchange and other sources if necessary

# Author: Navesh Kumar
# date : 19 october 2024
# Version 

# wrangle data from specified source to be made available in known format

def LoadData(product):
    #collect all file names from the output location
    #from product get the product-YYYY_MM_DD_HH_Min_SS
    # split the string to isloate the date YYYY_MM_DD_HH_Min_SS
    # search for the files with the same name matching till YYYY_MM_DD (pick the day of trading)
    # merge all the data
    #return mergedLoadedData
    pass
def TransformData():
    # get the merged data
    #filter the product
    # isolate the date from AOS to AOE
    # create the foundation data format time | Bid | BV | Offer | OV
    #return foundationdata
    pass
# Step 2: non-compatiable format to compatiable format transformation
# Step 2.1 : Get data requirements from 

def GetData(product,AOS,AOE,context):

    #if context == "Backtest":
    #    DataUpload = LoadData(product)
    #    foundation =TransformData(product,DataUpload,AOS,AOE)
    #else:
    #    print("Connecting to Live Stream ......")
        
    #return foundation
    return 100