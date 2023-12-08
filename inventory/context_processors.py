import datetime as datetime
from POS.models import Sale, Register


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


def reg(request):
    user = request.user
    if not user.is_anonymous:
        reg = Register.objects.filter(user=user, status='O').first()
        return {'reg': reg}
    else:
        return {'reg': None}
