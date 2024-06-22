import requests
from linebot.v3.messaging import TextMessage

class CnyesNewsSpider:
    def get_latest_news(self, pages=10, limit=10):
        headers = {
            'Origin': 'https://news.cnyes.com/',
            'Referer': 'https://news.cnyes.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        all_news = []
        for page in range(1, pages + 1):
            try:
                r = requests.get(f"https://api.cnyes.com/media/api/v1/newslist/category/headline?page={page}&limit={limit}", headers=headers, timeout=10)
                r.raise_for_status()  # 如果響應不是200，這將拋出異常
                data = r.json()
                print(f"API Response Page {page}: {data}")  # 打印每個頁面的響應
                all_news.extend(data.get('items', {}).get('data', []))
            except requests.RequestException as e:
                print(f"請求第{page}頁新聞失敗: {e}")
                break
            except ValueError as e:
                print(f"解析第{page}頁 JSON 失敗: {e}")
                break
        return all_news

    def filter_news(self, newslist, keywords):
        filtered_news = []
        for news in newslist:
            if any(keyword.lower() in news.get("title", "").lower() for keyword in keywords):
                filtered_news.append(news)
        return filtered_news

def fetch_and_filter_news_message(keywords, pages=10, limit=10):
    cnyes_news_spider = CnyesNewsSpider()
    latest_news = cnyes_news_spider.get_latest_news(pages=pages, limit=limit)
    print(f"Latest News: {latest_news}")  # 檢查最新新聞

    if latest_news:
        filtered_news = cnyes_news_spider.filter_news(latest_news, keywords)
        # 構建新聞列表消息
        news_list_text = "最新新聞:\n\n"
        for index, news in enumerate(filtered_news, 1):
            news_list_text += f"{index}. {news['title']}\n"
            news_list_text += f"   連結: https://news.cnyes.com/news/id/{news['newsId']}\n\n"

        if filtered_news:
            message = TextMessage(text=news_list_text.strip())
        else:
            message = TextMessage(text="最新新聞中沒有找到相關內容。")
    else:
        message = TextMessage(text="無法獲取最新新聞，請稍後再試。")
    
    return message
