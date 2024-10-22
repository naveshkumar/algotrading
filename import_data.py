# import data from exchange and other sources if necessary

# Author: Navesh Kumar
# date : 22 october 2024
# Version 2
# this version has been modified to be compatiable with the data recived on 21 Oct 2024

import os
import pandas as pd
from datetime import datetime, timezone, timedelta

def GetData(source_path,current_product,POS,POE,product_category,context):
    try:
        if context == 'Backtest':
            _ , deliveryStart = current_product.split('-')

            #deliveryStart with POS and POE will locate the relevant files
            # prd_id will filter the relevant data from the files
            deliveryStart_dt = datetime(*[*map(lambda _d:int(_d),[*deliveryStart.split('_')])])

            # IMPORTANT!!: CORRECTION #1 : Reducing date by 1 year to find the file
            deliveryStart_dt = deliveryStart_dt - timedelta(days=365) # 2022 and 2023 are not leap years

            # IMPORTANT!!: CORRECTION #1 : Reducing date by 1 year to find the file
            deliveryStart_dt = deliveryStart_dt - timedelta(minutes=60) # TZ -01:00

            # Gate Closure Calculations is kept at zero as the snapshots are at 5 min interval and so is the GC
            deliveryStart_dt_GC = deliveryStart_dt + timedelta(minutes=0)

            #calculating the POS and POE
            POS_dt = deliveryStart_dt_GC - timedelta(minutes=POS)
            POE_dt = deliveryStart_dt_GC - timedelta(minutes=POE)

            # name of the files we need to collect
            collect_files = []
            collect_this = POS_dt
            while collect_this <= POE_dt:
                collect_this_str = f"snapshot_{collect_this.year}_{collect_this.month}_{collect_this.day}_{collect_this.hour}_{collect_this.minute}_{collect_this.second}.parquet"
                collect_files.append(collect_this_str)
                collect_this = collect_this + timedelta(minutes=5)

            # get the files from the data location    
            matching_files_dataframes = []
            for file in collect_files:
                file_path = os.path.join(source_path, file)
                df = pd.read_parquet(file_path)
                file_str = os.path.splitext(file)[0].replace('snapshot_', '')
                file_str = datetime(*[*map(lambda _d:int(_d) ,file_str.split('_')) ])
                df['timestamp'] = file_str
                matching_files_dataframes.append(df)

            if matching_files_dataframes:
                combined_df = pd.concat(matching_files_dataframes, ignore_index=True)
            else:
                combined_df = pd.DataFrame()
            # IMPORTANT!! Only considering XBID market
            all_products = {
                            'HH': 'XBID_Half_Hour',
                            'QH': 'XBID_Quarter_Hour',
                            'H' : 'XBID_Hour'
                            }
            
            filter_product = all_products[product_category]
            combined_df = combined_df[combined_df['Product'] == filter_product]

            # filtering the instrument
            # formatting filter_instrument for filter query
            
            filter_instrument = deliveryStart_dt
            # IMPORTANT!! : Re-Correction of datetime back to UTC +00:00
            filter_instrument = filter_instrument + timedelta(minutes=60)
            # IMPORTANT!! : Re-Correction of datetime back to 2023
            filter_instrument = filter_instrument + timedelta(days=365)
            filter_instrument = filter_instrument.replace(tzinfo=timezone.utc)
            filter_instrument = pd.Timestamp(filter_instrument)

            combined_df = combined_df[combined_df['DeliveryStart']==filter_instrument]

            # Important!! : Correcting the timestamp bringing it back to 2023
            combined_df['timestamp'] = combined_df['timestamp'] + pd.DateOffset(days=365)
            # Important!! : Correcting the timestamp for time zone
            combined_df['timestamp'] = combined_df['timestamp'] + pd.DateOffset(hours=1)
            
            combined_df = combined_df.reset_index()

            # IMPORTANT!! : Re-Correction of datetime back to 2023
            GC = deliveryStart_dt_GC + timedelta(days=365)
            # IMPORTANT!! : Re-Correction of datetime back to UTC +00:00
            GC = GC + timedelta(minutes=60)
    except Exception as e:
        print(f"Error in Data Extraction {e}")

    return combined_df , GC