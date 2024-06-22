import twstock
from linebot.v3.messaging import TextMessage

def get_stock_price(stock_code):
    stock = twstock.realtime.get(stock_code)
    if stock['success']:
        return stock['realtime']['open'], stock['realtime']['latest_trade_price']
    message = TextMessage(text="Failed to retrieve data for stock code: {stock_code}")
    return message

def create_stock_message(stock_code):
    open_price, close_price = get_stock_price(stock_code)
    if open_price and close_price:
        send_text = f"Stock Code: {stock_code}\n"
        send_text += f"Open Price: {open_price}\n"
        send_text += f"Close Price: {close_price}\n"
        message = TextMessage(text=send_text)
    else:
        send_text = "Failed to retrieve stock prices."
        message = TextMessage(text=send_text)
    return message
