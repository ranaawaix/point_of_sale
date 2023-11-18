import datetime as datetime
from POS.models import Sale


def date_time(request):
    dt = datetime.datetime.now()
    return {
        'datetime': dt
    }


def notifications(request):
    notifications = Sale.objects.filter(status='H')
    return {
        'notifications': notifications
    }
