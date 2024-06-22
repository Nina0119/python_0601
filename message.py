from linebot.v3.messaging.models import *

# Function Definitions
def buttons_message1():
    message = TemplateMessage(
        alt_text='基本股票功能',
        template=ButtonsTemplate(
            text='請選擇以下功能',
            actions=[
                MessageAction(
                    label="查詢股票資訊",
                    text="查詢股票資訊"
                ),
                MessageAction(
                    label="歷史股價查詢",
                    text="歷史股價查詢"
                )
            ]
        )
    )
    return message

def buttons_message2():
    message = TemplateMessage(
        alt_text='換股',
        template=ButtonsTemplate(
            text='請選擇以下功能',
            actions=[
                MessageAction(
                    label="換股時間",
                    text="換股時間"
                ),
                MessageAction(
                    label="換了哪些股",
                    text="換了哪些股"
                )
            ]
        )
    )
    return message

def Carousel_Template():
    carousel_template_message = TemplateMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Number_1_in_green_rounded_square.svg/200px-Number_1_in_green_rounded_square.svg.png',
                    title='股票相關功能',
                    text='Description 1',
                    actions=[
                        MessageAction(
                            label='財報',
                            text='財報'
                        ),
                        MessageAction(
                            label='基本股票功能',
                            text='基本股票功能'
                        ),
                        MessageAction(
                            label='換股',
                            text='換股'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRuo7n2_HNSFuT3T7Z9PUZmn1SDM6G6-iXfRC3FxdGTj7X1Wr0RzA',
                    title='其他相關功能',
                    text='Description 2',
                    actions=[
                        URIAction(
                            label='互動式網站',
                            uri='https://backtest-kk2m.onrender.com/one_stock?id=0056&amount=3000&date=5&duration=1'
                        ),
                        MessageAction(
                            label='新聞',
                            text='新聞'
                        ),
                        MessageAction(
                            label='回測',
                            text='回測'
                        ),
                        # URIAction(
                        #     label='定期定額 回測API',    
                        #     uri='https://backtest-kk2m.onrender.com/one_stock?id=0056&amount=3000&date=5&duration=1'
                        # )
                    ]
                )
            ]
        )
    )
    return carousel_template_message
