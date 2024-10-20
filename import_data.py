# import data from exchange and other sources if necessary

# Author: Navesh Kumar
# date : 19 october 2024
# Version 

import os
import pandas as pd
from datetime import datetime , timedelta
# wrangle data from specified source to be made available in known format

def LoadData(product,filepath):

    #collect all file names from the output location
    files = os.listdir(filepath)
    parquet_files = [os.path.splitext(file)[0] for file in files if file.endswith('.parquet')]

    #from product get the product-YYYY_MM_DD_HH_Min_SS
    date_of_product = product.split('-')[1]

    # split the string to isloate the date YYYY_MM_DD
    date_of_product_day = '_'.join(date_of_product.split('_')[:3])

    # Get D and D-1
    date_of_product_dt = datetime.strptime(date_of_product_day, '%Y_%m_%d')
        # Calculate the previous day's date
    previous_day_dt = date_of_product_dt - timedelta(days=1)
        # Format the previous day's date to match the file naming format
    previous_day_str = previous_day_dt.strftime('%Y_%m_%d')


    # search for the files with the same name matching till YYYY_MM_DD (pick the day of trading)
    matching_files = [file for file in parquet_files if file.startswith(date_of_product_day) or file.startswith(previous_day_str)]

    matching_files_dataframes = []
    for file in matching_files:
        file_path = os.path.join(filepath, file + '.parquet')
        df = pd.read_parquet(file_path)  # Load the parquet file
        matching_files_dataframes.append(df)

    # merge all the data

    if matching_files_dataframes:
        mergedLoadedData = pd.concat(matching_files_dataframes, ignore_index=True)
    else:
        mergedLoadedData = pd.DataFrame()  # Empty dataframe if no files matched

    return mergedLoadedData

def TransformData(product,DataUpload,POS,POE):
    # get the product
    prd = product.split('-')[0]
    prd_number = int(prd[-2:])

    prd_date = product.split('-')[1]
    prd_date_string = prd_date.split('_')
    base_time = datetime(int(prd_date_string[0]),int(prd_date_string[1]),int(prd_date_string[2]))
    
    # get gate closure
    start_time = base_time + timedelta(minutes=(prd_number - 1) * 30)
    gate_closure_time = start_time - timedelta(minutes=15)

    #filter the product
    foundation_df = DataUpload[
        DataUpload['product_name'] == prd
    ]

    # isolate the date from AOS to AOE
    POE_time = gate_closure_time - timedelta(minutes=POE)
    POS_time = gate_closure_time - timedelta(minutes=POS)

    algo_observed_data = foundation_df[
        (foundation_df['timestamp'] >= POS_time)
        &
        (foundation_df['timestamp'] <= POE_time)
    ]
    # create the foundation data format time | Bid | BV | Offer | OV
        # not needed as dont have sample data on 20 October 2024
    
    return algo_observed_data

# Step 2: non-compatiable format to compatiable format transformation
# Step 2.1 : Get data requirements from 

def GetData(product,POS,POE,context,filepath):

    if context == "Backtest":
        DataUpload = LoadData(product,filepath)
        foundation =TransformData(product,DataUpload,POS,POE)
    else:
        print("Connecting to Live Stream ......")
        
    return foundation