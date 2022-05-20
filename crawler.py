import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StockWeb.settings")
import django
django.setup()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import requests
from bs4 import BeautifulSoup as BS
from stock.models import NewsData, StockCode

def get_each_news():
    code_list = StockCode.objects.filter(has_user=True)
    for code in code_list:
        crawler(code.company_code.zfill(6))


def crawler(next):
	contents = []
	base_url = 'https://finance.naver.com/item/news_news.naver?code='
	code = next

	get_html = requests.get(base_url + code)
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

	if __name__=='__main__':
		for news in contents:
			if NewsData.objects.filter(title = news['title']).first():
				pass
			else:
				NewsData(title = news['title'], info = news['info'], date = news['date'], link= news['link'],
				related_code=StockCode.objects.get(company_code=code.lstrip('0'))).save()
    

get_each_news()