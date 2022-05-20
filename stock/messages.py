from firebase_admin.messaging import Message
from fcm_django.models import FCMDevice
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StockWeb.settings")
import django
django.setup()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

message_obj = Message(
    data={
        "Nick" : "Mario",
        "body" : "great match!",
        "Room" : "PortugalVSDenmark"
   },
)

# You can still use .filter() or any methods that return QuerySet (from the chain)
device = FCMDevice.objects.all().first()
# send_message parameters include: message, dry_run, app
device.send_message(message_obj)