from django.conf import settings
from django.db import connections
from dormitory.models import Service, Bed, Occupant, Bill
import datetime

def schedule_api():
    
	print('hello')
	rows = Bed.objects.filter(bed_status__icontains='occupied')
	for row in rows:
		print(row.id)
		occupant = Occupant.objects.get(bed_id=row.id)
		print(occupant)
		cursor = connections['default'].cursor()
		query = f"INSERT INTO dormitory_bill(bill_date, due_date, total, occupant_id) VALUES(now(), now(), {row.price},{occupant});"
		print(query)
		# cursor.execute(query)
		
	# print('okay')


