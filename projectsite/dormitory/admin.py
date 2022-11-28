from django.contrib import admin

# Register your models here.
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=("room_name","floorlvl","description",)
    search_fields = ("room_name","dorm_name",)
    list_filter = ("created_at",)


from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display=("service_name","status","base_amount",)
    search_fields = ("service_name","is_offered","base_amount",)
    list_filter = ("created_at",)


from .models import Bed

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display=("room_id","bed_code","bed_description","price",)
    search_fields = ("room_id","bed_code","bed_description","price",)
    list_filter = ("created_at",)


from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=("lastname","firstname","username","password",
    "security_question","security_answer","recovery_email")
    search_fields =("lastname","firstname","username","password",
    "security_question","security_answer","recovery_email")
    list_filter = ("created_at",)


from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display=("psu_email","gender","program","office_dept",
    "contact_no","address","city","municipality","province","country",
    "guardian_first_name","guardian_last_name","guardian_email_address",
    "guardian_present_address","guardian_contact_no","reg_status")
    search_fields =("psu_email","gender","program","office_dept",
    "contact_no","address","city","municipality","province","country",
    "guardian_first_name","guardian_last_name","guardian_email_address",
    "guardian_present_address","guardian_contact_no","reg_status")
    list_filter = ("created_at",)
    

from .models import BedPriceHistory

@admin.register(BedPriceHistory)
class BedPriceHistoryAdmin(admin.ModelAdmin):
    list_display=("bed","start_date","price")
    search_fields =("bed","start_date","price")
    list_filter = ("created_at",)


from .models import Occupant

@admin.register(Occupant)
class OccupantAdmin(admin.ModelAdmin):
    list_display=("person","bed","bedPrice","start_date","end_date")
    search_fields =("person","bed","bedPrice","start_date","end_date")
    list_filter = ("created_at",)


from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display=("bill_date","due_date","total","occupant")
    search_fields =("bill_date","due_date","total","occupant")
    list_filter = ("created_at",)


from .models import Bill_Details

@admin.register(Bill_Details)
class Bill_DetailsAdmin(admin.ModelAdmin):
    list_display=("service","description","amount")
    search_fields =("service","description","amount")
    list_filter = ("created_at",)


from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=("occupant","payment_date","amount","receipt_no")
    search_fields =("occupant","payment_date","amount","receipt_no")
    list_filter = ("created_at",)


from .models import Demerit

@admin.register(Demerit)
class DemeritAdmin(admin.ModelAdmin):
    list_display=("demerit_name","demerit_points")
    search_fields =("demerit_name","demerit_points")
    list_filter = ("created_at",)


from .models import OccupantDemerit

@admin.register(OccupantDemerit)
class Occupant_DemeritAdmin(admin.ModelAdmin):
    list_display=("occupant","demerit_name","cur_date","remarks")
    search_fields =("occupant","demerit_name","cur_date","remarks")
    list_filter = ("created_at",)