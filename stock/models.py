from turtle import ondrag
from django.db import models
from django.contrib.auth.models import User

class StockCode(models.Model):
    company_code = models.TextField()
    company_name = models.CharField(max_length=50)
    stock_market_type = models.CharField(max_length=30)
    business_type_code = models.TextField()
    business_type = models.TextField()
    has_user = models.BooleanField(default=False)  # 관심가진 유저가 있는가 확인하며, 유저의 관심을 받은 종목들만 크롤링 할 것이기 때문에 그 종목만 모으기 위해 만듬. 
                                                    # 원래는 StockCode와 User 사이에 생긴 junction 테이블에 접근하고 싶었으나 어떻게 하는질 모르겠음.
    crawl_count = models.PositiveIntegerField(default=0)  # 첫번째 크롤링 시에는 메세지를 발송하지 않기위해. 하지만 한 유저의 관심목록에 있다가 없어진 후 오랜시간이 지나면 어떻게? 매일 아침마다 0으로 세팅되면 좋겠다.
    
    interested_user = models.ManyToManyField(User, related_name='interested_code')
    
    def __str__(self):
        return f'{self.company_name} - {self.company_code}'

class NewsData(models.Model):
    title = models.CharField(max_length=50)
    info = models.CharField(max_length=20)
    date = models.TextField()
    link = models.URLField(max_length=200)
    
    related_code = models.ForeignKey(StockCode, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.title}'