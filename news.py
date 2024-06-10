#NewsSendMessage(新聞訊息)
import time
import requests
from linebot.models import (
    TemplateSendMessage, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction
)

class CnyesNewsSpider:
    
    def get_newslist_info(self, pages=5, limit=5):
        headers = {
            'Origin': 'https://news.cnyes.com/',
            'Referer': 'https://news.cnyes.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        all_newslist_info = {'data': []}
        for page in range(1, pages + 1):
            r = requests.get(f"https://api.cnyes.com/media/api/v1/newslist/category/headline?page={page}&limit={limit}", headers=headers)
            if r.status_code != requests.codes.ok:
                print(f'請求第 {page} 頁失敗', r.status_code)
                continue
            newslist_info = r.json()['items']
            all_newslist_info['data'].extend(newslist_info['data'])
        return all_newslist_info

    def filter_news(self, newslist_info, keywords):
        filtered_news = []
        for news in newslist_info["data"]:
            if any(keyword in news["keyword"] for keyword in keywords):
                filtered_news.append(news)
        return filtered_news

from linebot.models import TextSendMessage

def fetch_and_filter_news_message(keywords, pages=30, limit=30):
    cnyes_news_spider = CnyesNewsSpider()
    newslist_info = cnyes_news_spider.get_newslist_info(pages=pages, limit=limit)
    print("API Response:", newslist_info)  # 檢查 API 響應

    if newslist_info:
        filtered_news = cnyes_news_spider.filter_news(newslist_info, keywords)
        print("Filtered News:", filtered_news)  # 檢查過濾後的新聞
        print(f'搜尋結果 > 符合條件的新聞總數：{len(filtered_news)}')

        # 構建新聞列表消息
        news_list_text = "最新新聞：\n\n"
        for index, news in enumerate(filtered_news[:10], 1):  # 只顯示最多10條新聞
            news_list_text += f"{index}. {news['title']}\n"
            news_list_text += f"   連結：https://news.cnyes.com/news/id/{news['newsId']}\n\n"

        message = TextSendMessage(text=news_list_text.strip())
        return message
    return None
