from atexit import register
from django.utils import timezone
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

import xlwt

from django.db.models.functions import TruncMonth, TruncYear

from dormitory.models import Room, Bed, Service, Occupant, Person, Bill_Details, Payment, Demerit, OccupantDemerit, User, Admin
from django import forms
from dormitory.forms import RoomForm, ServiceForm, BedForm, OccupantForm, RegistrationForm, BillingForm
from dormitory.forms import OccupantFormEdit, OtherBillingForm, PaymentForm, DemeritForm, OccupantDemeritForm
from dormitory.forms import OccupantRenewForm, UserLoginForm, AdminLoginForm, AdminForm, AdminForgotPasswordForm1, AdminForgotPasswordForm2
from dormitory.forms import UserBillingForm, UserOtherBillingForm, UserForgotPasswordForm1, UserForgotPasswordForm2, AdminProfileForm

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

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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


        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = start_of_month.replace(month=start_of_month.month+1) - timezone.timedelta(microseconds=1)

        context['current_month_occupant'] = Occupant.objects.filter(created_at__range=(start_of_month, end_of_month)).count()

        
        # SELECT YEAR(dormitory_person.created_at), MONTH(dormitory_person.created_at),
        # COUNT(id) AS total_orders FROM dormitory_person GROUP BY MONTH(dormitory_person.created_at);

        # from django.db.models.functions import ExtractMonth, ExtractYear
        # from django.db.models import Count

        # total_orders = (
        #     Person.objects.annotate(month=ExtractMonth('created_at'))
        #     .annotate(year=ExtractYear('created_at'))
        #     .values('year', 'month')
        #     .annotate(total_orders=Count('id'))
        # )
        # print(total_orders)
        
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
        Jan = Person.objects.filter(created_at__icontains="2023-01").count()
        Jan = int(Jan)
        print('Jan:', Jan)

        Feb = Person.objects.filter(created_at__icontains="2023-02").count()
        Feb = int(Feb)
        print('Feb:', Feb)

        Mar = Person.objects.filter(created_at__icontains="2023-03").count()
        Mar = int(Mar)
        print('Mar:', Mar)

        Apr = Person.objects.filter(created_at__icontains="2023-04").count()
        Apr = int(Apr)
        print('Apr:', Apr)

        May = Person.objects.filter(created_at__icontains="2023-05").count()
        May = int(May)
        print('May:', May)

        Jun = Person.objects.filter(created_at__icontains="2023-06").count()
        Jun = int(Jun)
        print('Jun:', Jun)

        Jul = Person.objects.filter(created_at__icontains="2023-07").count()
        Jul = int(Jul)
        print('Jul:', Jul)

        Aug = Person.objects.filter(created_at__icontains="2023-08").count()
        Aug = int(Aug)
        print('Aug:', Aug)

        Sep = Person.objects.filter(created_at__icontains="2023-09").count()
        Sep = int(Sep)
        print('Sep:', Sep)

        Oct = Person.objects.filter(created_at__icontains="2023-10").count()
        Oct = int(Oct)
        print('Oct:', Oct)

        Nov = Person.objects.filter(created_at__icontains="2023-11").count()
        Nov = int(Nov)
        print('Nov:', Nov)

        Dec = Person.objects.filter(created_at__icontains="2023-12").count()
        Dec = int(Dec)
        print('Dec:', Dec)

        monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['monthly_list'] = monthly_list
        context['monthly_number'] = monthly_number


        # Monthly Occupant Charts
        Jan = Occupant.objects.filter(created_at__icontains="2023-01").count()
        Jan = int(Jan)
        print('Jan:', Jan)

        Feb = Occupant.objects.filter(created_at__icontains="2023-02").count()
        Feb = int(Feb)
        print('Feb:', Feb)

        Mar = Occupant.objects.filter(created_at__icontains="2023-03").count()
        Mar = int(Mar)
        print('Mar:', Mar)

        Apr = Occupant.objects.filter(created_at__icontains="2023-04").count()
        Apr = int(Apr)
        print('Apr:', Apr)

        May = Occupant.objects.filter(created_at__icontains="2023-05").count()
        May = int(May)
        print('May:', May)

        Jun = Occupant.objects.filter(created_at__icontains="2023-06").count()
        Jun = int(Jun)
        print('Jun:', Jun)

        Jul = Occupant.objects.filter(created_at__icontains="2023-07").count()
        Jul = int(Jul)
        print('Jul:', Jul)

        Aug = Occupant.objects.filter(created_at__icontains="2023-08").count()
        Aug = int(Aug)
        print('Aug:', Aug)

        Sep = Occupant.objects.filter(created_at__icontains="2023-09").count()
        Sep = int(Sep)
        print('Sep:', Sep)

        Oct = Occupant.objects.filter(created_at__icontains="2023-10").count()
        Oct = int(Oct)
        print('Oct:', Oct)

        Nov = Occupant.objects.filter(created_at__icontains="2023-11").count()
        Nov = int(Nov)
        print('Nov:', Nov)

        Dec = Occupant.objects.filter(created_at__icontains="2023-12").count()
        Dec = int(Dec)
        print('Dec:', Dec)

        occ_monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        occ_monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['occ_monthly_list'] = occ_monthly_list
        context['occ_monthly_number'] = occ_monthly_number
        
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

    def form_valid(self, form):
      messages.success(self.request, "Admin account was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())
    

# @method_decorator(login_required, name='dispatch')
class DashMaleVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'dash_male_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(DashMaleVacantBed, self).get_queryset(*args, **kwargs)
        qs = qs.filter(bed_status="Vacant", room__dorm_name__iexact="Male Dorm")
        qs = qs.order_by("created_at")
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(room__room_name__iexact=query) | Q(room__floorlvl__iexact=query) 
                | Q(bed_code__iexact=query) | Q(bed_description__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['male_vacant'] = Bed.objects.filter(bed_status__icontains='Vacant', room_id__dorm_name__iexact="Male Dorm").count()
        return context


# @method_decorator(login_required, name='dispatch')
class DashFemaleVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'dash_female_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(DashFemaleVacantBed, self).get_queryset(*args, **kwargs)
        qs = qs.filter(bed_status="Vacant", room__dorm_name__iexact="Female Dorm")
        qs = qs.order_by("created_at")
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(room__room_name__iexact=query) | Q(room__floorlvl__iexact=query) 
                | Q(bed_code__iexact=query) | Q(bed_description__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['female_vacant'] = Bed.objects.filter(bed_status__icontains='Vacant', room_id__dorm_name__iexact="Female Dorm").count()
        return context


# @method_decorator(login_required, name='dispatch')
class DashForeignVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'dash_foreign_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(DashForeignVacantBed, self).get_queryset(*args, **kwargs)
        qs = qs.filter(bed_status="Vacant", room__dorm_name__iexact="Foreign Dorm")
        qs = qs.order_by("created_at")
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(room__room_name__iexact=query) | Q(room__floorlvl__iexact=query) 
                | Q(bed_code__iexact=query) | Q(bed_description__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['foreign_vacant'] = Bed.objects.filter(bed_status__icontains='Vacant', room_id__dorm_name__iexact="Foreign Dorm").count()
        return context


# @method_decorator(login_required, name='dispatch')
class RoomList(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'room_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(RoomList, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(
            TotalBeds=Count('bed'), 
            TotalVacant=Count('bed', filter=Q(bed__bed_status='Vacant')),)
        qs = qs.order_by("created_at")
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(room_name__iexact=query) | Q(floorlvl__icontains=query) 
                | Q(dorm_name__icontains=query) | Q(description__icontains=query)
                | Q(bed__bed_status__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.count()
        context['maledorm'] = Room.objects.filter(dorm_name__iexact="Male Dorm").count()
        context['maledorm'] = Room.objects.filter(dorm_name__iexact="Male Dorm").count()
        context['femaledorm'] = Room.objects.filter(dorm_name__iexact="Female Dorm").count()
        context['foreigndorm'] = Room.objects.filter(dorm_name__iexact="Foreign Dorm").count()
        return context
    

# @method_decorator(login_required, name='dispatch')
class RoomListCard(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'room_list_card.html'
    paginate_by = 9

    def get_queryset(self, *args, **kwargs):
        qs = super(RoomListCard, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(
            TotalBeds=Count('bed'), 
            TotalVacant=Count('bed', filter=Q(bed__bed_status='Vacant')),
            TotalOccupied=Count('bed', filter=Q(bed__bed_status='Occupied')),
            TotalUnder=Count('bed', filter=Q(bed__bed_status='Under Maint.')),)
        qs = qs.order_by("created_at")
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(room_name__iexact=query) | Q(floorlvl__icontains=query) 
                | Q(dorm_name__icontains=query) | Q(description__icontains=query)
                | Q(bed__bed_status__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.count()
        context['maledorm'] = Room.objects.filter(dorm_name__iexact="Male Dorm").count()
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

    def form_valid(self, form):
      messages.success(self.request, "Room details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class RoomCardUpdateView(UpdateView):
    model = Room
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'room_update.html'
    success_url = "/room_list_card"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Room details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class ServiceList(ListView):
    model = Service
    context_object_name = 'service'
    template_name = 'service_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services']= Service.objects.all().exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Dorm ID').count()
        context['available'] = Service.objects.filter(status__iexact="Available").exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').count()
        context['notavailable'] = Service.objects.filter(status__iexact="Not Available").count()
        context['services_limit']= Service.objects.all().exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID')
    
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ServiceList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("service_name")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("service_name").filter(Q(service_name__icontains=query))
        return qs


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

    def form_valid(self, form):
      messages.success(self.request, "Service details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


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

        cursor = connections['default'].cursor()
        query = f"UPDATE dormitory_bed SET bed_status = 'Vacant' WHERE id NOT IN (SELECT bed_id FROM dormitory_occupant) AND bed_status = 'Occupied'"
        cursor.execute(query)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BedList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("room_id")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("room_id").filter(Q(room__dorm_name__iexact=query) | Q(room__room_name__icontains=query)
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

    def form_valid(self, form):
      messages.success(self.request, "Bed details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


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
        context['today'] = timezone.now()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(OccupantList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-created_at").filter(Q(person__last_name__icontains=query) | Q(person__first_name__icontains=query)
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
        query2 = f"UPDATE dormitory_bed SET bed_status = 'Vacant' WHERE id NOT IN (SELECT bed_id FROM dormitory_occupant) AND bed_status = 'Occupied'"
        cursor.execute(query2)
        return "/occupant_list"

    def form_valid(self, form):
      messages.success(self.request, "Occupant details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class OccupantView(UpdateView):
    model = Occupant
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'occupant_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fetch_first_three'] = Bill_Details.objects.filter(occupant=self.object.id)[:3]
        context['billing_details'] = Bill_Details.objects.filter(occupant=self.object.id)[3:]
        context['total_bills_amount'] = Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['payment'] = Payment.objects.filter(occupant=self.object.id)
        context['total_payment_amount'] = Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['remaining_balance'] = (Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0)
        context['occupant_demerits'] = OccupantDemerit.objects.filter(occupant=self.object.id)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Occupant details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())
        

# @method_decorator(login_required, name='dispatch')
class OccupantViewBillingUpdate(UpdateView):
    model = Bill_Details
    # fields = "__all__"
    form_class = BillingForm
    context_object_name = 'occupant'
    template_name = 'billing_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(f"ID {self.object.occupant_id}")
        return context

    def get_success_url(self):
        return reverse('OccupantView', kwargs={'pk': self.object.occupant_id})

    def form_valid(self, form):
      messages.success(self.request, "Occupant bill was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


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

    def form_valid(self, form):
      messages.success(self.request, "Occupant payment was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


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

    def form_valid(self, form):

        remarks = form.cleaned_data.get('remarks')
        new_remarks = form.cleaned_data['new_remarks']
        existing_remarks = remarks or ''
        remarks = existing_remarks + ' ' + new_remarks

        messages.success(self.request, "Occupant demerit was updated successfully!")
        super().form_valid(form)

        return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class OccMonthRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'occ_month_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
                                    dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
                                    dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
                                    FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
                                    INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id
                                    WHERE MONTH(start_date) = MONTH(CURRENT_DATE()) AND YEAR(start_date) = YEAR(CURRENT_DATE()) 
                                    ORDER BY dormitory_occupant.created_at DESC''')
        return context

# @method_decorator(login_required, name='dispatch')
class OccYearRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'occ_year_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
                                    dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
                                    dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
                                    FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
                                    INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id
                                    WHERE YEAR(start_date) = YEAR(CURRENT_DATE()) ORDER BY dormitory_occupant.created_at DESC''')
        return context


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
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-created_at").filter(Q(psu_email__icontains=query) | Q(last_name__icontains=query) | Q(first_name__icontains=query) 
            | Q(program__icontains=query) | Q(boarder_type__icontains=query)| Q(reg_status__iexact=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class RegMonthRep(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'reg_month_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = Person.objects.raw('SELECT * FROM dormitory_person WHERE MONTH(created_at) = MONTH(CURRENT_DATE()) AND YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')
        return context

# @method_decorator(login_required, name='dispatch')
class RegYearRep(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'reg_year_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = Person.objects.raw('SELECT * FROM dormitory_person WHERE YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')
        return context


# @method_decorator(login_required, name='dispatch')
class RegistrationUpdateView(UpdateView):
    model = Person
    context_object_name = 'person'
    form_class = RegistrationForm
    template_name = 'registration_update.html'
    success_url = "/registration_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Registration details was updated successfully!")
      super().form_valid(form)

      person_id = form.instance.id
      program = form.cleaned_data.get('program')

      if program == "Bachelor of Science in Social Work":
        cursor = connections['default'].cursor()
        query1 = f"UPDATE dormitory_person SET office_dept = 'Department of Behavioral Science' WHERE `id` = {person_id}"
        cursor.execute(query1)

      elif program == "Bachelor of Science in Psychology":
        cursor = connections['default'].cursor()
        query2 = f"UPDATE dormitory_person SET office_dept = 'Department of Behavioral Science' WHERE `id` = {person_id}"
        cursor.execute(query2)

      elif program == "Bachelor of Arts in Communication":
        cursor = connections['default'].cursor()
        query3 = f"UPDATE dormitory_person SET office_dept = 'Department of Behavioral Science' WHERE `id` = {person_id}"
        cursor.execute(query3)

      elif program == "Bachelor of Arts in Political Science":
        cursor = connections['default'].cursor()
        query4 = f"UPDATE dormitory_person SET office_dept = 'Department of Social Sciences' WHERE `id` = {person_id}"
        cursor.execute(query4)

      elif program == "Bachelor of Arts in Philippine Studies":
        cursor = connections['default'].cursor()
        query5 = f"UPDATE dormitory_person SET office_dept = 'Department of Foreign Language' WHERE `id` = {person_id}"
        cursor.execute(query5)

      elif program == "Bachelor of Science in Biology Major in Medical Biology":
        cursor = connections['default'].cursor()
        query6 = f"UPDATE dormitory_person SET office_dept = 'Bio-Physical Science Department' WHERE `id` = {person_id}"
        cursor.execute(query6)

      elif program == "Bachelor of Science in Marine Biology":
        cursor = connections['default'].cursor()
        query7 = f"UPDATE dormitory_person SET office_dept = 'Bio-Physical Science Department' WHERE `id` = {person_id}"
        cursor.execute(query7)

      elif program == "Bachelor of Science in Environmental Science":
        cursor = connections['default'].cursor()
        query8 = f"UPDATE dormitory_person SET office_dept = 'Bio-Physical Science Department' WHERE `id` = {person_id}"
        cursor.execute(query8)

      elif program == "Bachelor of Science in Information Technology":
        cursor = connections['default'].cursor()
        query9 = f"UPDATE dormitory_person SET office_dept = 'Computer Studies Department' WHERE `id` = {person_id}"
        cursor.execute(query9)

      elif program == "Bachelor of Science in Computer Science":
        cursor = connections['default'].cursor()
        query10 = f"UPDATE dormitory_person SET office_dept = 'Computer Studies Department' WHERE `id` = {person_id}"
        cursor.execute(query10)

      elif program == "Bachelor of Science in Physical Education":
        cursor = connections['default'].cursor()
        query11 = f"UPDATE dormitory_person SET office_dept = 'Department of Physical Education' WHERE `id` = {person_id}"
        cursor.execute(query11)

      elif program == "Bachelor of Science in Elementary Education":
        cursor = connections['default'].cursor()
        query12 = f"UPDATE dormitory_person SET office_dept = 'Department of Elementary Education' WHERE `id` = {person_id}"
        cursor.execute(query12)

      elif program == "Bachelor of Science in Secondary Education Major in Science":
        cursor = connections['default'].cursor()
        query13 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
        cursor.execute(query13)

      elif program == "Bachelor of Science in Secondary Education Major in Math":
        cursor = connections['default'].cursor()
        query14 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
        cursor.execute(query14)

      elif program == "Bachelor of Science in Secondary Education Major in English":
        cursor = connections['default'].cursor()
        query15 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
        cursor.execute(query15)

      elif program == "Bachelor of Science in Secondary Education Major in Filipino":
        cursor = connections['default'].cursor()
        query16 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
        cursor.execute(query16)

      elif program == "Bachelor of Science in Secondary Education Major in Social Studies":
        cursor = connections['default'].cursor()
        query17 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
        cursor.execute(query17)

      elif program == "Bachelor of Science in Secondary Education Major in Values":
        cursor = connections['default'].cursor()
        query18 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
        cursor.execute(query18)

      elif program == "Bachelor of Science in Accountancy":
        cursor = connections['default'].cursor()
        query19 = f"UPDATE dormitory_person SET office_dept = 'Department of Accountancy' WHERE `id` = {person_id}"
        cursor.execute(query19)

      elif program == "Bachelor of Science in Management Accountancy":
        cursor = connections['default'].cursor()
        query20 = f"UPDATE dormitory_person SET office_dept = 'Department of Accountancy' WHERE `id` = {person_id}"
        cursor.execute(query20)

      elif program == "Bachelor of Science in Entrepreneurship":
        cursor = connections['default'].cursor()
        query21 = f"UPDATE dormitory_person SET office_dept = 'Department of Marketing Management, Entrepreneurship, and Public Administration' WHERE `id` = {person_id}"
        cursor.execute(query21)

      elif program == "Bachelor of Science in Business Administration  Major in Marketing Management":
        cursor = connections['default'].cursor()
        query22 = f"UPDATE dormitory_person SET office_dept = 'Department of Marketing Management, Entrepreneurship, and Public Administration' WHERE `id` = {person_id}"
        cursor.execute(query22)

      elif program == "Bachelor of Science in Business Administration  Major in Public Administration":
        cursor = connections['default'].cursor()
        query23 = f"UPDATE dormitory_person SET office_dept = 'Department of Marketing Management, Entrepreneurship, and Public Administration' WHERE `id` = {person_id}"
        cursor.execute(query23)

      elif program == "Bachelor of Science in Business Administration  Major in Financial Management":
        cursor = connections['default'].cursor()
        query24 = f"UPDATE dormitory_person SET office_dept = 'Department of Financial Management, Human Resource Management, and Business Economics' WHERE `id` = {person_id}"
        cursor.execute(query24)

      elif program == "Bachelor of Science in Business Administration  Major in Human Resource Management":
        cursor = connections['default'].cursor()
        query25 = f"UPDATE dormitory_person SET office_dept = 'Department of Financial Management, Human Resource Management, and Business Economics' WHERE `id` = {person_id}"
        cursor.execute(query25)

      elif program == "Bachelor of Science in Business Administration  Major in Business Economics":
        cursor = connections['default'].cursor()
        query26 = f"UPDATE dormitory_person SET office_dept = 'Department of Financial Management, Human Resource Management, and Business Economics' WHERE `id` = {person_id}"
        cursor.execute(query26)

      elif program == "Bachelor of Science in Hospitality Management":
        cursor = connections['default'].cursor()
        query27 = f"UPDATE dormitory_person SET office_dept = 'Hospitality Management Department' WHERE `id` = {person_id}"
        cursor.execute(query27)

      elif program == "Track - Culinary Arts and Kitchen Management":
        cursor = connections['default'].cursor()
        query28 = f"UPDATE dormitory_person SET office_dept = 'Hospitality Management Department' WHERE `id` = {person_id}"
        cursor.execute(query28)

      elif program == "Bachelor of Science in Tourism Management":
        cursor = connections['default'].cursor()
        query29 = f"UPDATE dormitory_person SET office_dept = 'Tourism Management Department' WHERE `id` = {person_id}"
        cursor.execute(query29)

      elif program == "Track - Hotel,Resort, and Club Management":
        cursor = connections['default'].cursor()
        query30 = f"UPDATE dormitory_person SET office_dept = 'Tourism Management Department' WHERE `id` = {person_id}"
        cursor.execute(query30)

      elif program == "Bachelor of Science in Civil Engineering":
        cursor = connections['default'].cursor()
        query31 = f"UPDATE dormitory_person SET office_dept = 'Department of Civil Engineering' WHERE `id` = {person_id}"
        cursor.execute(query31)

      elif program == "Bachelor of Science in Mechanical Engineering":
        cursor = connections['default'].cursor()
        query32 = f"UPDATE dormitory_person SET office_dept = 'Department of Mechanical Engineering' WHERE `id` = {person_id}"
        cursor.execute(query32)

      elif program == "Bachelor of Science in Electrical Engineering":
        cursor = connections['default'].cursor()
        query33 = f"UPDATE dormitory_person SET office_dept = 'Department of Electrical Engineering' WHERE `id` = {person_id}"
        cursor.execute(query33)

      elif program == "Bachelor of Science in Petroleum Engineering":
        cursor = connections['default'].cursor()
        query34 = f"UPDATE dormitory_person SET office_dept = 'Department of Petroleum Engineering' WHERE `id` = {person_id}"
        cursor.execute(query34)
     
      elif program == "Bachelor of Science in Architecture":
        cursor = connections['default'].cursor()
        query35 = f"UPDATE dormitory_person SET office_dept = 'Department of Architecture' WHERE `id` = {person_id}"
        cursor.execute(query35)

      elif program == "Bachelor of Science in Nursing":
        cursor = connections['default'].cursor()
        query36 = f"UPDATE dormitory_person SET office_dept = 'Department of Nursing' WHERE `id` = {person_id}"
        cursor.execute(query36)

      elif program == "Diploma in Midwifery":
        cursor = connections['default'].cursor()
        query37 = f"UPDATE dormitory_person SET office_dept = 'Department of Midwifery' WHERE `id` = {person_id}"
        cursor.execute(query37)

      elif program == "Bachelor of Science in Midwifery":
        cursor = connections['default'].cursor()
        query38 = f"UPDATE dormitory_person SET office_dept = 'Department of Midwifery' WHERE `id` = {person_id}"
        cursor.execute(query38)

      elif program == "Bachelor of Science in Criminology":
        cursor = connections['default'].cursor()
        query39 = f"UPDATE dormitory_person SET office_dept = 'No Office / Department' WHERE `id` = {person_id}"
        cursor.execute(query39)

      return HttpResponseRedirect(self.get_success_url())


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

    def form_valid(self, form):
      messages.success(self.request, "Registration details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


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
    form_class = BillingForm
    context_object_name = 'occupant'
    template_name = 'billing_update.html'
    success_url = "/billing_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Billing details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


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

    def form_valid(self, form):
      messages.success(self.request, "Payment details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


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

    def form_valid(self, form):
      messages.success(self.request, "Demerit details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class OccupantDemeritList(ListView):
    model = OccupantDemerit
    context_object_name = 'occupant'
    template_name = 'occupant_demerit_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['occupant_demerit'] = OccupantDemerit.objects.count()
        cursor = connections['default'].cursor()
        query = f"UPDATE dormitory_occupantdemerit SET new_remarks = null "
        cursor.execute(query)
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
    fields = ['prev_remarks', 'new_remarks']
    context_object_name = 'occupant'
    template_name = 'occupant_demerit_update.html'
    success_url = "/occupant_demerit_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Occupant demerit was updated successfully!")
      super().form_valid(form)

      occ_id = form.instance.id
      pre_r = form.cleaned_data.get('prev_remarks')
      new_r = form.cleaned_data.get('new_remarks')
      
      indent = '     '
      in_new_r = indent + new_r

      prev_plus_new = pre_r +" \n \n " + in_new_r

      cursor = connections['default'].cursor()
      query = "UPDATE dormitory_occupantdemerit SET prev_remarks = %s WHERE id = %s"
      params = (prev_plus_new, occ_id)
      cursor.execute(query, params)
      return HttpResponseRedirect(self.get_success_url())
    

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

    def form_valid(self, form):
      messages.success(self.request, "Occupant account was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())



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

            cursor = connections['default'].cursor()
            query = f"UPDATE dormitory_bed SET bed_status = 'Vacant' WHERE id NOT IN (SELECT bed_id FROM dormitory_occupant) AND bed_status = 'Occupied'"
            cursor.execute(query)

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
            email = sample_instance.psu_email

            occ_id = form.instance.id
            # print(boarder_type)
            # print(occ_id)

            html_body = render_to_string("occ_email.html")

            message = EmailMultiAlternatives(
                subject='PSU Dorm Successful Occupant',
                body="mail testing",
                from_email='settings.EMAIL_HOST_USER',
                to=[email]
            )
            message.attach_alternative(html_body, "text/html")
            message.send(fail_silently=False)

            person_id = request.POST.get("person")

            if boarder_type == "Local":
                cursor = connections['default'].cursor()
                query_deposit_local = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '1500', 1, now(), {occ_id}, '1')"
                cursor.execute(query_deposit_local)

                cursor = connections['default'].cursor()
                query_advance_local = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '1500', 2, now(), {occ_id}, '1')"
                cursor.execute(query_advance_local)

                cursor = connections['default'].cursor()
                query_dorm_id = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '150', 3, now(), {occ_id}, '1')"
                cursor.execute(query_dorm_id)

            elif boarder_type == "Foreign":
                cursor = connections['default'].cursor()
                query_deposit_foreign = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '4500', 4, now(), {occ_id}, '1')"
                cursor.execute(query_deposit_foreign)

                cursor = connections['default'].cursor()
                query_advance_foreign = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '4500', 5, now(), {occ_id}, '1')"
                cursor.execute(query_advance_foreign)

                cursor = connections['default'].cursor()
                query_dorm_id = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '150', 3, now(), {occ_id}, '1')"
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

        email = request.POST['psu_email']

        html_body = render_to_string("reg_email.html")

        message = EmailMultiAlternatives(
            subject='PSU Dorm Registration',
            body="mail testing",
            from_email='settings.EMAIL_HOST_USER',
            to=[email]
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)


        form = RegistrationForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            form.save()
            last_name = form.cleaned_data.get('last_name')
            first_name = form.cleaned_data.get('first_name')
            psu_email = form.cleaned_data.get('psu_email')
            contact_no = form.cleaned_data.get('contact_no')
            print(contact_no)
            person_id = form.instance.id

            cursor = connections['default'].cursor()
            query = f"INSERT INTO dormitory_user VALUES('', now(), now(), '{last_name}', '{first_name}', '{psu_email}', '123456', '', '', '', 'inactive','{contact_no}', '{person_id}')"
            cursor.execute(query)

            program = form.cleaned_data.get('program')

            if program == "Bachelor of Science in Social Work":
                cursor = connections['default'].cursor()
                query1 = f"UPDATE dormitory_person SET office_dept = 'Department of Behavioral Science' WHERE `id` = {person_id}"
                cursor.execute(query1)

            elif program == "Bachelor of Science in Psychology":
                cursor = connections['default'].cursor()
                query2 = f"UPDATE dormitory_person SET office_dept = 'Department of Behavioral Science' WHERE `id` = {person_id}"
                cursor.execute(query2)

            elif program == "Bachelor of Arts in Communication":
                cursor = connections['default'].cursor()
                query3 = f"UPDATE dormitory_person SET office_dept = 'Department of Behavioral Science' WHERE `id` = {person_id}"
                cursor.execute(query3)

            elif program == "Bachelor of Arts in Political Science":
                cursor = connections['default'].cursor()
                query4 = f"UPDATE dormitory_person SET office_dept = 'Department of Social Sciences' WHERE `id` = {person_id}"
                cursor.execute(query4)

            elif program == "Bachelor of Arts in Philippine Studies":
                cursor = connections['default'].cursor()
                query5 = f"UPDATE dormitory_person SET office_dept = 'Department of Foreign Language' WHERE `id` = {person_id}"
                cursor.execute(query5)

            elif program == "Bachelor of Science in Biology Major in Medical Biology":
                cursor = connections['default'].cursor()
                query6 = f"UPDATE dormitory_person SET office_dept = 'Bio-Physical Science Department' WHERE `id` = {person_id}"
                cursor.execute(query6)

            elif program == "Bachelor of Science in Marine Biology":
                cursor = connections['default'].cursor()
                query7 = f"UPDATE dormitory_person SET office_dept = 'Bio-Physical Science Department' WHERE `id` = {person_id}"
                cursor.execute(query7)

            elif program == "Bachelor of Science in Environmental Science":
                cursor = connections['default'].cursor()
                query8 = f"UPDATE dormitory_person SET office_dept = 'Bio-Physical Science Department' WHERE `id` = {person_id}"
                cursor.execute(query8)

            elif program == "Bachelor of Science in Information Technology":
                cursor = connections['default'].cursor()
                query9 = f"UPDATE dormitory_person SET office_dept = 'Computer Studies Department' WHERE `id` = {person_id}"
                cursor.execute(query9)

            elif program == "Bachelor of Science in Computer Science":
                cursor = connections['default'].cursor()
                query10 = f"UPDATE dormitory_person SET office_dept = 'Computer Studies Department' WHERE `id` = {person_id}"
                cursor.execute(query10)

            elif program == "Bachelor of Science in Physical Education":
                cursor = connections['default'].cursor()
                query11 = f"UPDATE dormitory_person SET office_dept = 'Department of Physical Education' WHERE `id` = {person_id}"
                cursor.execute(query11)

            elif program == "Bachelor of Science in Elementary Education":
                cursor = connections['default'].cursor()
                query12 = f"UPDATE dormitory_person SET office_dept = 'Department of Elementary Education' WHERE `id` = {person_id}"
                cursor.execute(query12)

            elif program == "Bachelor of Science in Secondary Education Major in Science":
                cursor = connections['default'].cursor()
                query13 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query13)

            elif program == "Bachelor of Science in Secondary Education Major in Math":
                cursor = connections['default'].cursor()
                query14 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query14)

            elif program == "Bachelor of Science in Secondary Education Major in English":
                cursor = connections['default'].cursor()
                query15 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query15)

            elif program == "Bachelor of Science in Secondary Education Major in Filipino":
                cursor = connections['default'].cursor()
                query16 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query16)

            elif program == "Bachelor of Science in Secondary Education Major in Social Studies":
                cursor = connections['default'].cursor()
                query17 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query17)

            elif program == "Bachelor of Science in Secondary Education Major in Values":
                cursor = connections['default'].cursor()
                query18 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query18)

            elif program == "Bachelor of Science in Accountancy":
                cursor = connections['default'].cursor()
                query19 = f"UPDATE dormitory_person SET office_dept = 'Department of Accountancy' WHERE `id` = {person_id}"
                cursor.execute(query19)

            elif program == "Bachelor of Science in Management Accountancy":
                cursor = connections['default'].cursor()
                query20 = f"UPDATE dormitory_person SET office_dept = 'Department of Accountancy' WHERE `id` = {person_id}"
                cursor.execute(query20)

            elif program == "Bachelor of Science in Entrepreneurship":
                cursor = connections['default'].cursor()
                query21 = f"UPDATE dormitory_person SET office_dept = 'Department of Marketing Management, Entrepreneurship, and Public Administration' WHERE `id` = {person_id}"
                cursor.execute(query21)

            elif program == "Bachelor of Science in Business Administration  Major in Marketing Management":
                cursor = connections['default'].cursor()
                query22 = f"UPDATE dormitory_person SET office_dept = 'Department of Marketing Management, Entrepreneurship, and Public Administration' WHERE `id` = {person_id}"
                cursor.execute(query22)

            elif program == "Bachelor of Science in Business Administration  Major in Public Administration":
                cursor = connections['default'].cursor()
                query23 = f"UPDATE dormitory_person SET office_dept = 'Department of Marketing Management, Entrepreneurship, and Public Administration' WHERE `id` = {person_id}"
                cursor.execute(query23)

            elif program == "Bachelor of Science in Business Administration  Major in Financial Management":
                cursor = connections['default'].cursor()
                query24 = f"UPDATE dormitory_person SET office_dept = 'Department of Financial Management, Human Resource Management, and Business Economics' WHERE `id` = {person_id}"
                cursor.execute(query24)

            elif program == "Bachelor of Science in Business Administration  Major in Human Resource Management":
                cursor = connections['default'].cursor()
                query25 = f"UPDATE dormitory_person SET office_dept = 'Department of Financial Management, Human Resource Management, and Business Economics' WHERE `id` = {person_id}"
                cursor.execute(query25)

            elif program == "Bachelor of Science in Business Administration  Major in Business Economics":
                cursor = connections['default'].cursor()
                query26 = f"UPDATE dormitory_person SET office_dept = 'Department of Financial Management, Human Resource Management, and Business Economics' WHERE `id` = {person_id}"
                cursor.execute(query26)

            elif program == "Bachelor of Science in Hospitality Management":
                cursor = connections['default'].cursor()
                query27 = f"UPDATE dormitory_person SET office_dept = 'Hospitality Management Department' WHERE `id` = {person_id}"
                cursor.execute(query27)

            elif program == "Track - Culinary Arts and Kitchen Management":
                cursor = connections['default'].cursor()
                query28 = f"UPDATE dormitory_person SET office_dept = 'Hospitality Management Department' WHERE `id` = {person_id}"
                cursor.execute(query28)

            elif program == "Bachelor of Science in Tourism Management":
                cursor = connections['default'].cursor()
                query29 = f"UPDATE dormitory_person SET office_dept = 'Tourism Management Department' WHERE `id` = {person_id}"
                cursor.execute(query29)

            elif program == "Track - Hotel,Resort, and Club Management":
                cursor = connections['default'].cursor()
                query30 = f"UPDATE dormitory_person SET office_dept = 'Tourism Management Department' WHERE `id` = {person_id}"
                cursor.execute(query30)

            elif program == "Bachelor of Science in Civil Engineering":
                cursor = connections['default'].cursor()
                query31 = f"UPDATE dormitory_person SET office_dept = 'Department of Civil Engineering' WHERE `id` = {person_id}"
                cursor.execute(query31)

            elif program == "Bachelor of Science in Mechanical Engineering":
                cursor = connections['default'].cursor()
                query32 = f"UPDATE dormitory_person SET office_dept = 'Department of Mechanical Engineering' WHERE `id` = {person_id}"
                cursor.execute(query32)

            elif program == "Bachelor of Science in Electrical Engineering":
                cursor = connections['default'].cursor()
                query33 = f"UPDATE dormitory_person SET office_dept = 'Department of Electrical Engineering' WHERE `id` = {person_id}"
                cursor.execute(query33)

            elif program == "Bachelor of Science in Petroleum Engineering":
                cursor = connections['default'].cursor()
                query34 = f"UPDATE dormitory_person SET office_dept = 'Department of Petroleum Engineering' WHERE `id` = {person_id}"
                cursor.execute(query34)

            elif program == "Bachelor of Science in Architecture":
                cursor = connections['default'].cursor()
                query35 = f"UPDATE dormitory_person SET office_dept = 'Department of Architecture' WHERE `id` = {person_id}"
                cursor.execute(query35)

            elif program == "Bachelor of Science in Nursing":
                cursor = connections['default'].cursor()
                query36 = f"UPDATE dormitory_person SET office_dept = 'Department of Nursing' WHERE `id` = {person_id}"
                cursor.execute(query36)

            elif program == "Diploma in Midwifery":
                cursor = connections['default'].cursor()
                query37 = f"UPDATE dormitory_person SET office_dept = 'Department of Midwifery' WHERE `id` = {person_id}"
                cursor.execute(query37)

            elif program == "Bachelor of Science in Midwifery":
                cursor = connections['default'].cursor()
                query38 = f"UPDATE dormitory_person SET office_dept = 'Department of Midwifery' WHERE `id` = {person_id}"
                cursor.execute(query38)

            elif program == "Bachelor of Science in Criminology":
                cursor = connections['default'].cursor()
                query39 = f"UPDATE dormitory_person SET office_dept = 'No Office / Department' WHERE `id` = {person_id}"
                cursor.execute(query39)

        
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

            service = form.cleaned_data['service']
            quantity = form.cleaned_data['quantity']
            
            price = Service.objects.filter(service_name= service).first()
            bill_id = form.instance.id

            total_amount = price.base_amount * quantity

            cursor = connections['default'].cursor()
            query = f"UPDATE dormitory_bill_details SET amount = '{total_amount}' WHERE `id` = {bill_id}"
            cursor.execute(query)
            
            messages.success(request, 'New bill added successfully!')
            return redirect('BillingAdd')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('BillingAdd')
    else:
        form = BillingForm()
        return render(request, 'billing_add.html',  {'form': form})


def other_add_billing(request):
    if request.method == "POST":
        form = OtherBillingForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'New bill added successfully!')
            return redirect('other-add')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('other-add')
    else:
        form = OtherBillingForm()
        return render(request, 'others_billing_add.html',  {'form': form})

def other_add(request):
    return render(request, 'billing_list/other_billing_add.html', {} )


def other_update_billing(request, billing_id):
    billing = Bill_Details.objects.get(pk=billing_id)
    form = OtherBillingForm(request.POST or None, instance=billing)
    if form.is_valid():
        form.save()
        messages.success(request, 'Billing details was updated successfully!')
        return redirect('BillingList')
    return render (request, 'others_billing_update.html', {'billing': billing, 'form': form})


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

# ===================================================
# The Show Begins
# ===================================================
x = ""

def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST) 
        if form.is_valid():
            
            UN = form.cleaned_data['username']
            PW = form.cleaned_data['password']
            user = form.instance.id

            cursor = connections['default'].cursor()
            query = f"SELECT username, password FROM dormitory_user WHERE username = '{UN}' AND password = '{PW}' AND user_status='Active'"
            cursor.execute(query)
            test1 = cursor.execute(query)

            cursor = connections['default'].cursor()
            query = f"SELECT username, password FROM dormitory_user WHERE username = '{UN}' AND password = '{PW}' AND user_status='Inactive'"
            cursor.execute(query)
            test2 = cursor.execute(query)


            if(test1 != 0):
                global x
                x = request.session['username'] = UN
                print(x)
                return redirect('UserDashboard')

            elif (test2 != 0):
                messages.error(request, 'Account is Deactivated!')
                return redirect('user_login')

            else:
                messages.error(request, 'Username or Password is incorrect!')
                return redirect('user_login')       

        else:
            messages.error(request, 'Username or Password field is empty!')
            return redirect('user_login')
    else:
        form = UserLoginForm()
        return render(request, 'user_login.html',  {'form': form})
        

def user_logout_view(request):
    logout(request)
    return redirect("user_login")


# @method_decorator(login_required, name='dispatch')
class User_Dashboard(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = "user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['per'] = Person.objects.filter(Q(psu_email=x)).values().order_by('-id')[:1]
        context ['occ'] = Occupant.objects.filter(Q(person__psu_email=x)).values('person__boarder_type', 'bed__bed_code', 'bed__room__room_name', 'bed__room__dorm_name').order_by('-id')[:1]
        return context


# @method_decorator(login_required, name='dispatch')
class User_Account(ListView):
    model = User
    context_object_name = 'user'
    template_name = "user_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global x
        context ['acc'] = User.objects.filter(Q(username=x)).values()
        return context


# @method_decorator(login_required, name='dispatch')
class User_AccountUpdateView(UpdateView):
    model = User
    fields = ['password','security_question', 'security_answer','recovery_email']
    context_object_name = 'user'
    template_name = 'user_account_update.html'
    success_url = "/user_account"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Your Account Information was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class User_Profile(ListView):
    model = Person
    context_object_name = 'person'
    template_name = "user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global x
        context ['prof'] = Person.objects.filter(Q(psu_email=x)).values()
        return context

# @method_decorator(login_required, name='dispatch')
class User_Billing(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = "user_billing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global x
        context ['cont'] = Occupant.objects.filter(Q(person__psu_email=x)).values('id', 'bed__bed_code', 'bed__bed_description', 'bedPrice', 'bed__room__room_name', 'bed__room__floorlvl', 'bed__room__dorm_name', 'start_date', 'end_date').order_by('-created_at')
        return context


# @method_decorator(login_required, name='dispatch')
class User_Contract_View(UpdateView):
    model = Occupant
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'user_contract_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global x
        
        context ['contract'] = Occupant.objects.filter(Q(person__psu_email=x, id=self.object.id)).values('id','bed__bed_code', 'person__boarder_type', 'bed__bed_description', 'bedPrice', 'bed__room__room_name', 'bed__room__floorlvl', 'bed__room__dorm_name', 'start_date', 'end_date').order_by('-created_at')
        context['fetch_first_three'] = Bill_Details.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).values('bill_date', 'service__service_name', 'amount')[0:3]
        context['billing_details'] = Bill_Details.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).values('bill_date', 'service__service_name', 'quantity', 'amount')[3:]
        context['total_bills_amount'] = Bill_Details.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).aggregate(Sum('amount'))['amount__sum'] or 0
        context['payment'] = Payment.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).values('payment_date', 'amount', 'receipt_no')
        context['total_payment_amount'] = Payment.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).aggregate(Sum('amount'))['amount__sum'] or 0
        context['remaining_balance'] = (Bill_Details.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0)
        return context


# @method_decorator(login_required, name='dispatch')
class User_Services(ListView):
    model = Service
    context_object_name = 'services'
    template_name = "user_services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['services_limit'] = Service.objects.filter(status__iexact='Available').exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others')
        return context

def user_add_billing(request):
    if request.method == "POST":
        form = UserBillingForm(request.POST)

        if form.is_valid():
            form.save()

            bill_id = form.instance.id

            occ = Occupant.objects.filter(person__psu_email=x).exclude(end_date__lte=timezone.now().date()).order_by('-created_at').first().id
            # print(occ)

            cursor1 = connections['default'].cursor()
            query1 = f"UPDATE dormitory_bill_details SET occupant_id ='{occ}' WHERE `id` = {bill_id}"
            cursor1.execute(query1)

            service = form.cleaned_data['service']
            quantity = form.cleaned_data['quantity']
            
            price = Service.objects.filter(service_name=service).first()

            total_amount = price.base_amount * quantity

            cursor = connections['default'].cursor()
            query = f"UPDATE dormitory_bill_details SET amount ='{total_amount}' WHERE `id` = {bill_id}"
            cursor.execute(query)
            
            messages.success(request, 'Service availed successfully!')
            return redirect('UserAvailService')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('UserAvailService')
    else:
        form = UserBillingForm()
        return render(request, 'user_service_avail.html',  {'form': form})


def user_other_add_billing(request):
    if request.method == "POST":
        form = UserOtherBillingForm(request.POST)
        if form.is_valid():
            form.save()

            bill_id = form.instance.id

            occ = Occupant.objects.filter(person__psu_email=x).exclude(end_date__lte=timezone.now().date()).order_by('-created_at').first().id
            # print(occ)

            cursor1 = connections['default'].cursor()
            query1 = f"UPDATE dormitory_bill_details SET occupant_id ='{occ}' WHERE `id` = {bill_id}"
            cursor1.execute(query1)

            amount = form.cleaned_data['amount']
            quantity = form.cleaned_data['quantity']
            
            total_amount = amount * quantity

            cursor = connections['default'].cursor()
            query = f"UPDATE dormitory_bill_details SET amount ='{total_amount}' WHERE `id` = {bill_id}"
            cursor.execute(query)
            
            messages.success(request, 'Service availed successfully!')
            return redirect('user_other_add')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('user_other_add')
    else:
        form = UserOtherBillingForm()
        return render(request, 'user_service_others.html',  {'form': form})

def user_other_add(request):
    return render(request, 'user_services/user_service_others.html', {} )

y = ""

def user_forgot_password_form(request):
    if request.method == 'POST':
        form = UserForgotPasswordForm1(request.POST) 
        if form.is_valid():
            
            Forgot_UserName = form.cleaned_data['username']

            cursor = connections['default'].cursor()
            query = f"SELECT username, password FROM dormitory_user WHERE username = '{Forgot_UserName}' AND user_status='Active'"
            cursor.execute(query)
            test1 = cursor.execute(query)

            cursor = connections['default'].cursor()
            query = f"SELECT username, password FROM dormitory_user WHERE username = '{Forgot_UserName}' AND user_status='Inactive'"
            cursor.execute(query)
            test2 = cursor.execute(query)


            if(test1 != 0):
                global y
                y = request.session['username'] = Forgot_UserName
                return redirect('user_security_question')

            elif (test2 != 0):
                messages.error(request, 'Account is Deactivated!')
                return redirect('user_forgot_password')

            else:
                messages.error(request, 'Username is incorrect!')
                return redirect('user_forgot_password')       

        else:
            messages.error(request, 'Username field is empty!')
            return redirect('user_forgot_password')
    else:
        form = UserForgotPasswordForm1()
        return render(request, 'user_forgot_password.html',  {'form': form})


def user_security_question_form(request):
    
    global y

    occ = User.objects.filter(username=y)

    # Check if the occ queryset is not empty
    if occ.exists():
        # Retrieve the first Occupant object in the queryset
        occ = occ.first()
        # Check if the security question is null
        if occ.security_question is None:
            # Redirect to the login page
            return redirect('user_login')

    if request.method == 'POST':
        form = UserForgotPasswordForm2(request.POST)

        if form.is_valid():
            
            sec_ans = form.cleaned_data['security_answer']

            if sec_ans == occ.security_answer:
                return redirect('user_show_password') 

            elif sec_ans is None:
                messages.error(request, 'Security answer field is empty!')
                return redirect('user_security_question')   
            
            else:
                messages.error(request, 'Security answer is incorrect!')
                return redirect('user_security_question')    

        else:
            messages.error(request, 'Security answer field is empty!')
            return redirect('user_security_question')
    else:
        security_question = occ.security_question
        form = UserForgotPasswordForm2()
        return render(request, 'user_security_question.html',  {'form': form, 'security_question': security_question})

def user_show_password_form(request):
    global y

    # Retrieve the Occupant object for the given email address
    occ = User.objects.get(username=y)
    # Retrieve the password for the Occupant object
    password = occ.password
    return render(request, 'user_show_password.html', {'password': password})

# ===================================================
# end of The Show Begins
# ===================================================
xy = ""

ac = ""

dm = ""

sa = ""

def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST) 
        if form.is_valid():
            UN = form.cleaned_data['username']
            PW = form.cleaned_data['password']

            cursor = connections['default'].cursor()
            query1 = f"SELECT username, password FROM dormitory_admin WHERE username = '{UN}' AND password = '{PW}' AND admin_class = 'Front Desk'"
            cursor.execute(query1)
            test1 = cursor.execute(query1)

            cursor = connections['default'].cursor()
            query2 = f"SELECT username, password FROM dormitory_admin WHERE username = '{UN}' AND password = '{PW}' AND admin_class = 'Accounting Staff'"
            cursor.execute(query2)
            test2 = cursor.execute(query2)

            cursor = connections['default'].cursor()
            query3 = f"SELECT username, password FROM dormitory_admin WHERE username = '{UN}' AND password = '{PW}' AND admin_class = 'Dorm Manager'"
            cursor.execute(query3)
            test3 = cursor.execute(query3)

            cursor = connections['default'].cursor()
            query4 = f"SELECT username, password FROM dormitory_admin WHERE username = '{UN}' AND password = '{PW}' AND admin_class = 'Super Administrator'"
            cursor.execute(query4)
            test4 = cursor.execute(query4)
            # print(test)
            
            if(test1 != 0):
                global xy
                xy = request.session['username'] = UN
                return redirect('frontdesk_home')

            elif(test2 != 0):
                global ac
                ac = request.session['username'] = UN
                return redirect('accounting_home')

            elif(test3 != 0):
                global dm
                dm = request.session['username'] = UN
                return redirect('dormmanager_home')

            elif(test4 != 0):
                global sa
                sa = request.session['username'] = UN
                return redirect('home')

            else:
                messages.error(request, 'Username or Password is incorrect')
                return redirect('admin_login')

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


def admin_logout_view(request):
    logout(request)
    return redirect("admin_login")


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

a_y = ""

def admin_forgot_password_form(request):
    if request.method == 'POST':
        form = AdminForgotPasswordForm1(request.POST) 
        if form.is_valid():
            
            Forgot_AdminName = form.cleaned_data['username']

            cursor = connections['default'].cursor()
            query = f"SELECT username FROM dormitory_admin WHERE username = '{Forgot_AdminName}'"
            cursor.execute(query)
            test1 = cursor.execute(query)

            if(test1 != 0):
                global a_y
                a_y = request.session['username'] = Forgot_AdminName
                return redirect('admin_security_question')

            else:
                messages.error(request, 'Username is incorrect!')
                return redirect('admin_forgot_password')       

        else:
            messages.error(request, 'Username field is empty!')
            return redirect('admin_forgot_password')
    else:
        form = AdminForgotPasswordForm1()
        return render(request, 'admin_forgot_password.html',  {'form': form})


def admin_security_question_form(request):
    
    global a_y

    ad = Admin.objects.filter(username=a_y)

    # Check if the occ queryset is not empty
    if ad.exists():
        # Retrieve the first Occupant object in the queryset
        ad = ad.first()
        # Check if the security question is null
        if ad.security_question is None:
            # Redirect to the login page
            return redirect('admin_login')

    if request.method == 'POST':
        form = AdminForgotPasswordForm2(request.POST)

        if form.is_valid():
            
            sec_ans = form.cleaned_data['security_answer']

            if sec_ans == ad.security_answer:
                return redirect('admin_show_password') 

            elif sec_ans is None:
                messages.error(request, 'Security answer field is empty!')
                return redirect('admin_security_question')   
            
            else:
                messages.error(request, 'Security answer is incorrect!')
                return redirect('admin_security_question')    

        else:
            messages.error(request, 'Security answer field is empty!')
            return redirect('admin_security_question')
    else:
        security_question = ad.security_question
        form = AdminForgotPasswordForm2()
        return render(request, 'admin_security_question.html',  {'form': form, 'security_question': security_question})

def admin_show_password_form(request):
    global a_y

    # Retrieve the Occupant object for the given email address
    ad = Admin.objects.get(username=a_y)
    # Retrieve the password for the Occupant object
    password = ad.password
    return render(request, 'admin_show_password.html', {'password': password})
# ===================================================
# Functions for deleting
# ===================================================
def delete_occupant(request, id):
  occupant = Occupant.objects.get(id=id)
  occupant.delete()
  return HttpResponseRedirect(reverse('OccupantList'))

def delete_bed(request, id):
  bed = Bed.objects.get(id=id)
  bed.delete()
  return HttpResponseRedirect(reverse('BedList'))

def delete_room(request, id):
  room = Room.objects.get(id=id)
  room.delete()
  return HttpResponseRedirect(reverse('RoomList'))

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
from django.template.loader import get_template
from xhtml2pdf import pisa

def RegPDF(request, pk):
    reg_person = Person.objects.get(id=pk)
    template_path = 'reg_pdf.html'
    context = {
        'reg_person': reg_person,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Registration Information.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def OccPDF(request, pk):
    occ_person = Occupant.objects.get(id=pk)
    table1 = Bill_Details.objects.filter(occupant=pk)[0:3]
    table2 = Bill_Details.objects.filter(occupant=pk)[3:]
    table3 = Payment.objects.filter(occupant=pk)
    total_bills_amount = Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    payment = Payment.objects.filter(occupant=pk)
    total_payment_amount = Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_balance = (Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0)
    table4 = OccupantDemerit.objects.filter(occupant=pk)
    template_path = 'occ_pdf.html'

    context = {
        'occ_person': occ_person,
        'table1': table1,
        'table2': table2,
        'table3': table3,
        'total_bills_amount': total_bills_amount,
        'payment': payment,
        'total_payment_amount': total_payment_amount,
        'remaining_balance': remaining_balance,
        'table4': table4,
    }
 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Occupant Information.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# CSV for Registration
def reg_all_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Registration Report.csv'

    writer = csv.writer(response)

    reg_all = Person.objects.raw('SELECT * FROM dormitory_person ORDER BY created_at DESC')


    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Middle Name', 'Gender', 'Boarder Type', 'Program', 'Office / Department', 
                    'Contact Number', 'Address', 'City', 'Municipality', 'Province', 'Country', 'Guardian First Name', 'Guardian Last Name',
                    'Guardian Contact Number', 'Guardian Email Address', 'Guardian Address', 'Status', 'Registered Date', 'Updated Date',])

    lines = []

    for reg in reg_all:
        writer.writerow([reg.psu_email, reg.last_name, reg.first_name, reg.middle_name, reg.gender, reg.boarder_type, reg.program, 
        reg.office_dept, reg.contact_no, reg.address, reg.city, reg.municipality, reg.province, reg.country, reg.guardian_first_name,
        reg.guardian_last_name, reg.guardian_contact_no, reg.guardian_email_address, reg.guardian_present_address,reg.reg_status, 
        reg.created_at, reg.updated_at,])

    response.writelines(lines)
    return response


def reg_month_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Monthly Registration Report.csv'

    writer = csv.writer(response)

    reg_month = Person.objects.raw('''SELECT * FROM dormitory_person WHERE MONTH(created_at) = MONTH(CURRENT_DATE()) 
                                        AND YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC''')


    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Middle Name', 'Gender', 'Boarder Type', 'Program', 'Office / Department', 
                    'Contact Number', 'Address', 'City', 'Municipality', 'Province', 'Country', 'Guardian First Name', 'Guardian Last Name',
                    'Guardian Contact Number', 'Guardian Email Address', 'Guardian Address', 'Status', 'Registered Date', 'Updated Date',])

    lines = []

    for reg in reg_month:
        writer.writerow([reg.psu_email, reg.last_name, reg.first_name, reg.middle_name, reg.gender, reg.boarder_type, reg.program, 
        reg.office_dept, reg.contact_no, reg.address, reg.city, reg.municipality, reg.province, reg.country, reg.guardian_first_name,
        reg.guardian_last_name, reg.guardian_contact_no, reg.guardian_email_address, reg.guardian_present_address,reg.reg_status, 
        reg.created_at, reg.updated_at,])

    response.writelines(lines)
    return response


def reg_year_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Yearly Registration Report.csv'

    writer = csv.writer(response)

    reg_year = Person.objects.raw('SELECT * FROM dormitory_person WHERE YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')


    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Middle Name', 'Gender', 'Boarder Type', 'Program', 'Office / Department', 
                    'Contact Number', 'Address', 'City', 'Municipality', 'Province', 'Country', 'Guardian First Name', 'Guardian Last Name',
                    'Guardian Contact Number', 'Guardian Email Address', 'Guardian Address', 'Status', 'Registered Date', 'Updated Date',])

    lines = []

    for reg in reg_year:
        writer.writerow([reg.psu_email, reg.last_name, reg.first_name, reg.middle_name, reg.gender, reg.boarder_type, reg.program, 
        reg.office_dept, reg.contact_no, reg.address, reg.city, reg.municipality, reg.province, reg.country, reg.guardian_first_name,
        reg.guardian_last_name, reg.guardian_contact_no, reg.guardian_email_address, reg.guardian_present_address,reg.reg_status, 
        reg.created_at, reg.updated_at,])

    response.writelines(lines)
    return response
# end of CSV for Registration


# CSV for Occupant
def occ_all_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Occupant Report.csv'

    writer = csv.writer(response)

    occ_all = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
                                    dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
                                    dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
                                    FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
                                    INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id ORDER BY dormitory_occupant.created_at DESC''')

    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Gender', 'Boarder Type', 'Bed Code', 'Bed Description', 'Start Date', 'End Date'])

    lines = []

    for occ in occ_all:
        writer.writerow([occ.psu_email, occ.last_name, occ.first_name, occ.gender, occ.boarder_type, 
                        occ.bed_code, occ.bed_description, occ.start_date, occ.end_date])

    response.writelines(lines)
    return response


def occ_month_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Monthly Occupant Report.csv'

    writer = csv.writer(response)

    occ_month = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
                                        dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
                                        dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
                                        FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
                                        INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id
                                        WHERE MONTH(start_date) = MONTH(CURRENT_DATE()) AND YEAR(start_date) = YEAR(CURRENT_DATE()) 
                                        ORDER BY dormitory_occupant.created_at DESC''')

    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Gender', 'Boarder Type', 'Bed Code', 'Bed Description', 'Start Date', 'End Date'])

    lines = []

    for occ in occ_month:
        writer.writerow([occ.psu_email, occ.last_name, occ.first_name, occ.gender, occ.boarder_type, 
                        occ.bed_code, occ.bed_description, occ.start_date, occ.end_date])

    response.writelines(lines)
    return response


def occ_year_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Yearly Occupant Report.csv'

    writer = csv.writer(response)

    occ_year = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
                                     dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
                                     dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
                                     FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
                                     INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id
                                     WHERE YEAR(start_date) = YEAR(CURRENT_DATE()) ORDER BY dormitory_occupant.created_at DESC''')

    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Gender', 'Boarder Type', 'Bed Code', 'Bed Description', 'Start Date', 'End Date'])

    lines = []

    for occ in occ_year:
        writer.writerow([occ.psu_email, occ.last_name, occ.first_name, occ.gender, occ.boarder_type, 
                        occ.bed_code, occ.bed_description, occ.start_date, occ.end_date])

    response.writelines(lines)
    return response
# end of CSV for Occupant

# ===================================================
# Functions for Notifications
# ===================================================
from datetime import datetime, timedelta
import datetime

def AdminNotifications(request):

    # Match list storage
    messages = []

    # 30th day of every month
    today = datetime.date.today()
    if today.day >= 23:
        # 1 week before 30th day of every month
        messages.append("The 30th of the month is coming up in 1 week! Occupant must pay for their monthly bills.")

    elif today.day >= 27:
        # 3 days before 30th day of every month
        messages.append("The 30th of the month is coming up in 3 days! Occupant must pay for their monthly bills.")

    elif today.day >= 29:
        # 1 day before 30th day of every month
        messages.append("The 30th of the month is coming up in tomorrow! Occupant must pay for their monthly bills.")

    elif today.month == 2:
        if today.day >= 23:
            messages.append("The 28th or 29h of the month is coming up in one week! Occupant must pay for their monthly bills.")

    # Calculate the number of days before the due date
    num_days_before_due_date = 8

    # Calculate the due date by adding the number of days to the current date
    due_date = timezone.now() + timedelta(days=num_days_before_due_date)

    # Filter the queryset of occupants to only include those that are within the desired number of days before the due date
    occupants = Occupant.objects.filter(end_date__lte=due_date, end_date__gte=timezone.now())

    # Iterate over the occupants and add an alert message to the list for each one
    for occupant in occupants:
        days_until_due_date = (occupant.end_date - timezone.now()).days

        if days_until_due_date == 7:
            message = " have until 7 days before his/her end date. Contract date is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string) 

        elif days_until_due_date == 3:
            message = " have until 3 days before his/her end date. Contract date is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string) 

        elif days_until_due_date == 1:
            message = " have until tomorrow before his/her end date. Contract date is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string)

        else: 
            message = ""

    return render(request, 'notification_list.html', {'messages': messages})

def OccupantNotifications(request):

    # Match list storage
    messages = []

    # 30th day of every month
    today = datetime.date.today()
    if today.day >= 23:
        # 1 week before 30th day of every month
        messages.append("The 30th of the month is coming up in 1 week! Occupant must pay for their monthly bills.")

    elif today.day >= 27:
        # 3 days before 30th day of every month
        messages.append("The 30th of the month is coming up in 3 days! Occupant must pay for their monthly bills.")

    elif today.day >= 29:
        # 1 day before 30th day of every month
        messages.append("The 30th of the month is coming up in tomorrow! Occupant must pay for their monthly bills.")

    elif today.month == 2:
        if today.day >= 23:
            messages.append("The 28th or 29h of the month is coming up in one week! Occupant must pay for their monthly bills.")
    
    # Calculate the number of days before the due date
    num_days_before_due_date = 8

    # Calculate the due date by adding the number of days to the current date
    due_date = timezone.now() + timedelta(days=num_days_before_due_date)


    # Filter the queryset of occupants to only include those that are within the desired number of days before the due date
    occupants = Occupant.objects.filter(end_date__lte=due_date, end_date__gte=timezone.now()).exclude(~(Q(person__psu_email=x)))
    # print(occupants)

    # Iterate over the occupants and add an alert message to the list for each one
    for occupant in occupants:
        days_until_due_date = (occupant.end_date - timezone.now()).days

        if days_until_due_date == 7:
            message = " You have until 7 days before your contract to end. That is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string) 

        elif days_until_due_date == 3:
            message = " You have until 3 days before your contract to end. That is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string) 

        elif days_until_due_date == 1:
            message = " You have until tomorrow before your contract to end. That is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"Hi there!, {firstname} {lastname}. {message} {formatedDate}. Please prepare for your renewal if you wish to stay in the dormitory. Thank you!"
            messages.append(output_string)

        else: 
            message = ""

    return render(request, 'user_notifications.html', {'messages': messages})

def FrontDeskAdminNotifications(request):

    # Match list storage
    messages = []

    # 30th day of every month
    today = datetime.date.today()
    if today.day >= 23:
        # 1 week before 30th day of every month
        messages.append("The 30th of the month is coming up in 1 week! Occupant must pay for their monthly bills.")

    elif today.day >= 27:
        # 3 days before 30th day of every month
        messages.append("The 30th of the month is coming up in 3 days! Occupant must pay for their monthly bills.")

    elif today.day >= 29:
        # 1 day before 30th day of every month
        messages.append("The 30th of the month is coming up in tomorrow! Occupant must pay for their monthly bills.")

    elif today.month == 2:
        if today.day >= 23:
            messages.append("The 28th or 29h of the month is coming up in one week! Occupant must pay for their monthly bills.")

    # Calculate the number of days before the due date
    num_days_before_due_date = 8

    # Calculate the due date by adding the number of days to the current date
    due_date = timezone.now() + timedelta(days=num_days_before_due_date)

    # Filter the queryset of occupants to only include those that are within the desired number of days before the due date
    occupants = Occupant.objects.filter(end_date__lte=due_date, end_date__gte=timezone.now())

    # Iterate over the occupants and add an alert message to the list for each one
    for occupant in occupants:
        days_until_due_date = (occupant.end_date - timezone.now()).days

        if days_until_due_date == 7:
            message = " have until 7 days before his/her end date. Contract date is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string) 

        elif days_until_due_date == 3:
            message = " have until 3 days before his/her end date. Contract date is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string) 

        elif days_until_due_date == 1:
            message = " have until tomorrow before his/her end date. Contract date is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string)

        else: 
            message = ""

    return render(request, 'frontdesk_notification_list.html', {'messages': messages})

def AccountingAdminNotifications(request):

    # Match list storage
    messages = []

    # 30th day of every month
    today = datetime.date.today()
    if today.day >= 23:
        # 1 week before 30th day of every month
        messages.append("The 30th of the month is coming up in 1 week! Occupant must pay for their monthly bills.")

    elif today.day >= 27:
        # 3 days before 30th day of every month
        messages.append("The 30th of the month is coming up in 3 days! Occupant must pay for their monthly bills.")

    elif today.day >= 29:
        # 1 day before 30th day of every month
        messages.append("The 30th of the month is coming up in tomorrow! Occupant must pay for their monthly bills.")

    elif today.month == 2:
        if today.day >= 23:
            messages.append("The 28th or 29h of the month is coming up in one week! Occupant must pay for their monthly bills.")

    # Calculate the number of days before the due date
    num_days_before_due_date = 8

    # Calculate the due date by adding the number of days to the current date
    due_date = timezone.now() + timedelta(days=num_days_before_due_date)

    # Filter the queryset of occupants to only include those that are within the desired number of days before the due date
    occupants = Occupant.objects.filter(end_date__lte=due_date, end_date__gte=timezone.now())

    # Iterate over the occupants and add an alert message to the list for each one
    for occupant in occupants:
        days_until_due_date = (occupant.end_date - timezone.now()).days

        if days_until_due_date == 7:
            message = " have until 7 days before his/her end date. Contract date is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string) 

        elif days_until_due_date == 3:
            message = " have until 3 days before his/her end date. Contract date is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string) 

        elif days_until_due_date == 1:
            message = " have until tomorrow before his/her end date. Contract date is on "
            dictionary = {'first_name': occupant.person.first_name, 'last_name': occupant.person.last_name, 'message': message, 'end_date': occupant.end_date}

            firstname = dictionary['first_name']
            lastname = dictionary['last_name']
            message = dictionary['message']
            enddate = dictionary['end_date']
        
            formatedDate = enddate.strftime("%A, %B %d, %Y %I:%M %p")

            output_string = f"{firstname} {lastname} {message} {formatedDate}"
            messages.append(output_string)

        else: 
            message = ""

    return render(request, 'accounting_notification_list.html', {'messages': messages})
# ===================================================
# FRONT DESK
# ===================================================

class FrontDeskHomePageView(ListView):
    model = Room
    context_object_name = 'room'
    template_name = "landingpage/frontdesk_home.html"

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
        Jan = Person.objects.filter(created_at__icontains="2023-01").count()
        Jan = int(Jan)
        print('Jan:', Jan)

        Feb = Person.objects.filter(created_at__icontains="2023-02").count()
        Feb = int(Feb)
        print('Feb:', Feb)

        Mar = Person.objects.filter(created_at__icontains="2023-03").count()
        Mar = int(Mar)
        print('Mar:', Mar)

        Apr = Person.objects.filter(created_at__icontains="2023-04").count()
        Apr = int(Apr)
        print('Apr:', Apr)

        May = Person.objects.filter(created_at__icontains="2023-05").count()
        May = int(May)
        print('May:', May)

        Jun = Person.objects.filter(created_at__icontains="2023-06").count()
        Jun = int(Jun)
        print('Jun:', Jun)

        Jul = Person.objects.filter(created_at__icontains="2023-07").count()
        Jul = int(Jul)
        print('Jul:', Jul)

        Aug = Person.objects.filter(created_at__icontains="2023-08").count()
        Aug = int(Aug)
        print('Aug:', Aug)

        Sep = Person.objects.filter(created_at__icontains="2023-09").count()
        Sep = int(Sep)
        print('Sep:', Sep)

        Oct = Person.objects.filter(created_at__icontains="2023-10").count()
        Oct = int(Oct)
        print('Oct:', Oct)

        Nov = Person.objects.filter(created_at__icontains="2023-11").count()
        Nov = int(Nov)
        print('Nov:', Nov)

        Dec = Person.objects.filter(created_at__icontains="2023-12").count()
        Dec = int(Dec)
        print('Dec:', Dec)

        monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['monthly_list'] = monthly_list
        context['monthly_number'] = monthly_number


        # Monthly Occupant Charts
        Jan = Occupant.objects.filter(created_at__icontains="2023-01").count()
        Jan = int(Jan)
        print('Jan:', Jan)

        Feb = Occupant.objects.filter(created_at__icontains="2023-02").count()
        Feb = int(Feb)
        print('Feb:', Feb)

        Mar = Occupant.objects.filter(created_at__icontains="2023-03").count()
        Mar = int(Mar)
        print('Mar:', Mar)

        Apr = Occupant.objects.filter(created_at__icontains="2023-04").count()
        Apr = int(Apr)
        print('Apr:', Apr)

        May = Occupant.objects.filter(created_at__icontains="2023-05").count()
        May = int(May)
        print('May:', May)

        Jun = Occupant.objects.filter(created_at__icontains="2023-06").count()
        Jun = int(Jun)
        print('Jun:', Jun)

        Jul = Occupant.objects.filter(created_at__icontains="2023-07").count()
        Jul = int(Jul)
        print('Jul:', Jul)

        Aug = Occupant.objects.filter(created_at__icontains="2023-08").count()
        Aug = int(Aug)
        print('Aug:', Aug)

        Sep = Occupant.objects.filter(created_at__icontains="2023-09").count()
        Sep = int(Sep)
        print('Sep:', Sep)

        Oct = Occupant.objects.filter(created_at__icontains="2023-10").count()
        Oct = int(Oct)
        print('Oct:', Oct)

        Nov = Occupant.objects.filter(created_at__icontains="2023-11").count()
        Nov = int(Nov)
        print('Nov:', Nov)

        Dec = Occupant.objects.filter(created_at__icontains="2023-12").count()
        Dec = int(Dec)
        print('Dec:', Dec)

        occ_monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        occ_monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['occ_monthly_list'] = occ_monthly_list
        context['occ_monthly_number'] = occ_monthly_number
        
        return context

# @method_decorator(login_required, name='dispatch')
class FrontDeskRegistrationList(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'frontdesk_registration_list.html'
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
        qs = super(FrontDeskRegistrationList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-created_at").filter(Q(psu_email__icontains=query) | Q(last_name__icontains=query) | Q(first_name__icontains=query) 
            | Q(program__icontains=query) | Q(boarder_type__icontains=query)| Q(reg_status__iexact=query))
        return qs

def front_desk_add_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            last_name = form.cleaned_data.get('last_name')
            first_name = form.cleaned_data.get('first_name')
            psu_email = form.cleaned_data.get('psu_email')
            contact_no = form.cleaned_data.get('contact_no')
            # print(contact_no)
            person_id = form.instance.id

            cursor = connections['default'].cursor()
            query = f"INSERT INTO dormitory_user VALUES('', now(), now(), '{last_name}', '{first_name}', '{psu_email}', '123456', '', '', '', 'inactive','{contact_no}', '{person_id}')"
            cursor.execute(query)

            program = form.cleaned_data.get('program')

            if program == "Bachelor of Science in Social Work":
                cursor = connections['default'].cursor()
                query1 = f"UPDATE dormitory_person SET office_dept = 'Department of Behavioral Science' WHERE `id` = {person_id}"
                cursor.execute(query1)

            elif program == "Bachelor of Science in Psychology":
                cursor = connections['default'].cursor()
                query2 = f"UPDATE dormitory_person SET office_dept = 'Department of Behavioral Science' WHERE `id` = {person_id}"
                cursor.execute(query2)

            elif program == "Bachelor of Arts in Communication":
                cursor = connections['default'].cursor()
                query3 = f"UPDATE dormitory_person SET office_dept = 'Department of Behavioral Science' WHERE `id` = {person_id}"
                cursor.execute(query3)

            elif program == "Bachelor of Arts in Political Science":
                cursor = connections['default'].cursor()
                query4 = f"UPDATE dormitory_person SET office_dept = 'Department of Social Sciences' WHERE `id` = {person_id}"
                cursor.execute(query4)

            elif program == "Bachelor of Arts in Philippine Studies":
                cursor = connections['default'].cursor()
                query5 = f"UPDATE dormitory_person SET office_dept = 'Department of Foreign Language' WHERE `id` = {person_id}"
                cursor.execute(query5)

            elif program == "Bachelor of Science in Biology Major in Medical Biology":
                cursor = connections['default'].cursor()
                query6 = f"UPDATE dormitory_person SET office_dept = 'Bio-Physical Science Department' WHERE `id` = {person_id}"
                cursor.execute(query6)

            elif program == "Bachelor of Science in Marine Biology":
                cursor = connections['default'].cursor()
                query7 = f"UPDATE dormitory_person SET office_dept = 'Bio-Physical Science Department' WHERE `id` = {person_id}"
                cursor.execute(query7)

            elif program == "Bachelor of Science in Environmental Science":
                cursor = connections['default'].cursor()
                query8 = f"UPDATE dormitory_person SET office_dept = 'Bio-Physical Science Department' WHERE `id` = {person_id}"
                cursor.execute(query8)

            elif program == "Bachelor of Science in Information Technology":
                cursor = connections['default'].cursor()
                query9 = f"UPDATE dormitory_person SET office_dept = 'Computer Studies Department' WHERE `id` = {person_id}"
                cursor.execute(query9)

            elif program == "Bachelor of Science in Computer Science":
                cursor = connections['default'].cursor()
                query10 = f"UPDATE dormitory_person SET office_dept = 'Computer Studies Department' WHERE `id` = {person_id}"
                cursor.execute(query10)

            elif program == "Bachelor of Science in Physical Education":
                cursor = connections['default'].cursor()
                query11 = f"UPDATE dormitory_person SET office_dept = 'Department of Physical Education' WHERE `id` = {person_id}"
                cursor.execute(query11)

            elif program == "Bachelor of Science in Elementary Education":
                cursor = connections['default'].cursor()
                query12 = f"UPDATE dormitory_person SET office_dept = 'Department of Elementary Education' WHERE `id` = {person_id}"
                cursor.execute(query12)

            elif program == "Bachelor of Science in Secondary Education Major in Science":
                cursor = connections['default'].cursor()
                query13 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query13)

            elif program == "Bachelor of Science in Secondary Education Major in Math":
                cursor = connections['default'].cursor()
                query14 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query14)

            elif program == "Bachelor of Science in Secondary Education Major in English":
                cursor = connections['default'].cursor()
                query15 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query15)

            elif program == "Bachelor of Science in Secondary Education Major in Filipino":
                cursor = connections['default'].cursor()
                query16 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query16)

            elif program == "Bachelor of Science in Secondary Education Major in Social Studies":
                cursor = connections['default'].cursor()
                query17 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query17)

            elif program == "Bachelor of Science in Secondary Education Major in Values":
                cursor = connections['default'].cursor()
                query18 = f"UPDATE dormitory_person SET office_dept = 'Department of Secondary Education' WHERE `id` = {person_id}"
                cursor.execute(query18)

            elif program == "Bachelor of Science in Accountancy":
                cursor = connections['default'].cursor()
                query19 = f"UPDATE dormitory_person SET office_dept = 'Department of Accountancy' WHERE `id` = {person_id}"
                cursor.execute(query19)

            elif program == "Bachelor of Science in Management Accountancy":
                cursor = connections['default'].cursor()
                query20 = f"UPDATE dormitory_person SET office_dept = 'Department of Accountancy' WHERE `id` = {person_id}"
                cursor.execute(query20)

            elif program == "Bachelor of Science in Entrepreneurship":
                cursor = connections['default'].cursor()
                query21 = f"UPDATE dormitory_person SET office_dept = 'Department of Marketing Management, Entrepreneurship, and Public Administration' WHERE `id` = {person_id}"
                cursor.execute(query21)

            elif program == "Bachelor of Science in Business Administration  Major in Marketing Management":
                cursor = connections['default'].cursor()
                query22 = f"UPDATE dormitory_person SET office_dept = 'Department of Marketing Management, Entrepreneurship, and Public Administration' WHERE `id` = {person_id}"
                cursor.execute(query22)

            elif program == "Bachelor of Science in Business Administration  Major in Public Administration":
                cursor = connections['default'].cursor()
                query23 = f"UPDATE dormitory_person SET office_dept = 'Department of Marketing Management, Entrepreneurship, and Public Administration' WHERE `id` = {person_id}"
                cursor.execute(query23)

            elif program == "Bachelor of Science in Business Administration  Major in Financial Management":
                cursor = connections['default'].cursor()
                query24 = f"UPDATE dormitory_person SET office_dept = 'Department of Financial Management, Human Resource Management, and Business Economics' WHERE `id` = {person_id}"
                cursor.execute(query24)

            elif program == "Bachelor of Science in Business Administration  Major in Human Resource Management":
                cursor = connections['default'].cursor()
                query25 = f"UPDATE dormitory_person SET office_dept = 'Department of Financial Management, Human Resource Management, and Business Economics' WHERE `id` = {person_id}"
                cursor.execute(query25)

            elif program == "Bachelor of Science in Business Administration  Major in Business Economics":
                cursor = connections['default'].cursor()
                query26 = f"UPDATE dormitory_person SET office_dept = 'Department of Financial Management, Human Resource Management, and Business Economics' WHERE `id` = {person_id}"
                cursor.execute(query26)

            elif program == "Bachelor of Science in Hospitality Management":
                cursor = connections['default'].cursor()
                query27 = f"UPDATE dormitory_person SET office_dept = 'Hospitality Management Department' WHERE `id` = {person_id}"
                cursor.execute(query27)

            elif program == "Track - Culinary Arts and Kitchen Management":
                cursor = connections['default'].cursor()
                query28 = f"UPDATE dormitory_person SET office_dept = 'Hospitality Management Department' WHERE `id` = {person_id}"
                cursor.execute(query28)

            elif program == "Bachelor of Science in Tourism Management":
                cursor = connections['default'].cursor()
                query29 = f"UPDATE dormitory_person SET office_dept = 'Tourism Management Department' WHERE `id` = {person_id}"
                cursor.execute(query29)

            elif program == "Track - Hotel,Resort, and Club Management":
                cursor = connections['default'].cursor()
                query30 = f"UPDATE dormitory_person SET office_dept = 'Tourism Management Department' WHERE `id` = {person_id}"
                cursor.execute(query30)

            elif program == "Bachelor of Science in Civil Engineering":
                cursor = connections['default'].cursor()
                query31 = f"UPDATE dormitory_person SET office_dept = 'Department of Civil Engineering' WHERE `id` = {person_id}"
                cursor.execute(query31)

            elif program == "Bachelor of Science in Mechanical Engineering":
                cursor = connections['default'].cursor()
                query32 = f"UPDATE dormitory_person SET office_dept = 'Department of Mechanical Engineering' WHERE `id` = {person_id}"
                cursor.execute(query32)

            elif program == "Bachelor of Science in Electrical Engineering":
                cursor = connections['default'].cursor()
                query33 = f"UPDATE dormitory_person SET office_dept = 'Department of Electrical Engineering' WHERE `id` = {person_id}"
                cursor.execute(query33)

            elif program == "Bachelor of Science in Petroleum Engineering":
                cursor = connections['default'].cursor()
                query34 = f"UPDATE dormitory_person SET office_dept = 'Department of Petroleum Engineering' WHERE `id` = {person_id}"
                cursor.execute(query34)

            elif program == "Bachelor of Science in Architecture":
                cursor = connections['default'].cursor()
                query35 = f"UPDATE dormitory_person SET office_dept = 'Department of Architecture' WHERE `id` = {person_id}"
                cursor.execute(query35)

            elif program == "Bachelor of Science in Nursing":
                cursor = connections['default'].cursor()
                query36 = f"UPDATE dormitory_person SET office_dept = 'Department of Nursing' WHERE `id` = {person_id}"
                cursor.execute(query36)

            elif program == "Diploma in Midwifery":
                cursor = connections['default'].cursor()
                query37 = f"UPDATE dormitory_person SET office_dept = 'Department of Midwifery' WHERE `id` = {person_id}"
                cursor.execute(query37)

            elif program == "Bachelor of Science in Midwifery":
                cursor = connections['default'].cursor()
                query38 = f"UPDATE dormitory_person SET office_dept = 'Department of Midwifery' WHERE `id` = {person_id}"
                cursor.execute(query38)

            elif program == "Bachelor of Science in Criminology":
                cursor = connections['default'].cursor()
                query39 = f"UPDATE dormitory_person SET office_dept = 'No Office / Department' WHERE `id` = {person_id}"
                cursor.execute(query39)

        
            messages.success(request, 'New student registered successfully!')
            return redirect('FrontDeskRegistrationAdd')

        else:
            messages.error(request, 'Please complete the required field/s.')
            # print()
            return redirect('FrontDeskRegistrationAdd')
    else:
        form = RegistrationForm()
        return render(request, 'frontdesk_registration_add.html',  {'form': form})


# @method_decorator(login_required, name='dispatch')
class FrontDeskRegMonthRep(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'frontdesk_reg_month_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = Person.objects.raw('SELECT * FROM dormitory_person WHERE MONTH(created_at) = MONTH(CURRENT_DATE()) AND YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')
        return context

# @method_decorator(login_required, name='dispatch')
class FrontDeskRegYearRep(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'frontdesk_reg_year_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = Person.objects.raw('SELECT * FROM dormitory_person WHERE YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')
        return context


# @method_decorator(login_required, name='dispatch')
class FrontDeskRegistrationUpdateView(UpdateView):
    model = Person
    fields = ['psu_email','last_name','first_name','middle_name','gender','boarder_type','program',
            'office_dept','contact_no','address','city','municipality','province','country',
            'guardian_first_name','guardian_last_name','guardian_email_address',
            'guardian_present_address','guardian_contact_no','Field1','Field2','Field3',
            'Field4','Field5','Field6','Field7']
    context_object_name = 'person'
    template_name = 'frontdesk_registration_update.html'
    success_url = "/frontdesk_registration_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Registration details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class FrontDeskRegistrationRegView(UpdateView):
    model = Person
    fields = "__all__"
    context_object_name = 'person'
    template_name = 'frontdesk_registration_view.html'
    success_url = "/frontdesk_registration_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Registration details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

def frontdesk_RegPDF(request, pk):
    reg_person = Person.objects.get(id=pk)
    template_path = 'frontdesk_reg_pdf.html'
    context = {
        'reg_person': reg_person,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Registration Information.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

    # CSV for Registration
def frontdesk_reg_all_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Registration Report.csv'

    writer = csv.writer(response)

    reg_all = Person.objects.raw('SELECT * FROM dormitory_person ORDER BY created_at DESC')


    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Middle Name', 'Gender', 'Boarder Type', 'Program', 'Office / Department', 
                    'Contact Number', 'Address', 'City', 'Municipality', 'Province', 'Country', 'Guardian First Name', 'Guardian Last Name',
                    'Guardian Contact Number', 'Guardian Email Address', 'Guardian Address', 'Status', 'Registered Date', 'Updated Date',])

    lines = []

    for reg in reg_all:
        writer.writerow([reg.psu_email, reg.last_name, reg.first_name, reg.middle_name, reg.gender, reg.boarder_type, reg.program, 
        reg.office_dept, reg.contact_no, reg.address, reg.city, reg.municipality, reg.province, reg.country, reg.guardian_first_name,
        reg.guardian_last_name, reg.guardian_contact_no, reg.guardian_email_address, reg.guardian_present_address,reg.reg_status, 
        reg.created_at, reg.updated_at,])

    response.writelines(lines)
    return response


def frontdesk_reg_month_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Monthly Registration Report.csv'

    writer = csv.writer(response)

    reg_month = Person.objects.raw('''SELECT * FROM dormitory_person WHERE MONTH(created_at) = MONTH(CURRENT_DATE()) 
                                        AND YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC''')


    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Middle Name', 'Gender', 'Boarder Type', 'Program', 'Office / Department', 
                    'Contact Number', 'Address', 'City', 'Municipality', 'Province', 'Country', 'Guardian First Name', 'Guardian Last Name',
                    'Guardian Contact Number', 'Guardian Email Address', 'Guardian Address', 'Status', 'Registered Date', 'Updated Date',])

    lines = []

    for reg in reg_month:
        writer.writerow([reg.psu_email, reg.last_name, reg.first_name, reg.middle_name, reg.gender, reg.boarder_type, reg.program, 
        reg.office_dept, reg.contact_no, reg.address, reg.city, reg.municipality, reg.province, reg.country, reg.guardian_first_name,
        reg.guardian_last_name, reg.guardian_contact_no, reg.guardian_email_address, reg.guardian_present_address,reg.reg_status, 
        reg.created_at, reg.updated_at,])

    response.writelines(lines)
    return response


def frontdesk_reg_year_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Yearly Registration Report.csv'

    writer = csv.writer(response)

    reg_year = Person.objects.raw('SELECT * FROM dormitory_person WHERE YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')


    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Middle Name', 'Gender', 'Boarder Type', 'Program', 'Office / Department', 
                    'Contact Number', 'Address', 'City', 'Municipality', 'Province', 'Country', 'Guardian First Name', 'Guardian Last Name',
                    'Guardian Contact Number', 'Guardian Email Address', 'Guardian Address', 'Status', 'Registered Date', 'Updated Date',])

    lines = []

    for reg in reg_year:
        writer.writerow([reg.psu_email, reg.last_name, reg.first_name, reg.middle_name, reg.gender, reg.boarder_type, reg.program, 
        reg.office_dept, reg.contact_no, reg.address, reg.city, reg.municipality, reg.province, reg.country, reg.guardian_first_name,
        reg.guardian_last_name, reg.guardian_contact_no, reg.guardian_email_address, reg.guardian_present_address,reg.reg_status, 
        reg.created_at, reg.updated_at,])

    response.writelines(lines)
    return response
# end of CSV for Registration


# @method_decorator(login_required, name='dispatch')
class FrontDeskOccupantList(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'frontdesk_occupant_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['occupants'] = Occupant.objects.values('person__last_name').distinct().count()
        context['local'] = Occupant.objects.values('person__last_name').distinct().filter(person__boarder_type__iexact="Local").count() 
        context['foreign'] = Occupant.objects.values('person__last_name').distinct().filter(person__boarder_type__iexact="Foreign").count()
        context['renewal'] = Occupant.objects.values('person__last_name').annotate(Count('id')).order_by().filter(id__count__gt=1).count()
        context['today'] = timezone.now()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(FrontDeskOccupantList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-created_at").filter(Q(person__last_name__icontains=query) | Q(person__first_name__icontains=query)
            | Q(bed__bed_code__icontains=query) | Q(person__boarder_type__icontains=query))
        return qs


def frontdesk_add_occupant(request):
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

            return redirect('FrontDeskOccupantAdd')

        else:
            
            messages.error(request, 'Please complete the required field.')
            # print()
            return redirect('FrontDeskOccupantAdd')
    else:
        form = OccupantForm()
        return render(request, 'frontdesk_occupant_add.html',  {'form': form})


def frontdesk_renew_occupant(request):
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

            return redirect('FrontDeskOccupantRenew')

        else:
            
            messages.error(request, 'Please complete the required field.')
            # print()
            return redirect('FrontDeskOccupantRenew')
    else:
        form = OccupantRenewForm()
        return render(request, 'frontdesk_occupant_renew.html',  {'form': form})  

# CSV for Occupant
def frontdesk_occ_all_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Occupant Report.csv'

    writer = csv.writer(response)

    occ_all = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
                                    dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
                                    dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
                                    FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
                                    INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id ORDER BY dormitory_occupant.created_at DESC''')

    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Gender', 'Boarder Type', 'Bed Code', 'Bed Description', 'Start Date', 'End Date'])

    lines = []

    for occ in occ_all:
        writer.writerow([occ.psu_email, occ.last_name, occ.first_name, occ.gender, occ.boarder_type, 
                        occ.bed_code, occ.bed_description, occ.start_date, occ.end_date])

    response.writelines(lines)
    return response


def frontdesk_occ_month_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Monthly Occupant Report.csv'

    writer = csv.writer(response)

    occ_month = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
                                        dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
                                        dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
                                        FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
                                        INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id
                                        WHERE MONTH(start_date) = MONTH(CURRENT_DATE()) AND YEAR(start_date) = YEAR(CURRENT_DATE()) 
                                        ORDER BY dormitory_occupant.created_at DESC''')

    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Gender', 'Boarder Type', 'Bed Code', 'Bed Description', 'Start Date', 'End Date'])

    lines = []

    for occ in occ_month:
        writer.writerow([occ.psu_email, occ.last_name, occ.first_name, occ.gender, occ.boarder_type, 
                        occ.bed_code, occ.bed_description, occ.start_date, occ.end_date])

    response.writelines(lines)
    return response


def frontdesk_occ_year_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Yearly Occupant Report.csv'

    writer = csv.writer(response)

    occ_year = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
                                     dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
                                     dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
                                     FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
                                     INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id
                                     WHERE YEAR(start_date) = YEAR(CURRENT_DATE()) ORDER BY dormitory_occupant.created_at DESC''')

    writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Gender', 'Boarder Type', 'Bed Code', 'Bed Description', 'Start Date', 'End Date'])

    lines = []

    for occ in occ_year:
        writer.writerow([occ.psu_email, occ.last_name, occ.first_name, occ.gender, occ.boarder_type, 
                        occ.bed_code, occ.bed_description, occ.start_date, occ.end_date])

    response.writelines(lines)
    return response
# end of CSV for Occupant


# @method_decorator(login_required, name='dispatch')
class FrontDeskOccMonthRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'frontdesk_occ_month_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
                                    dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
                                    dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
                                    FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
                                    INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id
                                    WHERE MONTH(start_date) = MONTH(CURRENT_DATE()) AND YEAR(start_date) = YEAR(CURRENT_DATE()) 
                                    ORDER BY dormitory_occupant.created_at DESC''')
        return context


# @method_decorator(login_required, name='dispatch')
class FrontDeskOccYearRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'frontdesk_occ_year_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
                                    dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
                                    dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
                                    FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
                                    INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id
                                    WHERE YEAR(start_date) = YEAR(CURRENT_DATE()) ORDER BY dormitory_occupant.created_at DESC''')
        return context


def FrontDeskOccPDF(request, pk):
    occ_person = Occupant.objects.get(id=pk)
    table1 = Bill_Details.objects.filter(occupant=pk)[0:3]
    table2 = Bill_Details.objects.filter(occupant=pk)[3:]
    table3 = Payment.objects.filter(occupant=pk)
    total_bills_amount = Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    payment = Payment.objects.filter(occupant=pk)
    total_payment_amount = Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_balance = (Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0)
    table4 = OccupantDemerit.objects.filter(occupant=pk)
    template_path = 'frontdesk_occ_pdf.html'

    context = {
        'occ_person': occ_person,
        'table1': table1,
        'table2': table2,
        'table3': table3,
        'total_bills_amount': total_bills_amount,
        'payment': payment,
        'total_payment_amount': total_payment_amount,
        'remaining_balance': remaining_balance,
        'table4': table4,
    }
 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Occupant Information.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# @method_decorator(login_required, name='dispatch')
class FrontDeskOccupantUpdateView(UpdateView):
    model = Occupant
    # fields = ['person','bed','start_date','end_date']
    context_object_name = 'occupant'
    form_class = OccupantFormEdit
    template_name = 'frontdesk_occupant_update.html'
    success_url = "/frontdesk_occupant_list"

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
        return "/frontdesk_occupant_list"

    def form_valid(self, form):
      messages.success(self.request, "Occupant details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class FrontDeskOccupantView(UpdateView):
    model = Occupant
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'frontdesk_occupant_view.html'

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

    def form_valid(self, form):
      messages.success(self.request, "Occupant details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class FrontDeskOccupantViewDemeritUpdate(UpdateView):
    model = OccupantDemerit
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'frontdesk_occupant_demerit_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(f"ID {self.object.occupant_id}")
        return context

    def get_success_url(self):
        return reverse('FrontDeskOccupantView', kwargs={'pk': self.object.occupant_id})

    def form_valid(self, form):
      messages.success(self.request, "Occupant demerit was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class FrontDeskOccupantDemeritList(ListView):
    model = OccupantDemerit
    context_object_name = 'occupant'
    template_name = 'frontdesk_occupant_demerit_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['occupant_demerit'] = OccupantDemerit.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(FrontDeskOccupantDemeritList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("occupant")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(demerit_name__demerit_name__icontains=query)
            | Q(demerit_name__demerit_points__icontains=query) | Q(cur_date__icontains=query) | Q(remarks__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class FrontDeskOccupantDemeritUpdateView(UpdateView):
    model = OccupantDemerit
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'frontdesk_occupant_demerit_update.html'
    success_url = "/frontdesk_occupant_demerit_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Occupant demerit was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


def frontdesk_add_occupant_demerit(request):
    if request.method == "POST":
        form = OccupantDemeritForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New demerit for occupant added successfully!')
            return redirect('FrontDeskOccupantDemeritAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('FrontDeskOccupantDemeritAdd')
    else:
        form = OccupantDemeritForm()
        return render(request, 'frontdesk_occupant_demerit_add.html',  {'form': form})


# @method_decorator(login_required, name='dispatch')
class FrontDeskRoomList(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'frontdesk_room_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(FrontDeskRoomList, self).get_queryset(*args, **kwargs)
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
class FrontDeskRoomUpdateView(UpdateView):
    model = Room
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'frontdesk_room_update.html'
    success_url = "/frontdesk_room_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Room details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


def frontdesk_add_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New room added successfully!')
            return redirect('FrontDeskRoomAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('FrontDeskRoomAdd')
    else:
        form = RoomForm()
        return render(request, 'frontdesk_room_add.html',  {'form': form})


# @method_decorator(login_required, name='dispatch')
class FrontDeskBedList(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'frontdesk_bed_list.html'
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
        qs = super(FrontDeskBedList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("room_id")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("room_id").filter(Q(room__dorm_name__iexact=query) | Q(room__room_name__icontains=query)
            | Q(bed_code__icontains=query) | Q(price__icontains=query) | Q(bed_status__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class FrontDeskBedUpdateView(UpdateView):
    model = Bed
    fields = "__all__"
    context_object_name = 'bed'
    template_name = 'frontdesk_bed_update.html'
    success_url = "/frontdesk_bed_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Bed details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


def frontdesk_add_bed(request):
    if request.method == "POST":
        form = BedForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New bed added successfully!')
            return redirect('FrontDeskBedAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('FrontDeskBedAdd')
    else:
        form = BedForm()
        return render(request, 'frontdesk_bed_add.html',  {'form': form})


# @method_decorator(login_required, name='dispatch')
class FrontDeskServiceList(ListView):
    model = Service
    context_object_name = 'service'
    template_name = 'frontdesk_service_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services']= Service.objects.all().exclude(service_name__iexact='Deposit').exclude(service_name__iexact='Advance').exclude(service_name__iexact='Dorm ID').count()
        context['available'] = Service.objects.filter(status__iexact="Available").exclude(service_name__iexact='Deposit').exclude(service_name__iexact='Advance').exclude(service_name__iexact='Dorm ID').count()
        context['notavailable'] = Service.objects.filter(status__iexact="Not Available").count()
        context['services_limit']= Service.objects.all().exclude(service_name__iexact='Deposit').exclude(service_name__iexact='Advance').exclude(service_name__iexact='Dorm ID')
    
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(FrontDeskServiceList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("service_name")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("service_name").filter(Q(service_name__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class FrontDeskServiceUpdateView(UpdateView):
    model = Service
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'frontdesk_service_update.html'
    success_url = "/frontdesk_service_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Service details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


def frontdesk_add_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New service added successfully!')
            return redirect('FrontDeskServiceAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('FrontDeskServiceAdd')
    else:
        form = ServiceForm()
        return render(request, 'frontdesk_service_add.html',  {'form': form})


# @method_decorator(login_required, name='dispatch')
class FrontDeskDemeritList(ListView):
    model = Demerit
    context_object_name = 'demerit'
    template_name = 'frontdesk_demerit_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demerit'] = Demerit.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(FrontDeskDemeritList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("demerit_points")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-demerit_points").filter(Q(demerit_name__icontains=query) 
            | Q(demerit_points__iexact=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class FrontDeskDemeritUpdateView(UpdateView):
    model = Demerit
    fields = "__all__"
    context_object_name = 'demerit'
    template_name = 'frontdesk_demerit_update.html'
    success_url = "/frontdesk_demerit_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Demerit details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


def frontdesk_add_demerit(request):
    if request.method == "POST":
        form = DemeritForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New demerit added successfully!')
            return redirect('FrontDeskDemeritAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('FrontDeskDemeritAdd')
    else:
        form = DemeritForm()
        return render(request, 'frontdesk_demerit_add.html',  {'form': form})

# @method_decorator(login_required, name='dispatch')
class FrontDeskAdminProfile(ListView):
    model = Admin
    context_object_name = 'admin'
    template_name = "frontdesk_admin_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global xy
        context ['acc'] = Admin.objects.filter(Q(username=xy)).values()
        return context

# @method_decorator(login_required, name='dispatch')
class FrontDeskAdminProfileUpdateView(UpdateView):
    model = Admin
    fields = ['firstname', 'lastname', 'username', 'password', 'security_question', 'security_answer', 'recovery_email']
    context_object_name = 'admin'
    template_name = 'frontdesk_admin_profile_update.html'
    success_url = "/frontdesk_admin_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Your Account Information was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# ===================================================
# ACCOUNTING STAFF
# ===================================================
# @method_decorator(login_required, name='dispatch')
class AccountingHomePageView(ListView):
    model = Room
    context_object_name = 'room'
    template_name = "landingpage/accounting_home.html"

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
        Jan = Person.objects.filter(created_at__icontains="2023-01").count()
        Jan = int(Jan)
        print('Jan:', Jan)

        Feb = Person.objects.filter(created_at__icontains="2023-02").count()
        Feb = int(Feb)
        print('Feb:', Feb)

        Mar = Person.objects.filter(created_at__icontains="2023-03").count()
        Mar = int(Mar)
        print('Mar:', Mar)

        Apr = Person.objects.filter(created_at__icontains="2023-04").count()
        Apr = int(Apr)
        print('Apr:', Apr)

        May = Person.objects.filter(created_at__icontains="2023-05").count()
        May = int(May)
        print('May:', May)

        Jun = Person.objects.filter(created_at__icontains="2023-06").count()
        Jun = int(Jun)
        print('Jun:', Jun)

        Jul = Person.objects.filter(created_at__icontains="2023-07").count()
        Jul = int(Jul)
        print('Jul:', Jul)

        Aug = Person.objects.filter(created_at__icontains="2023-08").count()
        Aug = int(Aug)
        print('Aug:', Aug)

        Sep = Person.objects.filter(created_at__icontains="2023-09").count()
        Sep = int(Sep)
        print('Sep:', Sep)

        Oct = Person.objects.filter(created_at__icontains="2023-10").count()
        Oct = int(Oct)
        print('Oct:', Oct)

        Nov = Person.objects.filter(created_at__icontains="2023-11").count()
        Nov = int(Nov)
        print('Nov:', Nov)

        Dec = Person.objects.filter(created_at__icontains="2023-12").count()
        Dec = int(Dec)
        print('Dec:', Dec)

        monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['monthly_list'] = monthly_list
        context['monthly_number'] = monthly_number


        # Monthly Occupant Charts
        Jan = Occupant.objects.filter(created_at__icontains="2023-01").count()
        Jan = int(Jan)
        print('Jan:', Jan)

        Feb = Occupant.objects.filter(created_at__icontains="2023-02").count()
        Feb = int(Feb)
        print('Feb:', Feb)

        Mar = Occupant.objects.filter(created_at__icontains="2023-03").count()
        Mar = int(Mar)
        print('Mar:', Mar)

        Apr = Occupant.objects.filter(created_at__icontains="2023-04").count()
        Apr = int(Apr)
        print('Apr:', Apr)

        May = Occupant.objects.filter(created_at__icontains="2023-05").count()
        May = int(May)
        print('May:', May)

        Jun = Occupant.objects.filter(created_at__icontains="2023-06").count()
        Jun = int(Jun)
        print('Jun:', Jun)

        Jul = Occupant.objects.filter(created_at__icontains="2023-07").count()
        Jul = int(Jul)
        print('Jul:', Jul)

        Aug = Occupant.objects.filter(created_at__icontains="2023-08").count()
        Aug = int(Aug)
        print('Aug:', Aug)

        Sep = Occupant.objects.filter(created_at__icontains="2023-09").count()
        Sep = int(Sep)
        print('Sep:', Sep)

        Oct = Occupant.objects.filter(created_at__icontains="2023-10").count()
        Oct = int(Oct)
        print('Oct:', Oct)

        Nov = Occupant.objects.filter(created_at__icontains="2023-11").count()
        Nov = int(Nov)
        print('Nov:', Nov)

        Dec = Occupant.objects.filter(created_at__icontains="2023-12").count()
        Dec = int(Dec)
        print('Dec:', Dec)

        occ_monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        occ_monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['occ_monthly_list'] = occ_monthly_list
        context['occ_monthly_number'] = occ_monthly_number
        
        return context

class AccountingAdminProfile(ListView):
    model = Admin
    context_object_name = 'admin'
    template_name = "accounting_admin_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global ac
        context ['acc'] = Admin.objects.filter(Q(username=ac)).values()
        return context

# @method_decorator(login_required, name='dispatch')
class AccountingAdminProfileUpdateView(UpdateView):
    model = Admin
    fields = ['firstname', 'lastname', 'username', 'password', 'security_question', 'security_answer', 'recovery_email']
    context_object_name = 'admin'
    template_name = 'accounting_admin_profile_update.html'
    success_url = "/accounting_admin_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Your Account Information was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class AccountingServiceList(ListView):
    model = Service
    context_object_name = 'service'
    template_name = 'accounting_service_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services']= Service.objects.all().exclude(service_name__iexact='Deposit').exclude(service_name__iexact='Advance').exclude(service_name__iexact='Dorm ID').count()
        context['available'] = Service.objects.filter(status__iexact="Available").exclude(service_name__iexact='Deposit').exclude(service_name__iexact='Advance').exclude(service_name__iexact='Dorm ID').count()
        context['notavailable'] = Service.objects.filter(status__iexact="Not Available").count()
        context['services_limit']= Service.objects.all().exclude(service_name__iexact='Deposit').exclude(service_name__iexact='Advance').exclude(service_name__iexact='Dorm ID')
    
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(AccountingServiceList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("service_name")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("service_name").filter(Q(service_name__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class AccountingPaymentList(ListView):
    model = Payment
    context_object_name = 'payment'
    template_name = 'accounting_payment_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment'] = Payment.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(AccountingPaymentList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("occupant")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(payment_date__icontains=query)
            | Q(amount__icontains=query) | Q(receipt_no__iexact=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class AccountingPaymentUpdateView(UpdateView):
    model = Payment
    fields = "__all__"
    context_object_name = 'payment'
    template_name = 'accounting_payment_update.html'
    success_url = "/accounting_payment_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Payment details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


def accounting_add_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New payment added successfully!')
            return redirect('AccountingPaymentAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('AccountingPaymentAdd')
    else:
        form = PaymentForm()
        return render(request, 'accounting_payment_add.html',  {'form': form})


def accounting_add_billing(request):
    if request.method == "POST":
        form = BillingForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()

            service = form.cleaned_data['service']
            quantity = form.cleaned_data['quantity']
            
            price = Service.objects.filter(service_name= service).first()
            bill_id = form.instance.id

            total_amount = price.base_amount * quantity

            cursor = connections['default'].cursor()
            query = f"UPDATE dormitory_bill_details SET amount = '{total_amount}' WHERE `id` = {bill_id}"
            cursor.execute(query)
            
            messages.success(request, 'New bill added successfully!')
            return redirect('AccountingBillingAdd')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('AccountingBillingAdd')
    else:
        form = BillingForm()
        return render(request, 'accounting_billing_add.html',  {'form': form})


def accounting_other_add_billing(request):
    if request.method == "POST":
        form = OtherBillingForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'New bill added successfully!')
            return redirect('accounting-other-add')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('accounting-other-add')
    else:
        form = OtherBillingForm()
        return render(request, 'accounting_others_billing_add.html',  {'form': form})

def accounting_other_add(request):
    return render(request, 'accounting_billing_list/accounting_others_billing_add.html', {} )


def accounting_other_update_billing(request, billing_id):
    billing = Bill_Details.objects.get(pk=billing_id)
    form = OtherBillingForm(request.POST or None, instance=billing)
    if form.is_valid():
        form.save()
        messages.success(request, 'Billing details was updated successfully!')
        return redirect('AccountingBillingList')
    return render (request, 'accounting_others_billing_update.html', {'billing': billing, 'form': form})

# @method_decorator(login_required, name='dispatch')
class AccountingBillingList(ListView):
    model = Bill_Details
    context_object_name = 'occupant'
    template_name = 'accounting_billing_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bills'] = Bill_Details.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(AccountingBillingList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("occupant")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(service__service_name__icontains=query)
            | Q(description__icontains=query) | Q(amount__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class AccountingBillingUpdateView(UpdateView):
    model = Bill_Details
    form_class = BillingForm
    context_object_name = 'occupant'
    template_name = 'accounting_billing_update.html'
    success_url = "/accounting_billing_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Billing details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class AccountingOccupantList(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'accounting_occupant_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['occupants'] = Occupant.objects.values('person__last_name').distinct().count()
        context['local'] = Occupant.objects.values('person__last_name').distinct().filter(person__boarder_type__iexact="Local").count() 
        context['foreign'] = Occupant.objects.values('person__last_name').distinct().filter(person__boarder_type__iexact="Foreign").count()
        context['renewal'] = Occupant.objects.values('person__last_name').annotate(Count('id')).order_by().filter(id__count__gt=1).count()
        context['today'] = timezone.now()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(AccountingOccupantList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-created_at").filter(Q(person__last_name__icontains=query) | Q(person__first_name__icontains=query)
            | Q(bed__bed_code__icontains=query) | Q(person__boarder_type__icontains=query))
        return qs


# def accounting_occ_all_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Occupant Report.csv'

#     writer = csv.writer(response)

#     occ_all = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
#                                     dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
#                                     dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
#                                     FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
#                                     INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id ORDER BY dormitory_occupant.created_at DESC''')

#     writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Gender', 'Boarder Type', 'Bed Code', 'Bed Description', 'Start Date', 'End Date'])

#     lines = []

#     for occ in occ_all:
#         writer.writerow([occ.psu_email, occ.last_name, occ.first_name, occ.gender, occ.boarder_type, 
#                         occ.bed_code, occ.bed_description, occ.start_date, occ.end_date])

#     response.writelines(lines)
#     return response


# def accounting_occ_month_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Monthly Occupant Report.csv'

#     writer = csv.writer(response)

#     occ_month = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
#                                         dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
#                                         dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
#                                         FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
#                                         INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id
#                                         WHERE MONTH(start_date) = MONTH(CURRENT_DATE()) AND YEAR(start_date) = YEAR(CURRENT_DATE()) 
#                                         ORDER BY dormitory_occupant.created_at DESC''')

#     writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Gender', 'Boarder Type', 'Bed Code', 'Bed Description', 'Start Date', 'End Date'])

#     lines = []

#     for occ in occ_month:
#         writer.writerow([occ.psu_email, occ.last_name, occ.first_name, occ.gender, occ.boarder_type, 
#                         occ.bed_code, occ.bed_description, occ.start_date, occ.end_date])

#     response.writelines(lines)
#     return response


# def accounting_occ_year_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=PSU Dormitory Yearly Occupant Report.csv'

#     writer = csv.writer(response)

#     occ_year = Occupant.objects.raw('''SELECT 1 as id, dormitory_person.psu_email, dormitory_person.last_name, dormitory_person.first_name,
#                                      dormitory_person.gender, dormitory_person.boarder_type, dormitory_bed.bed_code, 
#                                      dormitory_bed.bed_description, dormitory_occupant.start_date, dormitory_occupant.end_date 
#                                      FROM dormitory_person INNER JOIN dormitory_occupant ON dormitory_person.id=dormitory_occupant.person_id
#                                      INNER JOIN dormitory_bed ON dormitory_bed.id=dormitory_occupant.bed_id
#                                      WHERE YEAR(start_date) = YEAR(CURRENT_DATE()) ORDER BY dormitory_occupant.created_at DESC''')

#     writer.writerow(['PSU Email', 'Last Name', 'First Name', 'Gender', 'Boarder Type', 'Bed Code', 'Bed Description', 'Start Date', 'End Date'])

#     lines = []

#     for occ in occ_year:
#         writer.writerow([occ.psu_email, occ.last_name, occ.first_name, occ.gender, occ.boarder_type, 
#                         occ.bed_code, occ.bed_description, occ.start_date, occ.end_date])

#     response.writelines(lines)
#     return response
# # end of CSV for Occupant

# def AccoOccPDF(request, pk):
#     occ_person = Occupant.objects.get(id=pk)
#     table1 = Bill_Details.objects.filter(occupant=pk)[0:3]
#     table2 = Bill_Details.objects.filter(occupant=pk)[3:]
#     table3 = Payment.objects.filter(occupant=pk)
#     total_bills_amount = Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
#     payment = Payment.objects.filter(occupant=pk)
#     total_payment_amount = Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
#     remaining_balance = (Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0)
#     table4 = OccupantDemerit.objects.filter(occupant=pk)
#     template_path = 'occ_pdf.html'

#     context = {
#         'occ_person': occ_person,
#         'table1': table1,
#         'table2': table2,
#         'table3': table3,
#         'total_bills_amount': total_bills_amount,
#         'payment': payment,
#         'total_payment_amount': total_payment_amount,
#         'remaining_balance': remaining_balance,
#         'table4': table4,
#     }
 
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="Occupant Information.pdf"'
    
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     # if error then show some funy view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response


class AdminProfile(ListView):
    model = Admin
    context_object_name = 'admin'
    template_name = "admin_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global sa
        context ['acc'] = Admin.objects.filter(Q(username=sa)).values()
        return context

# @method_decorator(login_required, name='dispatch')
class AdminProfileUpdateView(UpdateView):
    model = Admin
    fields = ['firstname', 'lastname', 'username', 'password', 'security_question', 'security_answer', 'recovery_email']
    context_object_name = 'admin'
    template_name = 'admin_profile_update.html'
    success_url = "/admin_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Your Account Information was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class AccountingOccupantView(UpdateView):
    model = Occupant
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'accounting_occupant_view.html'

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

    def form_valid(self, form):
      messages.success(self.request, "Occupant details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

def AccountingOccPDF(request, pk):
    occ_person = Occupant.objects.get(id=pk)
    table1 = Bill_Details.objects.filter(occupant=pk)[0:3]
    table2 = Bill_Details.objects.filter(occupant=pk)[3:]
    table3 = Payment.objects.filter(occupant=pk)
    total_bills_amount = Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    payment = Payment.objects.filter(occupant=pk)
    total_payment_amount = Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_balance = (Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0)
    table4 = OccupantDemerit.objects.filter(occupant=pk)
    template_path = 'frontdesk_occ_pdf.html'

    context = {
        'occ_person': occ_person,
        'table1': table1,
        'table2': table2,
        'table3': table3,
        'total_bills_amount': total_bills_amount,
        'payment': payment,
        'total_payment_amount': total_payment_amount,
        'remaining_balance': remaining_balance,
        'table4': table4,
    }
 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Occupant Information.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# Due Date Email Notifications

# Get the current date and time
now = datetime.datetime.now()

# Calculate the date that is 1 week before the 30th of the month
if now.month == 2:  # February
    if now.day >= 23:
        occ_date = datetime.date(now.year, 3, 1) - datetime.timedelta(days=9)
    else:
        occ_date = datetime.date(now.year, 2, 30) - datetime.timedelta(days=7)
else:
    if now.day >= 23:
        next_month = now.replace(day=28) + datetime.timedelta(days=4)
        occ_date = next_month.replace(day=30) - datetime.timedelta(days=10)
    else:
        occ_date = now.replace(day=30) - datetime.timedelta(days=7)

# Check if the current date is equal to or after the calculated date
if now >= occ_date:
# Get all the occupants
    occupants = Occupant.objects.all()

    # Loop through the occupants and send an email to each one
    for occupant in occupants:
        # Get the PSU email address of the occupant
        email = occupant.person.psu_email.strip()

        # Skip any invalid email addresses
        if not email:
            continue

        # Render the HTML email template with occupant-specific data
        html_body = render_to_string("due_email.html", {'occupant': occupant})

        # Create and send the email to the occupant
        message = EmailMultiAlternatives(
            subject='PSU Dorm Successful Occupant',
            body="mail testing",
            from_email='settings.EMAIL_HOST_USER',
            to=[email]
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)

# End Date Email Notification

# Calculate the number of days before the due date
num_days_before_due_date = 8

# Calculate the due date by adding the number of days to the current date
due_date = timezone.now() + timedelta(days=num_days_before_due_date)

# Filter the queryset of occupants to only include those that are within the desired number of days before the due date
occupants = Occupant.objects.filter(end_date__lte=due_date, end_date__gte=timezone.now())

# Iterate over the occupants and add an alert message to the list for each one
for occupant in occupants:
    days_until_due_date = (occupant.end_date - timezone.now()).days

    if days_until_due_date == 7 | days_until_due_date == 3  | days_until_due_date == 1:
        # Render the email template
        html_body = render_to_string("end_email.html", {'occupant': occupant})

        # Create the email message
        message = EmailMultiAlternatives(
            subject='PSU Dorm End of Contract',
            body="mail testing",
            from_email='settings.EMAIL_HOST_USER',
            to=[occupant.person.psu_email]
        )
        message.attach_alternative(html_body, "text/html")

        # Send the email
        message.send(fail_silently=False)




