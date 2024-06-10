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

def fetch_and_filter_news_message(keywords, pages=5, limit=5):
    cnyes_news_spider = CnyesNewsSpider()
    newslist_info = cnyes_news_spider.get_newslist_info(pages=pages, limit=limit)
    
    if newslist_info:
        filtered_news = cnyes_news_spider.filter_news(newslist_info, keywords)
        print(f'搜尋結果 > 符合條件的新聞總數：{len(filtered_news)}')
        
        columns = []
        for news in filtered_news[:10]:  # 只显示最多10条新闻
            column = ImageCarouselColumn(
                image_url="https://via.placeholder.com/300",  # 这里应该使用新闻的图片URL
                action=URITemplateAction(
                    label=news["title"],
                    uri=f"https://news.cnyes.com/news/id/{news['newsId']}"
                )
            )
            columns.append(column)
        
        message = TemplateSendMessage(
            alt_text='新聞旋轉木馬',
            template=ImageCarouselTemplate(columns=columns)
        )
        return message
    return None

# Example of usage
if __name__ == "__main__":
    keywords = ["ETF", "股票", "殖利率"]
    message = fetch_and_filter_news_message(keywords, pages=5, limit=5)
    if message:
        print(message)
    else:
        print("No news found.")
