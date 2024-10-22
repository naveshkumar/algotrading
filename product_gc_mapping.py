from datetime import datetime, timedelta
def products_to_be_traded_generator(products,product_catogory,origin,end):
    if product_catogory == 'HH':
        collect_products_to_be_traded = []
        delivery_period = origin
        # rounding to nearest delivery period
        m = delivery_period.minute
        if m == 0:
            delivery_period.replace(second = 0,microsecond = 0)
        elif m <= 30:
            delivery_period.replace(minute = 30, second = 0,microsecond = 0)
        else:
            (delivery_period + timedelta(hours=1)).replace(minute = 0, second = 0,microsecond = 0)

        while delivery_period <= end:
            collect_products_to_be_traded.append(delivery_period)
            delivery_period = delivery_period + timedelta(minutes = 30)

    if product_catogory == 'QH':
        collect_products_to_be_traded = []
        delivery_period = origin
        m = delivery_period.minute
        if m % 15 == 0:
            delivery_period = delivery_period.replace(second=0, microsecond=0)
        else:
            # Calculate the nearest quarter-hour
            minute_adjustment = (15 - m % 15) % 15
            delivery_period = delivery_period + timedelta(minutes=minute_adjustment)
            delivery_period = delivery_period.replace(second=0, microsecond=0)

        # Collect quarter-hourly products
        while delivery_period <= end:
            collect_products_to_be_traded.append(delivery_period)
            delivery_period = delivery_period + timedelta(minutes=15)

    #convert the datetime into string for getting data
    str_products_to_be_traded = []
    for product in collect_products_to_be_traded:
        str_products_to_be_traded.append(f"{product.year}_{str(product.month)}_{str(product.day)}_{str(product.hour)}_{str(product.minute)}_{str(product.second)}")

    products_to_be_traded = []
    #find the product number for this delivery period
    for product_string in str_products_to_be_traded:
        product_map_id , check_entry_prd = product_to_time_mapping(product_catogory,product_string)
        if check_entry_prd in products:
            products_to_be_traded.append(f"{product_map_id}-{product_string}")
    
    return products_to_be_traded


def product_to_time_mapping(product_catogory,product_delivery_time_string):
    if product_catogory == 'HH':
        hour, minute = map(int, product_delivery_time_string.split('_')[3:5])
        product_number = (hour * 2) + (1 if minute == 0 else 2)
        return f"{product_catogory}{product_number:02}" , product_number
    
    if product_catogory == 'QH':
        hour, minute = map(int, product_delivery_time_string.split('_')[3:5])
        product_number = (hour * 4) + (minute // 15) + 1
        return f"{product_catogory}{product_number:02}", product_number


