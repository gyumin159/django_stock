from webpush.utils import send_to_subscription
import json # https://github.com/safwanrahman/django-webpush/issues/71
from webpush import send_user_notification


from celery import shared_task
import requests
from bs4 import BeautifulSoup as BS
from stock.models import NewsData, StockCode
from django.contrib import messages

@shared_task
def get_each_news():
    code_list = StockCode.objects.filter(has_user=True)
    for code in code_list:
        crawler(code.company_code)


def crawler(next):
    contents = []
    base_url = 'https://finance.naver.com/item/news_news.naver?code='
    code = next

    get_html = requests.get(base_url + code.zfill(6))  # zfill(6) 을 하면 6299 이런 코드들을 006299 이렇게 네이버에서 다루는 코드양식으로 바꿔줌
    soup = BS(get_html.text, 'html.parser')
    news_box = soup.find('tbody')
    news_list = news_box.find_all('tr')

    for news in news_list:
        title = news.find('a', 'tit').get_text()
        info = news.find('td', 'info').string
        date = news.find('td', 'date').string
        link = 'https://finance.naver.com' + news.find('a').attrs['href']

        comb = {'title': title, 'info': info, 'date': date, 'link': link}
        contents.append(comb)
    act(contents, code)
    
def act(contents, code):
    for news in contents:
        current_stock = StockCode.objects.get(company_code=code)
        if NewsData.objects.filter(title = news['title']).first():
            pass
        else:
            NewsData(title = news['title'], info = news['info'], date = news['date'], link= news['link'],
            related_code=StockCode.objects.get(company_code=code)).save()
            
            # if current_stock.crawl_count == 0:
            #     current_stock.crawl_count += 1
            #     current_stock.save()
            # else:
            webpush(news, StockCode.objects.get(company_code=code))



def webpush(news, stock_obj):
    
    users = stock_obj.interested_user.all()


    payload = {"head": f"{stock_obj.company_name} 업데이트 되었습니다.", "body": news['title'], 
             "url": news['link']}
     
    #payload = json.dumps(payload) # json으로 변환 https://github.com/safwanrahman/django-webpush/issues/71

    for user in users:
        send_user_notification(user=user, payload=payload, ttl=100)
        