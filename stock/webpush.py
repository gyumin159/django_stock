from django.contrib.auth import get_user_model

from webpush import send_user_notification
from webpush.utils import send_to_subscription
from webpush import send_group_notification

import json # https://github.com/safwanrahman/django-webpush/issues/71

def episode_webpush():

    User = get_user_model()
    users = User.objects.all()

    payload = {"head": "이 업데이트 되었습니다.", "body": "업데이트 일시", 
            "icon": "https://i.imgur.com/...", "url": "asdasd"}
     
    payload = json.dumps(payload) # json으로 변환 https://github.com/safwanrahman/django-webpush/issues/71

    for user in users:
        push_infos = user.webpush_info.select_related("subscription") 

        for push_info in push_infos:
            send_to_subscription(push_info.subscription, payload)