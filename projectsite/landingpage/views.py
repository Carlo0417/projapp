from atexit import register
from datetime import datetime
from typing import List

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
# from material import Field
from django.db.models import Sum

from django.db.models.functions import TruncMonth, TruncYear

from dormitory.models import Room, Bed, Service, Occupant, Person, Bill_Details, Payment, Demerit, OccupantDemerit, User, Admin
from django import forms
from dormitory.forms import RoomForm, ServiceForm, BedForm, OccupantForm, RegistrationForm, BillingForm
from dormitory.forms import OccupantFormEdit, BillingFormEdit, PaymentForm, DemeritForm, OccupantDemeritForm
from dormitory.forms import OccupantRenewForm, UserAvailServiceForm, UserLoginForm, AdminLoginForm, AdminForm
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
import csv

from decimal import Decimal

from django.db import connections


# @method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Room
    context_object_name = 'room'
    template_name = "landingpage/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_bed'] = Bed.objects.filter(bed_status__icontains='vacant').count()
        context['occupants'] = Occupant.objects.count()
        context['registered'] = Person.objects.filter(psu_email__isnull=False).count()
        context['complete'] = Person.objects.filter(reg_status__iexact="complete").count()
        context['incomplete'] = Person.objects.filter(reg_status__iexact="incomplete").count()
        context['local'] = Occupant.objects.filter(person_id__boarder_type__icontains='Local').count()
        context['foreign'] = Occupant.objects.filter(person_id__boarder_type__icontains='Foreign').count()
        context['maledorm_bed'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__iexact="Male Dorm").count()
        context['femaledorm_bed'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__iexact="Female Dorm").count()
        context['foreigndorm_bed'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__iexact="Foreign Dorm").count()
        
        # Students Gender Charts
        male_no = Person.objects.filter(gender="Male").count()
        male_no = int(male_no)
        # print('Male:', male_no)

        female_no = Person.objects.filter(gender="Female").count()
        female_no = int(female_no)
        # print('Female:', female_no)

        lgbt_no = Person.objects.filter(gender="LGBTQIA+").count()
        lgbt_no = int(lgbt_no)
        # print('LGBTQIA+:', lgbt_no)

        gender_list = ['Male', 'Female', 'LGBTQIA+']
        gender_number = [male_no, female_no, lgbt_no]

        context['gender_list'] = gender_list
        context['gender_number'] = gender_number

        
        # Monthly Registration Charts
        Jan = Person.objects.filter(created_at__icontains="2022-01").count()
        Jan = int(Jan)
        print('Jan:', Jan)

        Feb = Person.objects.filter(created_at__icontains="2022-02").count()
        Feb = int(Feb)
        print('Feb:', Feb)

        Mar = Person.objects.filter(created_at__icontains="2022-03").count()
        Mar = int(Mar)
        print('Mar:', Mar)

        Apr = Person.objects.filter(created_at__icontains="2022-04").count()
        Apr = int(Apr)
        print('Apr:', Apr)

        May = Person.objects.filter(created_at__icontains="2022-05").count()
        May = int(May)
        print('May:', May)

        Jun = Person.objects.filter(created_at__icontains="2022-06").count()
        Jun = int(Jun)
        print('Jun:', Jun)

        Jul = Person.objects.filter(created_at__icontains="2022-07").count()
        Jul = int(Jul)
        print('Jul:', Jul)

        Aug = Person.objects.filter(created_at__icontains="2022-08").count()
        Aug = int(Aug)
        print('Aug:', Aug)

        Sep = Person.objects.filter(created_at__icontains="2022-09").count()
        Sep = int(Sep)
        print('Sep:', Sep)

        Oct = Person.objects.filter(created_at__icontains="2022-10").count()
        Oct = int(Oct)
        print('Oct:', Oct)

        Nov = Person.objects.filter(created_at__icontains="2022-11").count()
        Nov = int(Nov)
        print('Nov:', Nov)

        Dec = Person.objects.filter(created_at__icontains="2022-12").count()
        Dec = int(Dec)
        print('Dec:', Dec)

        monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['monthly_list'] = monthly_list
        context['monthly_number'] = monthly_number
        
        return context

class AdminList(ListView):
    model = Admin
    context_object_name = 'admins'
    template_name = 'admin_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admins'] = Admin.objects.count()
        context['superadmins'] = Admin.objects.filter(admin_class__iexact="Super Administrator").count()
        context['otheradmins'] = Admin.objects.filter(~(Q(admin_class__iexact="Super Administrator"))).count() 
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(AdminList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("username")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("username").filter(Q(username__icontains=query) | Q(admin_class__icontains=query)
            | Q(firstname__icontains=query) | Q(lastname__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class AdminUpdateView(UpdateView):
    model = Admin
    fields = "__all__"
    context_object_name = 'admin'
    template_name = 'admin_update.html'
    success_url = "/admin_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# @method_decorator(login_required, name='dispatch')
class MaleDormVacantBedList(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'male_vacantbed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['male_vacant'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__iexact="Male Dorm").count()
        context['vacant_maledorm_bed'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__iexact="Male Dorm")
        return context


# @method_decorator(login_required, name='dispatch')
class FemaleDormVacantBedList(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'female_vacantbed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['female_vacant'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__iexact="Female Dorm").count()
        context['vacant_femaledorm_bed'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__iexact="Female Dorm")
        return context


# @method_decorator(login_required, name='dispatch')
class ForeignDormVacantBedList(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'foreign_vacantbed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['foreign_vacant'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__iexact="Foreign Dorm").count()
        context['vacant_foreigndorm_bed'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__iexact="Foreign Dorm")
        return context


# @method_decorator(login_required, name='dispatch')
class RoomList(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'room_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(RoomList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("floorlvl")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("room_name").filter(Q(room_name__icontains=query) | Q(floorlvl__icontains=query)
            | Q(dorm_name__icontains=query) | Q(description__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.count()
        context['maledorm'] = Room.objects.filter(dorm_name__iexact="Male Dorm").count()
        context['femaledorm'] = Room.objects.filter(dorm_name__iexact="Female Dorm").count()
        context['foreigndorm'] = Room.objects.filter(dorm_name__iexact="Foreign Dorm").count()
        return context


# @method_decorator(login_required, name='dispatch')
class RoomUpdateView(UpdateView):
    model = Room
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'room_update.html'
    success_url = "/room_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class ServiceList(ListView):
    model = Service
    context_object_name = 'service'
    template_name = 'service_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ServiceList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("service_name")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("service_name").filter(Q(service_name__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services']= Service.objects.all().exclude(service_name__iexact='Deposit').exclude(service_name__iexact='Advance').exclude(service_name__iexact='Dorm ID').count()
        context['available'] = Service.objects.filter(status__iexact="Available").exclude(service_name__iexact='Deposit').exclude(service_name__iexact='Advance').exclude(service_name__iexact='Dorm ID').count()
        context['notavailable'] = Service.objects.filter(status__iexact="Not Available").count()
        context['services_limit']= Service.objects.all().exclude(service_name__iexact='Deposit').exclude(service_name__iexact='Advance').exclude(service_name__iexact='Dorm ID')
        return context


# @method_decorator(login_required, name='dispatch')
class ServiceUpdateView(UpdateView):
    model = Service
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'service_update.html'
    success_url = "/service_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class BedList(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'bed_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beds'] = Bed.objects.count()
        context['vacant'] = Bed.objects.filter(bed_status__icontains='vacant').count()
        context['occupied'] = Bed.objects.filter(bed_status__icontains='occupied').count()
        context['vacant_maledorm_bed'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__iexact="Male Dorm")

        # cursor = connections['default'].cursor()
        # query = f"UPDATE dormitory_bed SET bed_status = 'Vacant' WHERE id NOT IN (SELECT bed_id FROM dormitory_occupant)"
        # cursor.execute(query)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BedList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("room_id")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("room_id").filter(Q(room__dorm_name__icontains=query) | Q(room__room_name__icontains=query)
            | Q(bed_code__icontains=query) | Q(price__icontains=query) | Q(bed_status__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class BedUpdateView(UpdateView):
    model = Bed
    fields = "__all__"
    context_object_name = 'bed'
    template_name = 'bed_update.html'
    success_url = "/bed_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class OccupantList(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'occupant_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['occupants'] = Occupant.objects.values('person__last_name').distinct().count()
        context['local'] = Occupant.objects.values('person__last_name').distinct().filter(person__boarder_type__iexact="Local").count() 
        context['foreign'] = Occupant.objects.values('person__last_name').distinct().filter(person__boarder_type__iexact="Foreign").count()
        context['renewal'] = Occupant.objects.values('person__last_name').annotate(Count('id')).order_by().filter(id__count__gt=1).count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(OccupantList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("person")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("person").filter(Q(person__last_name__icontains=query) | Q(person__first_name__icontains=query)
            | Q(bed__bed_code__icontains=query) | Q(person__boarder_type__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class OccupantUpdateView(UpdateView):
    model = Occupant
    # fields = ['person','bed','start_date','end_date']
    context_object_name = 'occupant'
    form_class = OccupantFormEdit
    template_name = 'occupant_update.html'
    success_url = "/occupant_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(f"Old Bed ID {self.object.bed_id}")
        return context
    
    def get_success_url(self, **kwargs):
        print(f"New Bed ID {self.object.bed_id}")
        cursor = connections['default'].cursor()
        query1 = f"UPDATE dormitory_bed SET bed_status = 'Occupied' WHERE `id` = {self.object.bed_id}"
        cursor.execute(query1)

        #Set Vacant those bed_id without occupant_id
        cursor = connections['default'].cursor()
        query2 = f"UPDATE dormitory_bed SET bed_status = 'Vacant' WHERE id NOT IN (SELECT bed_id FROM dormitory_occupant)"
        cursor.execute(query2)
        return "/occupant_list"


# @method_decorator(login_required, name='dispatch')
class OccupantView(UpdateView):
    model = Occupant
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'occupant_view.html'
    success_url = "/occupant_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fetch_first_three'] = Bill_Details.objects.filter(occupant=self.object.id)[0:3]
        context['billing_details'] = Bill_Details.objects.filter(occupant=self.object.id)[3:]
        context['total_bills_amount'] = Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['payment'] = Payment.objects.filter(occupant=self.object.id)
        context['total_payment_amount'] = Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['remaining_balance'] = (Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0)
        context['occupant_demerits'] = OccupantDemerit.objects.filter(occupant=self.object.id)
        return context
        

# @method_decorator(login_required, name='dispatch')
class OccupantViewBillingUpdate(UpdateView):
    model = Bill_Details
    # fields = "__all__"
    form_class = BillingFormEdit
    context_object_name = 'occupant'
    template_name = 'billing_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(f"ID {self.object.occupant_id}")
        return context

    def get_success_url(self):
        return reverse('OccupantView', kwargs={'pk': self.object.occupant_id})


# @method_decorator(login_required, name='dispatch')
class OccupantViewPaymentUpdate(UpdateView):
    model = Payment
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'payment_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(f"ID {self.object.occupant_id}")
        return context

    def get_success_url(self):
        return reverse('OccupantView', kwargs={'pk': self.object.occupant_id})


# @method_decorator(login_required, name='dispatch')
class OccupantViewDemeritUpdate(UpdateView):
    model = OccupantDemerit
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'occupant_demerit_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(f"ID {self.object.occupant_id}")
        return context

    def get_success_url(self):
        return reverse('OccupantView', kwargs={'pk': self.object.occupant_id})


# @method_decorator(login_required, name='dispatch')
class RegistrationList(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'registration_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registered'] = Person.objects.count()
        context['complete'] = Person.objects.filter(reg_status__iexact="complete").count()
        context['incomplete'] =  Person.objects.filter(reg_status__iexact="incomplete").count()

        cursor = connections['default'].cursor()
        query1 = f"UPDATE dormitory_person SET reg_status = 'Incomplete' WHERE Field1=0 or Field2=0 or Field3=0 or Field4=0 or Field5=0 or Field6=0 or Field7=0"
        cursor.execute(query1)
        
        cursor = connections['default'].cursor()
        query2 = f"UPDATE dormitory_person SET reg_status = 'Complete' WHERE Field1=1 and Field2=1 and Field3=1 and Field4=1 and Field5=1 and Field6=1 and Field7=1"
        cursor.execute(query2)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(RegistrationList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("psu_email")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("psu_email").filter(Q(psu_email__icontains=query) | Q(last_name__icontains=query) | Q(first_name__icontains=query) 
            | Q(program__icontains=query) | Q(boarder_type__icontains=query)| Q(reg_status__iexact=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class RegistrationUpdateView(UpdateView):
    model = Person
    fields = ['psu_email','last_name','first_name','middle_name','gender','boarder_type','program',
            'office_dept','contact_no','address','city','municipality','province','country',
            'guardian_first_name','guardian_last_name','guardian_email_address',
            'guardian_present_address','guardian_contact_no','Field1','Field2','Field3',
            'Field4','Field5','Field6','Field7']
    context_object_name = 'person'
    template_name = 'registration_update.html'
    success_url = "/registration_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class RegistrationRegView(UpdateView):
    model = Person
    fields = "__all__"
    context_object_name = 'person'
    template_name = 'registration_view.html'
    success_url = "/registration_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class BillingList(ListView):
    model = Bill_Details
    context_object_name = 'occupant'
    template_name = 'billing_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bills'] = Bill_Details.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BillingList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("occupant")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(service__service_name__icontains=query)
            | Q(description__icontains=query) | Q(amount__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class BillingUpdateView(UpdateView):
    model = Bill_Details
    # fields = "__all__"
    form_class = BillingFormEdit
    context_object_name = 'occupant'
    template_name = 'billing_update.html'
    success_url = "/billing_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class PaymentList(ListView):
    model = Payment
    context_object_name = 'payment'
    template_name = 'payment_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment'] = Payment.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(PaymentList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("occupant")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(payment_date__icontains=query)
            | Q(amount__icontains=query) | Q(receipt_no__iexact=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class PaymentUpdateView(UpdateView):
    model = Payment
    fields = "__all__"
    context_object_name = 'payment'
    template_name = 'payment_update.html'
    success_url = "/payment_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class DemeritList(ListView):
    model = Demerit
    context_object_name = 'demerit'
    template_name = 'demerit_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demerit'] = Demerit.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DemeritList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("demerit_points")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-demerit_points").filter(Q(demerit_name__icontains=query) 
            | Q(demerit_points__iexact=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class DemeritUpdateView(UpdateView):
    model = Demerit
    fields = "__all__"
    context_object_name = 'demerit'
    template_name = 'demerit_update.html'
    success_url = "/demerit_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class OccupantDemeritList(ListView):
    model = OccupantDemerit
    context_object_name = 'occupant'
    template_name = 'occupant_demerit_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['occupant_demerit'] = OccupantDemerit.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(OccupantDemeritList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("occupant")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(demerit_name__demerit_name__icontains=query)
            | Q(demerit_name__demerit_points__icontains=query) | Q(cur_date__icontains=query) | Q(remarks__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class OccupantDemeritUpdateView(UpdateView):
    model = OccupantDemerit
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'occupant_demerit_update.html'
    success_url = "/occupant_demerit_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class User_Dashboard(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = "user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class User_Services(ListView):
    model = Service
    context_object_name = 'services'
    template_name = "user_services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services_limit']= Service.objects.all().exclude(service_name__iexact='Deposit').exclude(service_name__iexact='Advance').exclude(service_name__iexact='Dorm ID')
        return context


# @method_decorator(login_required, name='dispatch')
class User_Profile(ListView):
    model = Person
    context_object_name = 'person'
    template_name = "user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class User_Account(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = "user_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @method_decorator(login_required, name='dispatch')
class User_Billing(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = "user_billing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# @method_decorator(login_required, name='dispatch')
class User_Notifications(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = "user_notifications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# @method_decorator(login_required, name='dispatch')
class NotificationList(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = "notification_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# @method_decorator(login_required, name='dispatch')
class OccupantAccounts(ListView):
    model = User
    context_object_name = 'users'
    template_name = "users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = User.objects.count()
        context['active'] = User.objects.filter(user_status__iexact="active").count()
        context['inactive'] = User.objects.filter(user_status__iexact="inactive").count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(OccupantAccounts, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("lastname")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("lastname").filter(Q(last_name__icontains=query) | Q(first_name__icontains=query) 
            | Q(username__icontains=query) | Q(user_status__iexact=query) | Q(recovery_email__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class OccupantAccountsUpdateView(UpdateView):
    model = User
    fields = ['username','password','security_question',
              'security_answer','recovery_email','user_status']
    context_object_name = 'user'
    template_name = 'users_update.html'
    success_url = "/users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



# ===================================================
# Functions for adding
# ===================================================
def add_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New room added successfully!')
            return redirect('RoomAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('RoomAdd')
    else:
        form = RoomForm()
        return render(request, 'room_add.html',  {'form': form})


def add_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New service added successfully!')
            return redirect('ServiceAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('ServiceAdd')
    else:
        form = ServiceForm()
        return render(request, 'service_add.html',  {'form': form})


def add_bed(request):
    if request.method == "POST":
        form = BedForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New bed added successfully!')
            return redirect('BedAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('BedAdd')
    else:
        form = BedForm()
        return render(request, 'bed_add.html',  {'form': form})


def add_occupant(request):
    if request.method == "POST":
        form = OccupantForm(request.POST)
        
        if form.is_valid():
            bed_id = request.POST.get("bed")
            occ = form.save(commit=False)
            occ.pk = None
            occ.bedPrice = Bed.objects.filter(pk=bed_id).values_list('price')
            print(request.POST)
            print(occ.bedPrice)
            occ.save()
        
            messages.success(request, 'New occupant added successfully!')

            # update BED: bed_status to occupied after adding occupant
            cursor = connections['default'].cursor()
            query1 = f"UPDATE dormitory_bed SET bed_status = 'Occupied' WHERE `id` = {bed_id}"
            cursor.execute(query1)

            person_id = request.POST.get("person")

            cursor = connections['default'].cursor()
            query2 = f"UPDATE dormitory_user SET user_status = 'active' WHERE person_id = '{person_id}'"
            cursor.execute(query2)

            #Add Billing to Occupant
            sample_instance = Person.objects.get(id=person_id)
            boarder_type = sample_instance.boarder_type

            occ_id = form.instance.id
            # print(boarder_type)
            # print(occ_id)

            person_id = request.POST.get("person")

            if boarder_type == "Local":
                cursor = connections['default'].cursor()
                query_deposit_local = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '1500', 9, now(), {occ_id}, '', '1')"
                cursor.execute(query_deposit_local)

                cursor = connections['default'].cursor()
                query_advance_local = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '1500', 10, now(), {occ_id}, '', '1')"
                cursor.execute(query_advance_local)

                cursor = connections['default'].cursor()
                query_dorm_id = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '150', 13, now(), {occ_id}, '', '1')"
                cursor.execute(query_dorm_id)

            elif boarder_type == "Foreign":
                cursor = connections['default'].cursor()
                query_deposit_local = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '4500', 11, now(), {occ_id}, '', '1')"
                cursor.execute(query_deposit_local)

                cursor = connections['default'].cursor()
                query_advance_local = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '4500', 12, now(), {occ_id}, '', '1')"
                cursor.execute(query_advance_local)

                cursor = connections['default'].cursor()
                query_dorm_id = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '150', 13, now(), {occ_id}, '', '1')"
                cursor.execute(query_dorm_id)

            return redirect('OccupantAdd')

        else:
            
            messages.error(request, 'Please complete the required field.')
            # print()
            return redirect('OccupantAdd')
    else:
        form = OccupantForm()
        return render(request, 'occupant_add.html',  {'form': form})


def add_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            last_name = form.cleaned_data.get('last_name')
            first_name = form.cleaned_data.get('first_name')
            psu_email = form.cleaned_data.get('psu_email')
            person_id = form.instance.id

            cursor = connections['default'].cursor()
            query = f"INSERT INTO dormitory_user VALUES('', now(), now(), '{last_name}', '{first_name}', '{psu_email}', '123456', '', '', '', 'inactive','{person_id}')"
            cursor.execute(query)
        
            messages.success(request, 'New student registered successfully!')
            return redirect('RegistrationAdd')

        else:
            messages.error(request, 'Please complete the required field/s.')
            # print()
            return redirect('RegistrationAdd')
    else:
        form = RegistrationForm()
        return render(request, 'registration_add.html',  {'form': form})


def add_billing(request):
    if request.method == "POST":
        form = BillingForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New bill added successfully!')
            return redirect('BillingAdd')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('BillingAdd')
    else:
        form = BillingForm()
        return render(request, 'billing_add.html',  {'form': form})


def add_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New payment added successfully!')
            return redirect('PaymentAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('PaymentAdd')
    else:
        form = PaymentForm()
        return render(request, 'payment_add.html',  {'form': form})


def add_demerit(request):
    if request.method == "POST":
        form = DemeritForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New demerit added successfully!')
            return redirect('DemeritAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('DemeritAdd')
    else:
        form = DemeritForm()
        return render(request, 'demerit_add.html',  {'form': form})


def add_occupant_demerit(request):
    if request.method == "POST":
        form = OccupantDemeritForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New demerit for occupant added successfully!')
            return redirect('OccupantDemeritAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('OccupantDemeritAdd')
    else:
        form = OccupantDemeritForm()
        return render(request, 'occupant_demerit_add.html',  {'form': form})


def add_bed(request):
    if request.method == "POST":
        form = BedForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New bed added successfully!')
            return redirect('BedAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('BedAdd')
    else:
        form = BedForm()
        return render(request, 'bed_add.html',  {'form': form})


def renew_occupant(request):
    if request.method == "POST":
        form = OccupantRenewForm(request.POST)
        
        if form.is_valid():
            bed_id = request.POST.get("bed")
            occ = form.save(commit=False)
            occ.pk = None
            occ.bedPrice = Bed.objects.filter(pk=bed_id).values_list('price')
            print(request.POST)
            print(occ.bedPrice)
            occ.save()
        
            messages.success(request, 'Occupant renewal added successfully!')

            # update BED: bed_status to occupied after adding occupant
            cursor = connections['default'].cursor()
            query = f"UPDATE dormitory_bed SET bed_status = 'Occupied' WHERE `id` = {bed_id}"
            cursor.execute(query)

            return redirect('OccupantRenew')

        else:
            
            messages.error(request, 'Please complete the required field.')
            # print()
            return redirect('OccupantRenew')
    else:
        form = OccupantRenewForm()
        return render(request, 'occupant_renew.html',  {'form': form})  

def avail_service(request):
    if request.method == "POST":
        form = UserAvailServiceForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service availed successfully!')
            return redirect('UserAvailService')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('UserAvailService')
    else:
        form = UserAvailServiceForm()
        return render(request, 'user_service_avail.html',  {'form': form})  

def user_logout_view(request):
    logout(request)
    return redirect("user_login")

def admin_logout_view(request):
    logout(request)
    return redirect("admin_login")

def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST) 
        if form.is_valid():
            UN = form.cleaned_data['username']
            PW = form.cleaned_data['password']

            cursor = connections['default'].cursor()
            query = f"SELECT username, password FROM dormitory_user WHERE username = '{UN}' AND password = '{PW}'"
            cursor.execute(query)
            test = cursor.execute(query)
            # print(test)

            for p in User.objects.raw('SELECT * FROM dormitory_user WHERE username = %s', [UN]):
             print(p)
            
            if(test == 0):
                return redirect('user_login')
            else:
                return redirect('UserDashboard')
              
    else:
        form = UserLoginForm()
        return render(request, 'user_login.html',  {'form': form})


def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST) 
        if form.is_valid():
            UN = form.cleaned_data['username']
            PW = form.cleaned_data['password']

            cursor = connections['default'].cursor()
            query = f"SELECT username, password FROM dormitory_admin WHERE username = '{UN}' AND password = '{PW}'"
            cursor.execute(query)
            test = cursor.execute(query)
            # print(test)
            
            if(test == 0):
                messages.error(request, 'Username or Password is incorrect')
                return redirect('admin_login')
            else:
                return redirect('home')

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

        if (username == "") or (password == ""):
            messages.error(request,"Either Username or Password is empty")
            return redirect('admin_login')
        
        elif (username == "") and (password == ""):
            messages.error(request,"Username and Password is empty")
            return redirect('admin_login')
              
    else:
        form = AdminLoginForm()
        return render(request, 'admin_login.html',  {'form': form})


def add_admin(request):
    if request.method == "POST":
        form = AdminForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New account for admin successfully!')
            return redirect('AdminAdd')

        else:
            messages.error(request, 'Please complete the required field/s.')
            # print()
            return redirect('AdminAdd')
    else:
        form = AdminForm()
        return render(request, 'admin_add.html',  {'form': form})


# ===================================================
# Functions for deleting
# ===================================================
def delete_occupant(request, id):
  occupant = Occupant.objects.get(id=id)
  occupant.delete()
  return HttpResponseRedirect(reverse('OccupantList'))

# def delete_bed(request, id):
#   bed = Bed.objects.get(id=id)
#   bed.delete()
#   return HttpResponseRedirect(reverse('BedList'))

def delete_reg(request, id):
  room = Person.objects.get(id=id)
  room.delete()
  return HttpResponseRedirect(reverse('RegistrationList'))

# def delete_demerit(request, id):
#   demerit = Demerit.objects.get(id=id)
#   demerit.delete()
#   return HttpResponseRedirect(reverse('DemeritList'))

def delete_user(request, id):
  occupant = User.objects.get(id=id)
  occupant.delete()
  return HttpResponseRedirect(reverse('OccupantAccounts'))



# ===================================================
# Functions for Exporting to PDF and EXCEL
# ===================================================
def venue_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4, bottomup=0)

    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    venues = Person.objects.all()

    lines = []

    for venue in venues:
        lines.append(venue.psu_email)
        lines.append(venue.last_name)
        lines.append(venue.first_name)
        lines.append(venue.middle_name)
        lines.append(venue.gender)
        lines.append(venue.boarder_type)
        lines.append(venue.program)
        lines.append(venue.office_dept)
        lines.append(" ")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venue.csv'

    writer = csv.writer(response)

    venues = Person.objects.all()

    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Middle Name', 'Gender',
                    'Boarder Type', 'Program', 'Office / Department'])

    lines = []

    for venue in venues:
        writer.writerow([venue.psu_email, venue.last_name, venue.first_name, venue.middle_name, 
                         venue.gender, venue.boarder_type, venue.program, venue.office_dept])

    response.writelines(lines)
    return response




