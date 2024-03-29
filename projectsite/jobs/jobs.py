from django.conf import settings
from django.db import connections
from dormitory.models import Service, Bed, Occupant, Bill, Bill_Details
import datetime

from django.utils import timezone

def add_billing():
	t = timezone.localtime(timezone.now())
	if t.day == 1:
		
		rows = Bed.objects.filter(bed_status__icontains='occupied')
		for row in rows:
			occupant = Occupant.objects.get(bed_id=row.id)
			recordcount = Bill.objects.filter(bill_date__year=t.year, bill_date__month=t.month,occupant_id = occupant.id).count()
			# print(row.id, occupant, recordcount)
			if (recordcount == 0):
				cursor = connections['default'].cursor()
				query = '''
						INSERT INTO dormdb.dormitory_bill(created_at, updated_at, bill_date, due_date, occupant_id, total)
						SELECT now(), now(), now(), DATE_ADD(now(), INTERVAL 8 DAY), occupant_id, SUM(amount) as `total bills` FROM dormdb.dormitory_bill_details
						WHERE YEAR(bill_date)=YEAR(now()) AND MONTH(bill_date)=MONTH(now()) GROUP by occupant_id;
						'''
				cursor.execute(query)

def add_rent_bill():
	t = timezone.localtime(timezone.now())
	# test if this is the 25th day of the month
	if t.day == 0:
		# searches all the occupied beds
		rows = Bed.objects.filter(bed_status__icontains='occupied')
		for row in rows:
			occupant = Occupant.objects.get(bed_id=row.id)
			reccnt = Bill_Details.objects.filter(bill_date__year=t.year, bill_date__month=t.month, service__service_name__icontains='Room Rental', occupant_id = occupant.id).count()
			if (reccnt == 0):
				cursor = connections['default'].cursor()
				query = f"INSERT INTO dormitory_bill_details(created_at, updated_at, bill_date, service_id, description, amount, occupant_id) VALUES(now(), now(), now(), 1,'Rental',{row.price},{occupant.id});"
				# print(query)
				cursor.execute(query)


