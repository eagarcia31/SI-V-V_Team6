def buy_item(item: str, payment_method: str, amount: Union[int, float]) -> Tuple[str, Union[float, None]]:
    price = get_item_price(item)
    if price is None:
        return "Sorry, that item is not available.", None
    if payment_method not in ACCEPTED_PAYMENT_METHODS:
        return "Sorry, we do not accept that payment method.", None
    if amount < price:
        return "Please insert more money.", None
    change = amount - price
    # Dispense item and change, update inventory and sales records
    update_inventory(item, -1)
    update_sales_record(item, price)
    if change == 0:
        return "Thank you for your purchase! Here's your {}.".format(item), None
    else:
        return "Thank you for your purchase! Here's your {} and your change of ${}.".format(item, change), change
