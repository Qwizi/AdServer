from django_cron import CronJobBase, Schedule

from ads.models import Ad


class AdCronJob(CronJobBase):
    #RUN_AT_TIMES = ['18:00']
    RUN_EVERY_MINS  = 2
    #schedule = Schedule(run_at_times=RUN_AT_TIMES)
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ads.cronjob'  # a unique code

    def do(self):
        ads = Ad.objects.filter(is_active=True, balance__gt=0)
        for ad in ads:
            ad.balance -= 1
            if ad.balance <= 0:
                ad.is_active = False
                ad.balance = 0
            ad.save()
