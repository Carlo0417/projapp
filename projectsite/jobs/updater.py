from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import add_billing, add_rent_bill

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(add_billing, 'interval', seconds=5)
	scheduler.add_job(add_rent_bill, 'interval', hours=0)
	scheduler.start()

	