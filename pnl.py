# Author: Navesh Kumar
# date : 20 october 2024
# Version 1

import pandas as pd
from import_data import GetData

def CreatePnLBook():
    PnLBook = pd.DataFrame(columns=['Product', 
                                    'Trade_value', 
                                    'Trade_direction', 
                                    'NOP'])
    return PnLBook

def CalculatePnL(products_to_be_traded,
                 POS,
                 POE,
                 PnLBook,
                 product_catogory,
                 context,
                 filepath,
                 outpath):
    PnLBook = PnLBook.copy()
    PnLBook['VWABid'] = None
    PnLBook['VWAOffer'] = None

    # per product calculate the volume weigthed average bid and offer
    for current_product in products_to_be_traded:
        this_product_full_data, GC = GetData(filepath,
                                        current_product,
                                        POS,
                                        POE,
                                        product_catogory,
                                        context)

        
        # Ensure no NaN values for VWABid calculation
        valid_bid_data = this_product_full_data[['Bid', 'BQty']].dropna()
        valid_bid_data['Bid'] = pd.to_numeric(valid_bid_data['Bid'], errors='coerce')

        # Calculate VWABid
        VWABid = (valid_bid_data['Bid'] * valid_bid_data['BQty']).sum() / valid_bid_data['BQty'].sum()

        # Ensure no NaN values for VWAOffer calculation
        valid_offer_data = this_product_full_data[['Ask', 'AQty']].dropna()
        valid_offer_data['Ask'] = pd.to_numeric(valid_offer_data['Ask'], errors='coerce')

        # Calculate VWAOffer
        VWAOffer = (valid_offer_data['Ask'] * valid_offer_data['AQty']).sum() / valid_offer_data['AQty'].sum()

        PnLBook.loc[PnLBook['Product'] == current_product, 'VWABid'] = VWABid
        PnLBook.loc[PnLBook['Product'] == current_product,'VWAOffer'] = VWAOffer


    # the profit loss statement of the BUY is determined by how less was the trade from the VWA Bid
    PnLBook.loc[PnLBook['Trade_direction'] == 'BUY', 'BidPnL'] = PnLBook['VWABid'] - PnLBook['Trade_value']

    # the profit loss statement of the SELL is determined by how more was the trade from the VWA Offer
    PnLBook.loc[PnLBook['Trade_direction'] == 'SELL','OfferPnL'] = PnLBook['Trade_value'] - PnLBook['VWABid']

    # Final profit of this strategy is the difference between SELL and BUY
    # profit is SELL - BUY but by design they appear on different rows
    # hence they are calculated separately and then merged with final df
    # since BUY is -ve revenue and SELL is +ve revenue we convert Trade_value for buys to -ve

    PnLBook.loc[PnLBook['Trade_direction'] == 'BUY', 'NOP'] = -PnLBook.loc[PnLBook['Trade_direction'] == 'BUY', 'NOP']

    PnLBook['Revenue'] = PnLBook['Trade_value'] * PnLBook['NOP']

    # now summing to get the Net Revenue
    net_revenue_df = PnLBook.groupby(
        'Product',
        as_index = False
        )['Revenue'].sum()
    
    net_revenue_df = net_revenue_df.rename(columns = {
        'Revenue' : 'Net_Reveue'
    })

    PnLBook = pd.merge(PnLBook,net_revenue_df,
                       on = 'Product',
                       how= 'left')
    outpath = f'{outpath}/pnl.csv'
    PnLBook.to_csv(outpath,index=False)