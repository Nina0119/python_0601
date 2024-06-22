import requests, re
from linebot.v3.messaging import TextMessage

def get_stock_data(id, amount, duration):
    url = 'https://backtest-kk2m.onrender.com/one_stock'
    params = {
        'id': id,
        'amount': amount,
        'duration': duration
    }
    response = requests.get(url, params=params)
    return response.json()


# for 定期定額使用
def backtest(msg):
    parts = msg.split(',')
    numbers = [re.findall(r'\d+', part) for part in parts]
    inputs = [numbers[0][0]] + [int(num) for sublist in numbers[1:] for num in sublist]
    
    send_text = ""
    if len(numbers) ==3:
        results = get_stock_data(inputs[0], inputs[1], inputs[2])
        # 提取 id
        stock_id = results.get("id")
        # 提取 info
        stock_info = results.get("info")
        # 提取 analysis
        stock_analysis = results.get("analysis")
        # 构建字符串
        send_text = ""

        send_text += f"定期定額投資: {stock_id}\n"
        for value in stock_info:
            send_text += f"{value}\n"
        for value in stock_analysis:
            send_text += f"{value}\n"
        send_text += f"(Notes:不包含股利計算)"

            
    else:
        send_text = "資料錯誤"
    
    message = TextMessage(text=send_text)
    return message