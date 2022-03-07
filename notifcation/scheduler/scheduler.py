from apscheduler.schedulers.background import BackgroundScheduler
from notifcation.views import send_note


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_note, 'interval', seconds=15665644, name='clean_accounts')
    scheduler.start()
    