# Author: Navesh Kumar
# date : 20 october 2024
# Version 1

import pandas as pd
from import_data import LoadData, PnLTransformation

def CreatePnLBook():
    PnLBook = pd.DataFrame(columns=['Product', 
                                    'Trade_value', 
                                    'Trade_direction', 
                                    'NOP', 
                                    'VWABid',
                                    'VWAOffer'])
    return PnLBook

def CalculatePnL(products_to_be_traded,PnLBook,filepath):
    PnLBook = PnLBook.copy()
    # per product calculate the volume weigthed average bid and offer
    for product in products_to_be_traded:
        this_product_full_data = LoadData(product,filepath)
        this_product_full_data = PnLTransformation(product,this_product_full_data)
        
        VWABid = this_product_full_data['bid'] * this_product_full_data['bv'] / this_product_full_data['bv']
        VWAOffer = this_product_full_data['offer'] * this_product_full_data['ov'] / this_product_full_data['ov'] 

        PnLBook.loc[
            PnLBook['Product'] == product,
            'VWABid'
        ] = VWABid

        PnLBook.loc[
            PnLBook['Product'] == product,
            'VWAOffer'
        ] = VWAOffer

    # the profit loss statement of the BUY is determined by how less was the trade from the VWA Bid
    PnLBook.loc[
        PnLBook['Trade_direction'] == 'BUY',
        'BidPnL'
    ] = PnLBook['VWABid'] - PnLBook['Trade_value']

    # the profit loss statement of the SELL is determined by how more was the trade from the VWA Offer
    PnLBook.loc[
        PnLBook['Trade_direction'] == 'SELL',
        'OfferPnL'
    ] = PnLBook['Trade_value'] - PnLBook['VWABid']

    # Final profit of this strategy is the difference between SELL and BUY
    # profit is SELL - BUY but by design they appear on different rows
    # hence they are calculated separately and then merged with final df
    # since BUY is -ve revenue and SELL is +ve revenue we convert Trade_value for buys to -ve

    PnLBook[
        PnLBook['Trade_direction'] == 'BUY',
        'Trade_value'
    ] = -PnLBook['Trade_value']

    # now summing to get the Net Revenue
    net_revenue_df = PnLBook.groupby(
        'Product',
        as_index = False
        )['Trade_value'].sum()
    net_revenue_df = net_revenue_df.rename(columns = {
        'Trade_value' : 'Net_Reveue'
    })

    PnLBook = pd.merge(PnLBook,net_revenue_df,
                       on = 'Product',
                       how= 'left')