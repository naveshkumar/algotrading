def product_to_time_mapping(product_delivery_time_string):
    hour, minute = map(int, product_delivery_time_string.split('_')[3:5])
    product_number = (hour * 2) + (1 if minute == 0 else 2)
    return f"HH{product_number:02}" , product_number