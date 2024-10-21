# Author: Navesh Kumar
# date : 20 october 2024
# Version 1

import pandas as pd
from import_data import LoadData, PnLTransformation

def CreatePnLBook():
    PnLBook = pd.DataFrame(columns=['Product', 
                                    'Trade_value', 
                                    'Trade_direction', 
                                    'NOP'])
    return PnLBook

def CalculatePnL(products_to_be_traded,PnLBook,filepath,outpath):
    PnLBook = PnLBook.copy()
    PnLBook['VWABid'] = None
    PnLBook['VWAOffer'] = None

    # per product calculate the volume weigthed average bid and offer
    for product in products_to_be_traded:
        this_product_full_data = LoadData(product,filepath)
        this_product_full_data = PnLTransformation(product,this_product_full_data)
        
        # Ensure no NaN values for VWABid calculation
        valid_bid_data = this_product_full_data[['bid', 'bv']].dropna()

        # Calculate VWABid
        VWABid = (valid_bid_data['bid'] * valid_bid_data['bv']).sum() / valid_bid_data['bv'].sum()

        # Ensure no NaN values for VWAOffer calculation
        valid_offer_data = this_product_full_data[['offer', 'ov']].dropna()

        # Calculate VWAOffer
        VWAOffer = (valid_offer_data['offer'] * valid_offer_data['ov']).sum() / valid_offer_data['ov'].sum()

        PnLBook.loc[PnLBook['Product'] == product, 'VWABid'] = VWABid

        PnLBook.loc[PnLBook['Product'] == product,'VWAOffer'] = VWAOffer


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