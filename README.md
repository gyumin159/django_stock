# django_stock
first project

It helps you to keep in touch with latest news of stocks you're interested in.

How to use

1. install requirements & redis (https://redis.io/docs/getting-started/)
2. start the redis server (sudo service redis-server start)
3. go to dir where manage.py located
4. start the django server
5. start celery (celery -A StockWeb worker -l info --pool=solo)
6. start celery beat (celery -A StockWeb.celery beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler)

you can change the duration of crawling in admin site by creating superuser
