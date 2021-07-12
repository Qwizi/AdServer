from celery import shared_task
from celery.schedules import crontab

from ads.models import Ad
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def deposit_ads():
    logger.info("The sample task just ran.")
    ads = Ad.objects.filter(is_active=True, balance__gt=0)
    print(ads)
    for ad in ads:
        ad.balance -= 1
        if ad.balance <= 0:
            ad.is_active = False
            ad.balance = 0
        ad.save()
