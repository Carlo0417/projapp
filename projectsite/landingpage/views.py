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

import os

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


# ===================================================
# Start of Superadmin
# ===================================================

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
            
        # Students Gender Charts
        male_no = Person.objects.filter(gender="Male").count()
        male_no = int(male_no)

        female_no = Person.objects.filter(gender="Female").count()
        female_no = int(female_no)

        lgbt_no = Person.objects.filter(gender="LGBTQIA+").count()
        lgbt_no = int(lgbt_no)

        gender_list = ['Male', 'Female', 'LGBTQIA+']
        gender_number = [male_no, female_no, lgbt_no]

        context['gender_list'] = gender_list
        context['gender_number'] = gender_number

                
        # Monthly Registration Charts
        Jan_Reg = Person.objects.filter(created_at__icontains="2023-01").count()
        Jan_Reg = int(Jan_Reg)

        Feb_Reg = Person.objects.filter(created_at__icontains="2023-02").count()
        Feb_Reg = int(Feb_Reg)

        Mar_Reg = Person.objects.filter(created_at__icontains="2023-03").count()
        Mar_Reg = int(Mar_Reg)

        Apr_Reg = Person.objects.filter(created_at__icontains="2023-04").count()
        Apr_Reg = int(Apr_Reg)

        May_Reg = Person.objects.filter(created_at__icontains="2023-05").count()
        May_Reg = int(May_Reg)

        Jun_Reg = Person.objects.filter(created_at__icontains="2023-06").count()
        Jun_Reg = int(Jun_Reg)

        Jul_Reg = Person.objects.filter(created_at__icontains="2023-07").count()
        Jul_Reg = int(Jul_Reg)

        Aug_Reg = Person.objects.filter(created_at__icontains="2023-08").count()
        Aug_Reg = int(Aug_Reg)

        Sep_Reg = Person.objects.filter(created_at__icontains="2023-09").count()
        Sep_Reg = int(Sep_Reg)

        Oct_Reg = Person.objects.filter(created_at__icontains="2023-10").count()
        Oct_Reg = int(Oct_Reg)

        Nov_Reg = Person.objects.filter(created_at__icontains="2023-11").count()
        Nov_Reg = int(Nov_Reg)

        Dec_Reg = Person.objects.filter(created_at__icontains="2023-12").count()
        Dec_Reg = int(Dec_Reg)

        monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_number = [Jan_Reg, Feb_Reg, Mar_Reg, Apr_Reg, May_Reg, Jun_Reg, Jul_Reg, Aug_Reg, Sep_Reg, Oct_Reg, Nov_Reg, Dec_Reg]

        context['monthly_list'] = monthly_list
        context['monthly_number'] = monthly_number


        # Monthly Occupant Charts
        Jan = Occupant.objects.filter(created_at__icontains="2023-01").count()
        Jan = int(Jan)

        Feb = Occupant.objects.filter(created_at__icontains="2023-02").count()
        Feb = int(Feb)

        Mar = Occupant.objects.filter(created_at__icontains="2023-03").count()
        Mar = int(Mar)

        Apr = Occupant.objects.filter(created_at__icontains="2023-04").count()
        Apr = int(Apr)

        May = Occupant.objects.filter(created_at__icontains="2023-05").count()
        May = int(May)

        Jun = Occupant.objects.filter(created_at__icontains="2023-06").count()
        Jun = int(Jun)

        Jul = Occupant.objects.filter(created_at__icontains="2023-07").count()
        Jul = int(Jul)

        Aug = Occupant.objects.filter(created_at__icontains="2023-08").count()
        Aug = int(Aug)

        Sep = Occupant.objects.filter(created_at__icontains="2023-09").count()
        Sep = int(Sep)

        Oct = Occupant.objects.filter(created_at__icontains="2023-10").count()
        Oct = int(Oct)

        Nov = Occupant.objects.filter(created_at__icontains="2023-11").count()
        Nov = int(Nov)

        Dec = Occupant.objects.filter(created_at__icontains="2023-12").count()
        Dec = int(Dec)

        occ_monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        occ_monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['occ_monthly_list'] = occ_monthly_list
        context['occ_monthly_number'] = occ_monthly_number


        # Monthly Male Charts
        Jan_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="Male").count()
        Jan_Male_Per = (Jan_Tot_Male / Jan) * 100 if Jan != 0 else 0
        Jan_Male_Per = int(round(Jan_Male_Per))

        Feb_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="Male").count()
        Feb_Male_Per = (Feb_Tot_Male / Feb) * 100 if Feb != 0 else 0
        Feb_Male_Per = int(round(Feb_Male_Per))

        Mar_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="Male").count()
        Mar_Male_Per = (Mar_Tot_Male / Mar) * 100 if Mar != 0 else 0
        Mar_Male_Per = int(round(Mar_Male_Per))

        Apr_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="Male").count()
        Apr_Male_Per = (Apr_Tot_Male / Apr) * 100 if Apr != 0 else 0
        Apr_Male_Per = int(round(Apr_Male_Per))

        May_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="Male").count()
        May_Male_Per = (May_Tot_Male / May) * 100 if May != 0 else 0
        May_Male_Per = int(round(May_Male_Per))

        Jun_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="Male").count()
        Jun_Male_Per = (Jun_Tot_Male / Jun) * 100 if Jun != 0 else 0
        Jun_Male_Per = int(round(Jun_Male_Per))

        Jul_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="Male").count()
        Jul_Male_Per = (Jul_Tot_Male / Jul) * 100 if Jul != 0 else 0
        Jul_Male_Per = int(round(Jul_Male_Per))

        Aug_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="Male").count()
        Aug_Male_Per = (Aug_Tot_Male / Aug) * 100 if Aug != 0 else 0
        Aug_Male_Per = int(round(Aug_Male_Per))

        Sep_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="Male").count()
        Sep_Male_Per = (Sep_Tot_Male / Sep) * 100 if Sep != 0 else 0
        Sep_Male_Per = int(round(Sep_Male_Per))

        Oct_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="Male").count()
        Oct_Male_Per = (Oct_Tot_Male / Oct) * 100 if Oct != 0 else 0
        Oct_Male_Per = int(round(Oct_Male_Per))

        Nov_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="Male").count()
        Nov_Male_Per = (Nov_Tot_Male / Nov) * 100 if Nov != 0 else 0
        Nov_Male_Per = int(round(Nov_Male_Per))

        Dec_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="Male").count()
        Dec_Male_Per = (Dec_Tot_Male / Dec) * 100 if Dec != 0 else 0
        Dec_Male_Per = int(round(Dec_Male_Per))

        male_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        male_monthly_occ_per = [Jan_Male_Per, Feb_Male_Per, Mar_Male_Per, Apr_Male_Per, May_Male_Per, Jun_Male_Per, 
                                Jul_Male_Per, Aug_Male_Per, Sep_Male_Per, Oct_Male_Per, Nov_Male_Per, Dec_Male_Per]
        
        context['male_monthly_occ_per_list'] = male_monthly_occ_per_list
        context['male_monthly_occ_per'] = male_monthly_occ_per
        

        # Monthly Female Charts
        Jan_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="Female").count()
        Jan_Female_Per = (Jan_Tot_Female / Jan) * 100 if Jan != 0 else 0
        Jan_Female_Per = int(round(Jan_Female_Per))

        Feb_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="Female").count()
        Feb_Female_Per = (Feb_Tot_Female / Feb) * 100 if Feb != 0 else 0
        Feb_Female_Per = int(round(Feb_Female_Per))

        Mar_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="Female").count()
        Mar_Female_Per = (Mar_Tot_Female / Mar) * 100 if Mar != 0 else 0
        Mar_Female_Per = int(round(Mar_Female_Per))

        Apr_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="Female").count()
        Apr_Female_Per = (Apr_Tot_Female / Apr) * 100 if Apr != 0 else 0
        Apr_Female_Per = int(round(Apr_Female_Per))

        May_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="Female").count()
        May_Female_Per = (May_Tot_Female / May) * 100 if May != 0 else 0
        May_Female_Per = int(round(May_Female_Per))

        Jun_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="Female").count()
        Jun_Female_Per = (Jun_Tot_Female / Jun) * 100 if Jun != 0 else 0
        Jun_Female_Per = int(round(Jun_Female_Per))

        Jul_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="Female").count()
        Jul_Female_Per = (Jul_Tot_Female / Jul) * 100 if Jul != 0 else 0
        Jul_Female_Per = int(round(Jul_Female_Per))

        Aug_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="Female").count()
        Aug_Female_Per = (Aug_Tot_Female / Aug) * 100 if Aug != 0 else 0
        Aug_Female_Per = int(round(Aug_Female_Per))

        Sep_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="Female").count()
        Sep_Female_Per = (Sep_Tot_Female / Sep) * 100 if Sep != 0 else 0
        Sep_Female_Per = int(round(Sep_Female_Per))

        Oct_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="Female").count()
        Oct_Female_Per = (Oct_Tot_Female/ Oct) * 100 if Oct != 0 else 0
        Oct_Female_Per = int(round(Oct_Female_Per))

        Nov_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="Female").count()
        Nov_Female_Per = (Nov_Tot_Female / Nov) * 100 if Nov != 0 else 0
        Nov_Female_Per = int(round(Nov_Female_Per))

        Dec_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="Female").count()
        Dec_Female_Per = (Dec_Tot_Female / Dec) * 100 if Dec != 0 else 0
        Dec_Female_Per = int(round(Dec_Female_Per))

        female_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        female_monthly_occ_per = [Jan_Female_Per, Feb_Female_Per, Mar_Female_Per, Apr_Female_Per, May_Female_Per, Jun_Female_Per, 
                                Jul_Female_Per, Aug_Female_Per, Sep_Female_Per, Oct_Female_Per, Nov_Female_Per, Dec_Female_Per]
        
        context['female_monthly_occ_per_list'] = female_monthly_occ_per_list
        context['female_monthly_occ_per'] = female_monthly_occ_per


        # Monthly LGBTQIA+ Charts
        Jan_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="LGBTQIA+").count()
        Jan_LGBTQIA_Per = (Jan_Tot_LGBTQIA / Jan) * 100 if Jan != 0 else 0
        Jan_LGBTQIA_Per = int(round(Jan_LGBTQIA_Per))

        Feb_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="LGBTQIA+").count()
        Feb_LGBTQIA_Per = (Feb_Tot_LGBTQIA / Feb) * 100 if Feb != 0 else 0
        Feb_LGBTQIA_Per = int(round(Feb_LGBTQIA_Per))

        Mar_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="LGBTQIA+").count()
        Mar_LGBTQIA_Per = (Mar_Tot_LGBTQIA / Mar) * 100 if Mar != 0 else 0
        Mar_LGBTQIA_Per = int(round(Mar_LGBTQIA_Per))

        Apr_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="LGBTQIA+").count()
        Apr_LGBTQIA_Per = (Apr_Tot_LGBTQIA / Apr) * 100 if Apr != 0 else 0
        Apr_LGBTQIA_Per = int(round(Apr_LGBTQIA_Per))

        May_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="LGBTQIA+").count()
        May_LGBTQIA_Per = (May_Tot_LGBTQIA / May) * 100 if May != 0 else 0
        May_LGBTQIA_Per = int(round(May_LGBTQIA_Per))

        Jun_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="LGBTQIA+").count()
        Jun_LGBTQIA_Per = (Jun_Tot_LGBTQIA / Jun) * 100 if Jun != 0 else 0
        Jun_LGBTQIA_Per = int(round(Jun_LGBTQIA_Per))

        Jul_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="LGBTQIA+").count()
        Jul_LGBTQIA_Per = (Jul_Tot_LGBTQIA / Jul) * 100 if Jul != 0 else 0
        Jul_LGBTQIA_Per = int(round(Jul_LGBTQIA_Per))

        Aug_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="LGBTQIA+").count()
        Aug_LGBTQIA_Per = (Aug_Tot_LGBTQIA / Aug) * 100 if Aug != 0 else 0
        Aug_LGBTQIA_Per = int(round(Aug_LGBTQIA_Per))

        Sep_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="LGBTQIA+").count()
        Sep_LGBTQIA_Per = (Sep_Tot_LGBTQIA / Sep) * 100 if Sep != 0 else 0
        Sep_LGBTQIA_Per = int(round(Sep_LGBTQIA_Per))

        Oct_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="LGBTQIA+").count()
        Oct_LGBTQIA_Per = (Oct_Tot_LGBTQIA/ Oct) * 100 if Oct != 0 else 0
        Oct_LGBTQIA_Per = int(round(Oct_LGBTQIA_Per))

        Nov_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="LGBTQIA+").count()
        Nov_LGBTQIA_Per = (Nov_Tot_LGBTQIA / Nov) * 100 if Nov != 0 else 0
        Nov_LGBTQIA_Per = int(round(Nov_LGBTQIA_Per))

        Dec_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="LGBTQIA+").count()
        Dec_LGBTQIA_Per = (Dec_Tot_LGBTQIA / Dec) * 100 if Dec != 0 else 0
        Dec_LGBTQIA_Per = int(round(Dec_LGBTQIA_Per))

        LGBTQIA_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        LGBTQIA_monthly_occ_per = [Jan_LGBTQIA_Per, Feb_LGBTQIA_Per, Mar_LGBTQIA_Per, Apr_LGBTQIA_Per, May_LGBTQIA_Per, Jun_LGBTQIA_Per, 
                                    Jul_LGBTQIA_Per, Aug_LGBTQIA_Per, Sep_LGBTQIA_Per, Oct_LGBTQIA_Per, Nov_LGBTQIA_Per, Dec_LGBTQIA_Per]
        
        context['LGBTQIA_monthly_occ_per_list'] = LGBTQIA_monthly_occ_per_list
        context['LGBTQIA_monthly_occ_per'] = LGBTQIA_monthly_occ_per

        
        # Monthly Unpaid Charts
        Jan_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-01", payment__isnull=False).distinct().count()
        Jan_Unpaid_Per = (Jan_Unpaid_Occ / Jan) * 100 if Jan != 0 else 0
        Jan_Unpaid_Per = int(round(Jan_Unpaid_Per))

        Feb_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-02", payment__isnull=False).distinct().count()
        Feb_Unpaid_Per = (Feb_Unpaid_Occ / Feb) * 100 if Feb != 0 else 0
        Feb_Unpaid_Per = int(round(Feb_Unpaid_Per))

        Mar_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-03", payment__isnull=False).distinct().count()
        Mar_Unpaid_Per = (Mar_Unpaid_Occ / Mar) * 100 if Mar != 0 else 0
        Mar_Unpaid_Per = int(round(Mar_Unpaid_Per))

        Apr_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-04", payment__isnull=False).distinct().count()
        Apr_Unpaid_Per = (Apr_Unpaid_Occ / Apr) * 100 if Apr != 0 else 0
        Apr_Unpaid_Per = int(round(Apr_Unpaid_Per))

        May_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-05", payment__isnull=False).distinct().count()
        May_Unpaid_Per = (May_Unpaid_Occ / May) * 100 if May != 0 else 0
        May_Unpaid_Per = int(round(May_Unpaid_Per))

        Jun_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-06", payment__isnull=False).distinct().count()
        Jun_Unpaid_Per = (Jun_Unpaid_Occ / Jun) * 100 if Jun != 0 else 0
        Jun_Unpaid_Per = int(round(Jun_Unpaid_Per))

        Jul_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-07", payment__isnull=False).distinct().count()
        Jul_Unpaid_Per = (Jul_Unpaid_Occ / Jul) * 100 if Jul != 0 else 0
        Jul_Unpaid_Per = int(round(Jul_Unpaid_Per))

        Aug_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-08", payment__isnull=False).distinct().count()
        Aug_Unpaid_Per = (Aug_Unpaid_Occ / Aug) * 100 if Aug != 0 else 0
        Aug_Unpaid_Per = int(round(Aug_Unpaid_Per))

        Sep_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-09", payment__isnull=False).distinct().count()
        Sep_Unpaid_Per = (Sep_Unpaid_Occ / Sep) * 100 if Sep != 0 else 0
        Sep_Unpaid_Per = int(round(Sep_Unpaid_Per))

        Oct_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-10", payment__isnull=False).distinct().count()
        Oct_Unpaid_Per = (Oct_Unpaid_Occ / Oct) * 100 if Oct != 0 else 0
        Oct_Unpaid_Per = int(round(Oct_Unpaid_Per))

        Nov_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-11", payment__isnull=False).distinct().count()
        Nov_Unpaid_Per = (Nov_Unpaid_Occ / Nov) * 100 if Nov != 0 else 0
        Nov_Unpaid_Per = int(round(Nov_Unpaid_Per))

        Dec_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-12", payment__isnull=False).distinct().count()
        Dec_Unpaid_Per = (Dec_Unpaid_Occ / Dec) * 100 if Dec != 0 else 0
        Dec_Unpaid_Per = int(round(Dec_Unpaid_Per))


        unpaid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        unpaid_monthly_occ_per = [Jan_Unpaid_Per, Feb_Unpaid_Per, Mar_Unpaid_Per, Apr_Unpaid_Per, May_Unpaid_Per, Jun_Unpaid_Per, 
                                Jul_Unpaid_Per, Aug_Unpaid_Per, Sep_Unpaid_Per, Oct_Unpaid_Per, Nov_Unpaid_Per, Dec_Unpaid_Per]
        
        context['unpaid_monthly_occ_per_list'] = unpaid_monthly_occ_per_list
        context['unpaid_monthly_occ_per'] = unpaid_monthly_occ_per


        # Monthly Paid Charts

        # Partially Paid and Paid in January
        occupant_bills_jan = Occupant.objects.filter(bill_details__created_at__icontains="2023-01")\
            .annotate(total_bills_jan=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jan')\
            .distinct().order_by('person__last_name')

        occupant_payments_jan = Occupant.objects.filter(payment__created_at__icontains="2023-01")\
            .annotate(total_payments_jan=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jan')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jan = 0
        occupants_with_zero_or_negative_balance_jan = 0

        for occupant_bill_jan in occupant_bills_jan:
            total_payments_jan = 0
            for occupant_payment_jan in occupant_payments_jan:
                if occupant_payment_jan['id'] == occupant_bill_jan['id']:
                    total_payments_jan = occupant_payment_jan['total_payments_jan']
                    break
            remaining_balance_jan = occupant_bill_jan['total_bills_jan'] - total_payments_jan
            if remaining_balance_jan > 0 and total_payments_jan > 0:
                occupants_with_balance_jan += 1
            if remaining_balance_jan <= 0:
                occupants_with_zero_or_negative_balance_jan += 1

        Jan_PatiallyPaid_Per = (occupants_with_balance_jan / Jan) * 100 if Jan != 0 else 0
        Jan_PatiallyPaid_Per = int(round(Jan_PatiallyPaid_Per))

        Jan_Paid_Per = (occupants_with_zero_or_negative_balance_jan / Jan) * 100 if Jan != 0 else 0
        Jan_Paid_Per = int(round(Jan_Paid_Per))


        # Partially Paid and Paid in February
        occupant_bills_feb = Occupant.objects.filter(bill_details__created_at__icontains="2023-02")\
            .annotate(total_bills_feb=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_feb')\
            .distinct().order_by('person__last_name')

        occupant_payments_feb = Occupant.objects.filter(payment__created_at__icontains="2023-02")\
            .annotate(total_payments_feb=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_feb')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_feb = 0
        occupants_with_zero_or_negative_balance_feb = 0

        for occupant_bill_feb in occupant_bills_feb:
            total_payments_feb = 0
            for occupant_payment_feb in occupant_payments_feb:
                if occupant_payment_feb['id'] == occupant_bill_feb['id']:
                    total_payments_feb = occupant_payment_feb['total_payments_feb']
                    break
            remaining_balance_feb = occupant_bill_feb['total_bills_feb'] - total_payments_feb
            if remaining_balance_feb > 0 and total_payments_feb  > 0:
                occupants_with_balance_feb += 1
            if remaining_balance_feb <= 0:
                occupants_with_zero_or_negative_balance_feb += 1

        Feb_PatiallyPaid_Per = (occupants_with_balance_feb / Feb) * 100 if Feb != 0 else 0
        Feb_PatiallyPaid_Per = int(round(Feb_PatiallyPaid_Per))

        Feb_Paid_Per = (occupants_with_zero_or_negative_balance_feb / Feb) * 100 if Feb != 0 else 0
        Feb_Paid_Per = int(round(Feb_Paid_Per))


        # Partially Paid and Paid in March
        occupant_bills_mar = Occupant.objects.filter(bill_details__created_at__icontains="2023-03")\
            .annotate(total_bills_mar=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_mar')\
            .distinct().order_by('person__last_name')

        occupant_payments_mar = Occupant.objects.filter(payment__created_at__icontains="2023-03")\
            .annotate(total_payments_mar=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_mar')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_mar = 0
        occupants_with_zero_or_negative_balance_mar = 0

        for occupant_bill_mar in occupant_bills_mar:
            total_payments_mar = 0
            for occupant_payment_mar in occupant_payments_mar:
                if occupant_payment_mar['id'] == occupant_bill_mar['id']:
                    total_payments_mar = occupant_payment_mar['total_payments_mar']
                    break
            remaining_balance_mar = occupant_bill_mar['total_bills_mar'] - total_payments_mar
            if remaining_balance_mar > 0 and total_payments_mar > 0:
                occupants_with_balance_mar += 1
            if remaining_balance_mar <= 0:
                occupants_with_zero_or_negative_balance_mar += 1

        Mar_PatiallyPaid_Per = (occupants_with_balance_mar / Mar) * 100 if Mar != 0 else 0
        Mar_PatiallyPaid_Per = int(round(Mar_PatiallyPaid_Per))

        Mar_Paid_Per = (occupants_with_zero_or_negative_balance_mar / Mar) * 100 if Mar != 0 else 0
        Mar_Paid_Per = int(round(Mar_Paid_Per))


        # Partially Paid and Paid in April
        occupant_bills_apr = Occupant.objects.filter(bill_details__created_at__icontains="2023-04")\
            .annotate(total_bills_apr=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_apr')\
            .distinct().order_by('person__last_name')

        occupant_payments_apr = Occupant.objects.filter(payment__created_at__icontains="2023-04")\
            .annotate(total_payments_apr=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_apr')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_apr = 0
        occupants_with_zero_or_negative_balance_apr = 0

        for occupant_bill_apr in occupant_bills_apr:
            total_payments_apr = 0
            for occupant_payment_apr in occupant_payments_apr:
                if occupant_payment_apr['id'] == occupant_bill_apr['id']:
                    total_payments_apr = occupant_payment_apr['total_payments_apr']
                    break
            remaining_balance_apr = occupant_bill_apr['total_bills_apr'] - total_payments_apr
            if remaining_balance_apr > 0 and total_payments_apr > 0:
                occupants_with_balance_apr += 1
            if remaining_balance_apr <= 0:
                occupants_with_zero_or_negative_balance_apr += 1

        Apr_PatiallyPaid_Per = (occupants_with_balance_apr / Apr) * 100 if Apr != 0 else 0
        Apr_PatiallyPaid_Per = int(round(Apr_PatiallyPaid_Per))

        Apr_Paid_Per = (occupants_with_zero_or_negative_balance_apr / Apr) * 100 if Apr != 0 else 0
        Apr_Paid_Per = int(round(Apr_Paid_Per))


        # Partially Paid and Paid in May
        occupant_bills_may = Occupant.objects.filter(bill_details__created_at__icontains="2023-05")\
            .annotate(total_bills_may=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_may')\
            .distinct().order_by('person__last_name')

        occupant_payments_may = Occupant.objects.filter(payment__created_at__icontains="2023-05")\
            .annotate(total_payments_may=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_may')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_may = 0
        occupants_with_zero_or_negative_balance_may = 0
        
        for occupant_bill_may in occupant_bills_may:
            total_payments_may = 0
            for occupant_payment_may in occupant_payments_may:
                if occupant_payment_may['id'] == occupant_bill_may['id']:
                    total_payments_may = occupant_payment_may['total_payments_may']
                    break
            remaining_balance_may = occupant_bill_may['total_bills_may'] - total_payments_may
            if remaining_balance_may > 0 and total_payments_may > 0:
                occupants_with_balance_may += 1
            if remaining_balance_may <= 0:
                occupants_with_zero_or_negative_balance_may += 1

        May_PatiallyPaid_Per = (occupants_with_balance_may / May) * 100 if May != 0 else 0
        May_PatiallyPaid_Per = int(round(May_PatiallyPaid_Per))

        May_Paid_Per = (occupants_with_zero_or_negative_balance_may / May) * 100 if May != 0 else 0
        May_Paid_Per = int(round(May_Paid_Per))

        
        # Partially Paid and Paid in June
        occupant_bills_jun = Occupant.objects.filter(bill_details__created_at__icontains="2023-06")\
            .annotate(total_bills_jun=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jun')\
            .distinct().order_by('person__last_name')

        occupant_payments_jun = Occupant.objects.filter(payment__created_at__icontains="2023-06")\
            .annotate(total_payments_jun=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jun')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jun = 0
        occupants_with_zero_or_negative_balance_jun = 0
        
        for occupant_bill_jun in occupant_bills_jun:
            total_payments_jun = 0
            for occupant_payment_jun in occupant_payments_jun:
                if occupant_payment_jun['id'] == occupant_bill_jun['id']:
                    total_payments_jun = occupant_payment_jun['total_payments_jun']
                    break
            remaining_balance_jun = occupant_bill_jun['total_bills_jun'] - total_payments_jun
            if remaining_balance_jun > 0 and total_payments_jun > 0:
                occupants_with_balance_jun += 1
            if remaining_balance_jun <= 0:
                occupants_with_zero_or_negative_balance_jun += 1

        Jun_PatiallyPaid_Per = (occupants_with_balance_jun / Jun) * 100 if Jun != 0 else 0
        Jun_PatiallyPaid_Per = int(round(Jun_PatiallyPaid_Per))

        Jun_Paid_Per = (occupants_with_zero_or_negative_balance_jun / Jun) * 100 if Jun != 0 else 0
        Jun_Paid_Per = int(round(Jun_Paid_Per))


        # Partially Paid and Paid in July
        occupant_bills_jul = Occupant.objects.filter(bill_details__created_at__icontains="2023-07")\
            .annotate(total_bills_jul=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jul')\
            .distinct().order_by('person__last_name')

        occupant_payments_jul = Occupant.objects.filter(payment__created_at__icontains="2023-07")\
            .annotate(total_payments_jul=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jul')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jul = 0
        occupants_with_zero_or_negative_balance_jul = 0
        
        for occupant_bill_jul in occupant_bills_jul:
            total_payments_jul = 0
            for occupant_payment_jul in occupant_payments_jul:
                if occupant_payment_jul['id'] == occupant_bill_jul['id']:
                    total_payments_jul = occupant_payment_jul['total_payments_jul']
                    break
            remaining_balance_jul = occupant_bill_jul['total_bills_jul'] - total_payments_jul
            if remaining_balance_jul > 0 and total_payments_jul > 0:
                occupants_with_balance_jul += 1
            if remaining_balance_jul <= 0:
                occupants_with_zero_or_negative_balance_jul += 1

        Jul_PatiallyPaid_Per = (occupants_with_balance_jul / Jul) * 100 if Jul != 0 else 0
        Jul_PatiallyPaid_Per = int(round(Jul_PatiallyPaid_Per))

        Jul_Paid_Per = (occupants_with_zero_or_negative_balance_jul / Jul) * 100 if Jul != 0 else 0
        Jul_Paid_Per = int(round(Jul_Paid_Per))


        # Partially Paid and Paid in August
        occupant_bills_aug = Occupant.objects.filter(bill_details__created_at__icontains="2023-08")\
            .annotate(total_bills_aug=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_aug')\
            .distinct().order_by('person__last_name')

        occupant_payments_aug = Occupant.objects.filter(payment__created_at__icontains="2023-08")\
            .annotate(total_payments_aug=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_aug')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_aug = 0
        occupants_with_zero_or_negative_balance_aug = 0

        for occupant_bill_aug in occupant_bills_aug:
            total_payments_aug = 0
            for occupant_payment_aug in occupant_payments_aug:
                if occupant_payment_aug['id'] == occupant_bill_aug['id']:
                    total_payments_aug = occupant_payment_aug['total_payments_aug']
                    break
            remaining_balance_aug = occupant_bill_aug['total_bills_aug'] - total_payments_aug
            if remaining_balance_aug > 0 and total_payments_aug > 0:
                occupants_with_balance_aug += 1
            if remaining_balance_aug <= 0:
                occupants_with_zero_or_negative_balance_aug += 1

        Aug_PatiallyPaid_Per = (occupants_with_balance_aug / Aug) * 100 if Aug != 0 else 0
        Aug_PatiallyPaid_Per = int(round(Aug_PatiallyPaid_Per))

        Aug_Paid_Per = (occupants_with_zero_or_negative_balance_aug / Aug) * 100 if Aug != 0 else 0
        Aug_Paid_Per = int(round(Aug_Paid_Per))


        # Partially Paid and Paid in September
        occupant_bills_sep = Occupant.objects.filter(bill_details__created_at__icontains="2023-09")\
            .annotate(total_bills_sep=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_sep')\
            .distinct().order_by('person__last_name')

        occupant_payments_sep = Occupant.objects.filter(payment__created_at__icontains="2023-09")\
            .annotate(total_payments_sep=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_sep')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_sep = 0
        occupants_with_zero_or_negative_balance_sep = 0
        
        for occupant_bill_sep in occupant_bills_sep:
            total_payments_sep = 0
            for occupant_payment_sep in occupant_payments_sep:
                if occupant_payment_sep['id'] == occupant_bill_sep['id']:
                    total_payments_sep = occupant_payment_sep['total_payments_sep']
                    break
            remaining_balance_sep = occupant_bill_sep['total_bills_aug'] - total_payments_sep
            if remaining_balance_sep > 0 and total_payments_sep > 0:
                occupants_with_balance_sep += 1
            if remaining_balance_sep <= 0:
                occupants_with_zero_or_negative_balance_sep += 1

        Sep_PatiallyPaid_Per = (occupants_with_balance_sep / Sep) * 100 if Sep != 0 else 0
        Sep_PatiallyPaid_Per = int(round(Sep_PatiallyPaid_Per))

        Sep_Paid_Per = (occupants_with_zero_or_negative_balance_sep / Sep) * 100 if Sep != 0 else 0
        Sep_Paid_Per = int(round(Sep_Paid_Per))


        # Partially Paid and Paid in October
        occupant_bills_oct = Occupant.objects.filter(bill_details__created_at__icontains="2023-10")\
            .annotate(total_bills_oct=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_oct')\
            .distinct().order_by('person__last_name')

        occupant_payments_oct = Occupant.objects.filter(payment__created_at__icontains="2023-10")\
            .annotate(total_payments_oct=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_oct')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_oct = 0
        occupants_with_zero_or_negative_balance_oct = 0
        
        for occupant_bill_oct in occupant_bills_oct:
            total_payments_oct = 0
            for occupant_payment_oct in occupant_payments_oct:
                if occupant_payment_oct['id'] == occupant_bill_oct['id']:
                    total_payments_oct = occupant_payment_oct['total_payments_oct']
                    break
            remaining_balance_oct = occupant_bill_oct['total_bills_oct'] - total_payments_oct
            if remaining_balance_oct > 0 and total_payments_oct > 0:
                occupants_with_balance_oct += 1
            if remaining_balance_oct <= 0:
                occupants_with_zero_or_negative_balance_oct += 1

        Oct_PatiallyPaid_Per = (occupants_with_balance_oct / Oct) * 100 if Oct != 0 else 0
        Oct_PatiallyPaid_Per = int(round(Oct_PatiallyPaid_Per))

        Oct_Paid_Per = (occupants_with_zero_or_negative_balance_oct / Oct) * 100 if Oct != 0 else 0
        Oct_Paid_Per = int(round(Oct_Paid_Per))


        # Partially Paid and Paid in November
        occupant_bills_nov = Occupant.objects.filter(bill_details__created_at__icontains="2023-11")\
            .annotate(total_bills_nov=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_nov')\
            .distinct().order_by('person__last_name')

        occupant_payments_nov = Occupant.objects.filter(payment__created_at__icontains="2023-11")\
            .annotate(total_payments_nov=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_nov')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_nov = 0
        occupants_with_zero_or_negative_balance_nov = 0

        for occupant_bill_nov in occupant_bills_nov:
            total_payments_nov = 0
            for occupant_payment_nov in occupant_payments_nov:
                if occupant_payment_nov['id'] == occupant_bill_nov['id']:
                    total_payments_nov = occupant_payment_nov['total_payments_nov']
                    break
            remaining_balance_nov = occupant_bill_nov['total_bills_nov'] - total_payments_nov
            if remaining_balance_nov > 0 and total_payments_nov > 0:
                occupants_with_balance_nov += 1
            if remaining_balance_nov <= 0:
                occupants_with_zero_or_negative_balance_nov += 1

        Nov_PatiallyPaid_Per = (occupants_with_balance_nov / Nov) * 100 if Nov != 0 else 0
        Nov_PatiallyPaid_Per = int(round(Nov_PatiallyPaid_Per))

        Nov_Paid_Per = (occupants_with_zero_or_negative_balance_nov / Nov) * 100 if Nov != 0 else 0
        Nov_Paid_Per = int(round(Nov_Paid_Per))


        # Partially Paid and Paid in December
        occupant_bills_dec = Occupant.objects.filter(bill_details__created_at__icontains="2023-12")\
            .annotate(total_bills_dec=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_dec')\
            .distinct().order_by('person__last_name')

        occupant_payments_dec = Occupant.objects.filter(payment__created_at__icontains="2023-12")\
            .annotate(total_payments_dec=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_dec')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_dec = 0
        occupants_with_zero_or_negative_balance_dec = 0
        
        for occupant_bill_dec in occupant_bills_dec:
            total_payments_dec = 0
            for occupant_payment_dec in occupant_payments_dec:
                if occupant_payment_dec['id'] == occupant_bill_dec['id']:
                    total_payments_dec = occupant_payment_dec['total_payments_dec']
                    break
            remaining_balance_dec = occupant_bill_dec['total_bills_dec'] - total_payments_dec
            if remaining_balance_dec > 0 and total_payments_dec > 0:
                occupants_with_balance_dec += 1
            if remaining_balance_dec <= 0:
                occupants_with_zero_or_negative_balance_dec += 1

        Dec_PatiallyPaid_Per = (occupants_with_balance_dec / Dec) * 100 if Dec != 0 else 0
        Dec_PatiallyPaid_Per = int(round(Dec_PatiallyPaid_Per))

        Dec_Paid_Per = (occupants_with_zero_or_negative_balance_dec / Dec) * 100 if Dec != 0 else 0
        Dec_Paid_Per = int(round(Dec_Paid_Per))


        partiallypaid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        partiallypaid_monthly_occ_per = [Jan_PatiallyPaid_Per, Feb_PatiallyPaid_Per, Mar_PatiallyPaid_Per, Apr_PatiallyPaid_Per,
                                          May_PatiallyPaid_Per, Jun_PatiallyPaid_Per, Jul_PatiallyPaid_Per, Aug_PatiallyPaid_Per, 
                                          Sep_PatiallyPaid_Per, Oct_PatiallyPaid_Per, Nov_PatiallyPaid_Per, Dec_PatiallyPaid_Per]
        
        context['partiallypaid_monthly_occ_per_list'] = partiallypaid_monthly_occ_per_list
        context['partiallypaid_monthly_occ_per'] = partiallypaid_monthly_occ_per


        paid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        paid_monthly_occ_per = [Jan_Paid_Per, Feb_Paid_Per, Mar_Paid_Per, Apr_Paid_Per,
                                May_Paid_Per, Jun_Paid_Per, Jul_Paid_Per, Aug_Paid_Per, 
                                Sep_Paid_Per, Oct_Paid_Per, Nov_Paid_Per, Dec_Paid_Per]
        
        context['paid_monthly_occ_per_list'] = paid_monthly_occ_per_list
        context['paid_monthly_occ_per'] = paid_monthly_occ_per


        return context

# @method_decorator(login_required, name='dispatch')
class DashMaleVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'superadmin/dash_male_vacant_bed.html'
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
    template_name = 'superadmin/dash_female_vacant_bed.html'
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
    template_name = 'superadmin/dash_foreign_vacant_bed.html'
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
class RegistrationList(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'superadmin/registration_list.html'
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
            | Q(program__icontains=query) | Q(boarder_type__icontains=query)| Q(reg_status__iexact=query) | Q(gender__iexact=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class RegMonthRep(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'superadmin/reg_month_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = Person.objects.raw('SELECT * FROM dormitory_person WHERE MONTH(created_at) = MONTH(CURRENT_DATE()) AND YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')
        return context

# @method_decorator(login_required, name='dispatch')
class RegYearRep(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'superadmin/reg_year_rep.html'
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
    template_name = 'superadmin/registration_update.html'
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
    template_name = 'superadmin/registration_view.html'
    success_url = "/registration_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Registration details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class OccupantList(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'superadmin/occupant_list.html'
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
    template_name = 'superadmin/occupant_update.html'
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
    template_name = 'superadmin/occupant_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fetch_first_three'] = Bill_Details.objects.filter(occupant=self.object.id)[:3]
        context['billing_details'] = Bill_Details.objects.filter(occupant=self.object.id)[3:]
        context['total_bills_amount'] = Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['payment'] = Payment.objects.filter(occupant=self.object.id)
        context['total_payment_amount'] = Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['remaining_balance'] = (Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0)
        context['occupant_demerits'] = OccupantDemerit.objects.filter(occupant=self.object.id)

        cursor = connections['default'].cursor()
        query = f"UPDATE dormitory_occupantdemerit SET new_remarks = null "
        cursor.execute(query)

        return context

    def form_valid(self, form):
      messages.success(self.request, "Occupant details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class OccMonthRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'superadmin/occ_month_rep.html'
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
    template_name = 'superadmin/occ_year_rep.html'
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
class BillingList(ListView):
    model = Bill_Details
    context_object_name = 'occupant'
    template_name = 'superadmin/billing_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bills'] = Bill_Details.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BillingList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
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
    template_name = 'superadmin/billing_update.html'
    success_url = "/billing_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Billing details was updated successfully!")
      super().form_valid(form)

      service = form.cleaned_data['service']
      quantity = form.cleaned_data['quantity']
      price = Service.objects.filter(service_name=service).first()
      bill_id = form.instance.id
      total_amount = price.base_amount * quantity
            
      cursor = connections['default'].cursor()
      query = "UPDATE dormitory_bill_details SET amount = %s WHERE id = %s"
      cursor.execute(query, (total_amount, bill_id))

      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class OccupantViewBillingUpdate(UpdateView):
    model = Bill_Details
    # fields = "__all__"
    form_class = BillingForm
    context_object_name = 'occupant'
    template_name = 'superadmin/billing_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(f"ID {self.object.occupant_id}")
        return context

    def get_success_url(self):
        return reverse('OccupantView', kwargs={'pk': self.object.occupant_id})

    def form_valid(self, form):
      messages.success(self.request, "Occupant bill was updated successfully!")
      super().form_valid(form)

      service = form.cleaned_data['service']
      quantity = form.cleaned_data['quantity']
      price = Service.objects.filter(service_name=service).first()
      bill_id = form.instance.id
      total_amount = price.base_amount * quantity
            
      cursor = connections['default'].cursor()
      query = "UPDATE dormitory_bill_details SET amount = %s WHERE id = %s"
      cursor.execute(query, (total_amount, bill_id))
      
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class PaymentList(ListView):
    model = Payment
    context_object_name = 'payment'
    template_name = 'superadmin/payment_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment'] = Payment.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(PaymentList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
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
    template_name = 'superadmin/payment_update.html'
    success_url = "/payment_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Payment details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class OccupantViewPaymentUpdate(UpdateView):
    model = Payment
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'superadmin/payment_update.html'

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
class OccupantDemeritList(ListView):
    model = OccupantDemerit
    context_object_name = 'occupant'
    template_name = 'superadmin/occupant_demerit_list.html'
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
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(demerit_name__demerit_name__icontains=query)
            | Q(demerit_name__demerit_points__icontains=query) | Q(cur_date__icontains=query) | Q(prev_remarks__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class OccupantDemeritUpdateView(UpdateView):
    model = OccupantDemerit
    fields = ['prev_remarks', 'new_remarks']
    context_object_name = 'occupant'
    template_name = 'superadmin/occupant_demerit_update.html'
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

      prev_plus_new = pre_r +" \n \n " + new_r

      cursor = connections['default'].cursor()
      query = "UPDATE dormitory_occupantdemerit SET prev_remarks = %s WHERE id = %s"
      params = (prev_plus_new, occ_id)
      cursor.execute(query, params)
      return HttpResponseRedirect(self.get_success_url())
  
# @method_decorator(login_required, name='dispatch')
class OccupantViewDemeritUpdate(UpdateView):
    model = OccupantDemerit
    fields = ['prev_remarks', 'new_remarks']
    context_object_name = 'occupant'
    template_name = 'superadmin/occupant_demerit_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('OccupantView', kwargs={'pk': self.object.occupant_id})

    def form_valid(self, form):
        messages.success(self.request, "Occupant demerit was updated successfully!")
        super().form_valid(form)

        occ_id = form.instance.id
        pre_r = form.cleaned_data.get('prev_remarks')
        new_r = form.cleaned_data.get('new_remarks')

        prev_plus_new = pre_r +" \n \n " + new_r

        cursor = connections['default'].cursor()
        query = "UPDATE dormitory_occupantdemerit SET prev_remarks = %s WHERE id = %s"
        params = (prev_plus_new, occ_id)
        cursor.execute(query, params)

        return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class RoomList(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'superadmin/room_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(RoomList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(room_name__iexact=query) | Q(floorlvl__icontains=query) 
                | Q(dorm_name__icontains=query) | Q(description__icontains=query))
        
        # Annotate the queryset after the search filter has been applied
        qs = qs.annotate(
            TotalBeds=Count('bed'), 
            TotalVacant=Count('bed', filter=Q(bed__bed_status='Vacant'))
        ).order_by('created_at')
        
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
    template_name = 'superadmin/room_list_card.html'
    paginate_by = 9
    
    def get_queryset(self, *args, **kwargs):
        qs = super(RoomListCard, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(room_name__iexact=query) | Q(floorlvl__icontains=query) 
                | Q(dorm_name__icontains=query) | Q(description__icontains=query))
        
        # Annotate the queryset after the search filter has been applied
        qs = qs.annotate(
            TotalBeds=Count('bed'), 
            TotalVacant=Count('bed', filter=Q(bed__bed_status='Vacant')),
            TotalOccupied=Count('bed', filter=Q(bed__bed_status='Occupied')),
            TotalUnder=Count('bed', filter=Q(bed__bed_status='Under Maint.')),
        ).order_by('created_at')
        
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
    template_name = 'superadmin/room_update.html'
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
    template_name = 'superadmin/room_update.html'
    success_url = "/room_list_card"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Room details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class BedList(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'superadmin/bed_list.html'
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
    template_name = 'superadmin/bed_update.html'
    success_url = "/bed_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Bed details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class ServiceList(ListView):
    model = Service
    context_object_name = 'service'
    template_name = 'superadmin/service_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services']= Service.objects.all().exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others').count()
        context['available'] = Service.objects.filter(status__iexact="Available").exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others').count()
        context['notavailable'] = Service.objects.filter(status__iexact="Not Available").count()
        context['services_limit'] = Service.objects.all().exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others')
    
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ServiceList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("service_name").filter(Q(service_name__icontains=query) | Q(status__icontains=query)
            | Q(base_amount__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class ServiceUpdateView(UpdateView):
    model = Service
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'superadmin/service_update.html'
    success_url = "/service_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Service details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class DemeritList(ListView):
    model = Demerit
    context_object_name = 'demerit'
    template_name = 'superadmin/demerit_list.html'
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
    template_name = 'superadmin/demerit_update.html'
    success_url = "/demerit_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Demerit details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())
 

# @method_decorator(login_required, name='dispatch')
class AdminList(ListView):
    model = Admin
    context_object_name = 'admins'
    template_name = 'superadmin/admin_list.html'
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
    template_name = 'superadmin/admin_update.html'
    success_url = "/admin_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Admin account was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())
    

# @method_decorator(login_required, name='dispatch')
class OccupantAccounts(ListView):
    model = User
    context_object_name = 'users'
    template_name = "superadmin/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = User.objects.count()
        context['active'] = User.objects.filter(user_status__iexact="active").count()
        context['inactive'] = User.objects.filter(user_status__iexact="inactive").count()

        # cursor = connections['default'].cursor()
        # query = "DELETE FROM dormitory_user WHERE person_id NOT IN (SELECT person_id FROM dormitory_person)"
        # cursor.execute(query)
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
    template_name = 'superadmin/users_update.html'
    success_url = "/users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Occupant account was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class AdminProfile(ListView):
    model = Admin
    context_object_name = 'admin'
    template_name = "superadmin/admin_profile.html"

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
    template_name = 'superadmin/admin_profile_update.html'
    success_url = "/admin_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Your Account Information was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# ===================================================
# End of Superadmin
# ===================================================


# ===================================================
# Start of Frontdesk
# ===================================================
# @method_decorator(login_required, name='dispatch')
class FDHomePageView(ListView):
    model = Room
    context_object_name = 'room'
    template_name = "landingpage/fd_home.html"

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
            
        # Students Gender Charts
        male_no = Person.objects.filter(gender="Male").count()
        male_no = int(male_no)

        female_no = Person.objects.filter(gender="Female").count()
        female_no = int(female_no)

        lgbt_no = Person.objects.filter(gender="LGBTQIA+").count()
        lgbt_no = int(lgbt_no)

        gender_list = ['Male', 'Female', 'LGBTQIA+']
        gender_number = [male_no, female_no, lgbt_no]

        context['gender_list'] = gender_list
        context['gender_number'] = gender_number

                
        # Monthly Registration Charts
        Jan_Reg = Person.objects.filter(created_at__icontains="2023-01").count()
        Jan_Reg = int(Jan_Reg)

        Feb_Reg = Person.objects.filter(created_at__icontains="2023-02").count()
        Feb_Reg = int(Feb_Reg)

        Mar_Reg = Person.objects.filter(created_at__icontains="2023-03").count()
        Mar_Reg = int(Mar_Reg)

        Apr_Reg = Person.objects.filter(created_at__icontains="2023-04").count()
        Apr_Reg = int(Apr_Reg)

        May_Reg = Person.objects.filter(created_at__icontains="2023-05").count()
        May_Reg = int(May_Reg)

        Jun_Reg = Person.objects.filter(created_at__icontains="2023-06").count()
        Jun_Reg = int(Jun_Reg)

        Jul_Reg = Person.objects.filter(created_at__icontains="2023-07").count()
        Jul_Reg = int(Jul_Reg)

        Aug_Reg = Person.objects.filter(created_at__icontains="2023-08").count()
        Aug_Reg = int(Aug_Reg)

        Sep_Reg = Person.objects.filter(created_at__icontains="2023-09").count()
        Sep_Reg = int(Sep_Reg)

        Oct_Reg = Person.objects.filter(created_at__icontains="2023-10").count()
        Oct_Reg = int(Oct_Reg)

        Nov_Reg = Person.objects.filter(created_at__icontains="2023-11").count()
        Nov_Reg = int(Nov_Reg)

        Dec_Reg = Person.objects.filter(created_at__icontains="2023-12").count()
        Dec_Reg = int(Dec_Reg)

        monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_number = [Jan_Reg, Feb_Reg, Mar_Reg, Apr_Reg, May_Reg, Jun_Reg, Jul_Reg, Aug_Reg, Sep_Reg, Oct_Reg, Nov_Reg, Dec_Reg]

        context['monthly_list'] = monthly_list
        context['monthly_number'] = monthly_number


        # Monthly Occupant Charts
        Jan = Occupant.objects.filter(created_at__icontains="2023-01").count()
        Jan = int(Jan)

        Feb = Occupant.objects.filter(created_at__icontains="2023-02").count()
        Feb = int(Feb)

        Mar = Occupant.objects.filter(created_at__icontains="2023-03").count()
        Mar = int(Mar)

        Apr = Occupant.objects.filter(created_at__icontains="2023-04").count()
        Apr = int(Apr)

        May = Occupant.objects.filter(created_at__icontains="2023-05").count()
        May = int(May)

        Jun = Occupant.objects.filter(created_at__icontains="2023-06").count()
        Jun = int(Jun)

        Jul = Occupant.objects.filter(created_at__icontains="2023-07").count()
        Jul = int(Jul)

        Aug = Occupant.objects.filter(created_at__icontains="2023-08").count()
        Aug = int(Aug)

        Sep = Occupant.objects.filter(created_at__icontains="2023-09").count()
        Sep = int(Sep)

        Oct = Occupant.objects.filter(created_at__icontains="2023-10").count()
        Oct = int(Oct)

        Nov = Occupant.objects.filter(created_at__icontains="2023-11").count()
        Nov = int(Nov)

        Dec = Occupant.objects.filter(created_at__icontains="2023-12").count()
        Dec = int(Dec)

        occ_monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        occ_monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['occ_monthly_list'] = occ_monthly_list
        context['occ_monthly_number'] = occ_monthly_number


        # Monthly Male Charts
        Jan_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="Male").count()
        Jan_Male_Per = (Jan_Tot_Male / Jan) * 100 if Jan != 0 else 0
        Jan_Male_Per = int(round(Jan_Male_Per))

        Feb_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="Male").count()
        Feb_Male_Per = (Feb_Tot_Male / Feb) * 100 if Feb != 0 else 0
        Feb_Male_Per = int(round(Feb_Male_Per))

        Mar_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="Male").count()
        Mar_Male_Per = (Mar_Tot_Male / Mar) * 100 if Mar != 0 else 0
        Mar_Male_Per = int(round(Mar_Male_Per))

        Apr_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="Male").count()
        Apr_Male_Per = (Apr_Tot_Male / Apr) * 100 if Apr != 0 else 0
        Apr_Male_Per = int(round(Apr_Male_Per))

        May_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="Male").count()
        May_Male_Per = (May_Tot_Male / May) * 100 if May != 0 else 0
        May_Male_Per = int(round(May_Male_Per))

        Jun_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="Male").count()
        Jun_Male_Per = (Jun_Tot_Male / Jun) * 100 if Jun != 0 else 0
        Jun_Male_Per = int(round(Jun_Male_Per))

        Jul_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="Male").count()
        Jul_Male_Per = (Jul_Tot_Male / Jul) * 100 if Jul != 0 else 0
        Jul_Male_Per = int(round(Jul_Male_Per))

        Aug_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="Male").count()
        Aug_Male_Per = (Aug_Tot_Male / Aug) * 100 if Aug != 0 else 0
        Aug_Male_Per = int(round(Aug_Male_Per))

        Sep_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="Male").count()
        Sep_Male_Per = (Sep_Tot_Male / Sep) * 100 if Sep != 0 else 0
        Sep_Male_Per = int(round(Sep_Male_Per))

        Oct_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="Male").count()
        Oct_Male_Per = (Oct_Tot_Male / Oct) * 100 if Oct != 0 else 0
        Oct_Male_Per = int(round(Oct_Male_Per))

        Nov_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="Male").count()
        Nov_Male_Per = (Nov_Tot_Male / Nov) * 100 if Nov != 0 else 0
        Nov_Male_Per = int(round(Nov_Male_Per))

        Dec_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="Male").count()
        Dec_Male_Per = (Dec_Tot_Male / Dec) * 100 if Dec != 0 else 0
        Dec_Male_Per = int(round(Dec_Male_Per))

        male_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        male_monthly_occ_per = [Jan_Male_Per, Feb_Male_Per, Mar_Male_Per, Apr_Male_Per, May_Male_Per, Jun_Male_Per, 
                                Jul_Male_Per, Aug_Male_Per, Sep_Male_Per, Oct_Male_Per, Nov_Male_Per, Dec_Male_Per]
        
        context['male_monthly_occ_per_list'] = male_monthly_occ_per_list
        context['male_monthly_occ_per'] = male_monthly_occ_per
        

        # Monthly Female Charts
        Jan_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="Female").count()
        Jan_Female_Per = (Jan_Tot_Female / Jan) * 100 if Jan != 0 else 0
        Jan_Female_Per = int(round(Jan_Female_Per))

        Feb_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="Female").count()
        Feb_Female_Per = (Feb_Tot_Female / Feb) * 100 if Feb != 0 else 0
        Feb_Female_Per = int(round(Feb_Female_Per))

        Mar_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="Female").count()
        Mar_Female_Per = (Mar_Tot_Female / Mar) * 100 if Mar != 0 else 0
        Mar_Female_Per = int(round(Mar_Female_Per))

        Apr_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="Female").count()
        Apr_Female_Per = (Apr_Tot_Female / Apr) * 100 if Apr != 0 else 0
        Apr_Female_Per = int(round(Apr_Female_Per))

        May_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="Female").count()
        May_Female_Per = (May_Tot_Female / May) * 100 if May != 0 else 0
        May_Female_Per = int(round(May_Female_Per))

        Jun_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="Female").count()
        Jun_Female_Per = (Jun_Tot_Female / Jun) * 100 if Jun != 0 else 0
        Jun_Female_Per = int(round(Jun_Female_Per))

        Jul_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="Female").count()
        Jul_Female_Per = (Jul_Tot_Female / Jul) * 100 if Jul != 0 else 0
        Jul_Female_Per = int(round(Jul_Female_Per))

        Aug_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="Female").count()
        Aug_Female_Per = (Aug_Tot_Female / Aug) * 100 if Aug != 0 else 0
        Aug_Female_Per = int(round(Aug_Female_Per))

        Sep_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="Female").count()
        Sep_Female_Per = (Sep_Tot_Female / Sep) * 100 if Sep != 0 else 0
        Sep_Female_Per = int(round(Sep_Female_Per))

        Oct_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="Female").count()
        Oct_Female_Per = (Oct_Tot_Female/ Oct) * 100 if Oct != 0 else 0
        Oct_Female_Per = int(round(Oct_Female_Per))

        Nov_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="Female").count()
        Nov_Female_Per = (Nov_Tot_Female / Nov) * 100 if Nov != 0 else 0
        Nov_Female_Per = int(round(Nov_Female_Per))

        Dec_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="Female").count()
        Dec_Female_Per = (Dec_Tot_Female / Dec) * 100 if Dec != 0 else 0
        Dec_Female_Per = int(round(Dec_Female_Per))

        female_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        female_monthly_occ_per = [Jan_Female_Per, Feb_Female_Per, Mar_Female_Per, Apr_Female_Per, May_Female_Per, Jun_Female_Per, 
                                Jul_Female_Per, Aug_Female_Per, Sep_Female_Per, Oct_Female_Per, Nov_Female_Per, Dec_Female_Per]
        
        context['female_monthly_occ_per_list'] = female_monthly_occ_per_list
        context['female_monthly_occ_per'] = female_monthly_occ_per


        # Monthly LGBTQIA+ Charts
        Jan_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="LGBTQIA+").count()
        Jan_LGBTQIA_Per = (Jan_Tot_LGBTQIA / Jan) * 100 if Jan != 0 else 0
        Jan_LGBTQIA_Per = int(round(Jan_LGBTQIA_Per))

        Feb_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="LGBTQIA+").count()
        Feb_LGBTQIA_Per = (Feb_Tot_LGBTQIA / Feb) * 100 if Feb != 0 else 0
        Feb_LGBTQIA_Per = int(round(Feb_LGBTQIA_Per))

        Mar_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="LGBTQIA+").count()
        Mar_LGBTQIA_Per = (Mar_Tot_Female / Mar) * 100 if Mar != 0 else 0
        Mar_LGBTQIA_Per = int(round(Mar_LGBTQIA_Per))

        Apr_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="LGBTQIA+").count()
        Apr_LGBTQIA_Per = (Apr_Tot_LGBTQIA / Apr) * 100 if Apr != 0 else 0
        Apr_LGBTQIA_Per = int(round(Apr_LGBTQIA_Per))

        May_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="LGBTQIA+").count()
        May_LGBTQIA_Per = (May_Tot_LGBTQIA / May) * 100 if May != 0 else 0
        May_LGBTQIA_Per = int(round(May_LGBTQIA_Per))

        Jun_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="LGBTQIA+").count()
        Jun_LGBTQIA_Per = (Jun_Tot_LGBTQIA / Jun) * 100 if Jun != 0 else 0
        Jun_LGBTQIA_Per = int(round(Jun_LGBTQIA_Per))

        Jul_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="LGBTQIA+").count()
        Jul_LGBTQIA_Per = (Jul_Tot_LGBTQIA / Jul) * 100 if Jul != 0 else 0
        Jul_LGBTQIA_Per = int(round(Jul_LGBTQIA_Per))

        Aug_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="LGBTQIA+").count()
        Aug_LGBTQIA_Per = (Aug_Tot_LGBTQIA / Aug) * 100 if Aug != 0 else 0
        Aug_LGBTQIA_Per = int(round(Aug_LGBTQIA_Per))

        Sep_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="LGBTQIA+").count()
        Sep_LGBTQIA_Per = (Sep_Tot_LGBTQIA / Sep) * 100 if Sep != 0 else 0
        Sep_LGBTQIA_Per = int(round(Sep_LGBTQIA_Per))

        Oct_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="LGBTQIA+").count()
        Oct_LGBTQIA_Per = (Oct_Tot_LGBTQIA/ Oct) * 100 if Oct != 0 else 0
        Oct_LGBTQIA_Per = int(round(Oct_LGBTQIA_Per))

        Nov_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="LGBTQIA+").count()
        Nov_LGBTQIA_Per = (Nov_Tot_LGBTQIA / Nov) * 100 if Nov != 0 else 0
        Nov_LGBTQIA_Per = int(round(Nov_LGBTQIA_Per))

        Dec_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="LGBTQIA+").count()
        Dec_LGBTQIA_Per = (Dec_Tot_LGBTQIA / Dec) * 100 if Dec != 0 else 0
        Dec_LGBTQIA_Per = int(round(Dec_LGBTQIA_Per))

        LGBTQIA_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        LGBTQIA_monthly_occ_per = [Jan_LGBTQIA_Per, Feb_LGBTQIA_Per, Mar_LGBTQIA_Per, Apr_LGBTQIA_Per, May_LGBTQIA_Per, Jun_LGBTQIA_Per, 
                                    Jul_LGBTQIA_Per, Aug_LGBTQIA_Per, Sep_LGBTQIA_Per, Oct_LGBTQIA_Per, Nov_LGBTQIA_Per, Dec_LGBTQIA_Per]
        
        context['LGBTQIA_monthly_occ_per_list'] = LGBTQIA_monthly_occ_per_list
        context['LGBTQIA_monthly_occ_per'] = LGBTQIA_monthly_occ_per

        
        # Monthly Unpaid Charts
        Jan_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-01", payment__isnull=False).distinct().count()
        Jan_Unpaid_Per = (Jan_Unpaid_Occ / Jan) * 100 if Jan != 0 else 0
        Jan_Unpaid_Per = int(round(Jan_Unpaid_Per))

        Feb_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-02", payment__isnull=False).distinct().count()
        Feb_Unpaid_Per = (Feb_Unpaid_Occ / Feb) * 100 if Feb != 0 else 0
        Feb_Unpaid_Per = int(round(Feb_Unpaid_Per))

        Mar_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-03", payment__isnull=False).distinct().count()
        Mar_Unpaid_Per = (Mar_Unpaid_Occ / Mar) * 100 if Mar != 0 else 0
        Mar_Unpaid_Per = int(round(Mar_Unpaid_Per))

        Apr_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-04", payment__isnull=False).distinct().count()
        Apr_Unpaid_Per = (Apr_Unpaid_Occ / Apr) * 100 if Apr != 0 else 0
        Apr_Unpaid_Per = int(round(Apr_Unpaid_Per))

        May_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-05", payment__isnull=False).distinct().count()
        May_Unpaid_Per = (May_Unpaid_Occ / May) * 100 if May != 0 else 0
        May_Unpaid_Per = int(round(May_Unpaid_Per))

        Jun_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-06", payment__isnull=False).distinct().count()
        Jun_Unpaid_Per = (Jun_Unpaid_Occ / Jun) * 100 if Jun != 0 else 0
        Jun_Unpaid_Per = int(round(Jun_Unpaid_Per))

        Jul_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-07", payment__isnull=False).distinct().count()
        Jul_Unpaid_Per = (Jul_Unpaid_Occ / Jul) * 100 if Jul != 0 else 0
        Jul_Unpaid_Per = int(round(Jul_Unpaid_Per))

        Aug_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-08", payment__isnull=False).distinct().count()
        Aug_Unpaid_Per = (Aug_Unpaid_Occ / Aug) * 100 if Aug != 0 else 0
        Aug_Unpaid_Per = int(round(Aug_Unpaid_Per))

        Sep_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-09", payment__isnull=False).distinct().count()
        Sep_Unpaid_Per = (Sep_Unpaid_Occ / Sep) * 100 if Sep != 0 else 0
        Sep_Unpaid_Per = int(round(Sep_Unpaid_Per))

        Oct_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-10", payment__isnull=False).distinct().count()
        Oct_Unpaid_Per = (Oct_Unpaid_Occ / Oct) * 100 if Oct != 0 else 0
        Oct_Unpaid_Per = int(round(Oct_Unpaid_Per))

        Nov_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-11", payment__isnull=False).distinct().count()
        Nov_Unpaid_Per = (Nov_Unpaid_Occ / Nov) * 100 if Nov != 0 else 0
        Nov_Unpaid_Per = int(round(Nov_Unpaid_Per))

        Dec_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-12", payment__isnull=False).distinct().count()
        Dec_Unpaid_Per = (Dec_Unpaid_Occ / Dec) * 100 if Dec != 0 else 0
        Dec_Unpaid_Per = int(round(Dec_Unpaid_Per))


        unpaid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        unpaid_monthly_occ_per = [Jan_Unpaid_Per, Feb_Unpaid_Per, Mar_Unpaid_Per, Apr_Unpaid_Per, May_Unpaid_Per, Jun_Unpaid_Per, 
                                Jul_Unpaid_Per, Aug_Unpaid_Per, Sep_Unpaid_Per, Oct_Unpaid_Per, Nov_Unpaid_Per, Dec_Unpaid_Per]
        
        context['unpaid_monthly_occ_per_list'] = unpaid_monthly_occ_per_list
        context['unpaid_monthly_occ_per'] = unpaid_monthly_occ_per


        # Monthly Paid Charts

        # Partially Paid and Paid in January
        occupant_bills_jan = Occupant.objects.filter(bill_details__created_at__icontains="2023-01")\
            .annotate(total_bills_jan=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jan')\
            .distinct().order_by('person__last_name')

        occupant_payments_jan = Occupant.objects.filter(payment__created_at__icontains="2023-01")\
            .annotate(total_payments_jan=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jan')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jan = 0
        occupants_with_zero_or_negative_balance_jan = 0

        for occupant_bill_jan in occupant_bills_jan:
            total_payments_jan = 0
            for occupant_payment_jan in occupant_payments_jan:
                if occupant_payment_jan['id'] == occupant_bill_jan['id']:
                    total_payments_jan = occupant_payment_jan['total_payments_jan']
                    break
            remaining_balance_jan = occupant_bill_jan['total_bills_jan'] - total_payments_jan
            if remaining_balance_jan > 0:
                occupants_with_balance_jan += 1
            else:
                occupants_with_zero_or_negative_balance_jan += 1

        Jan_PatiallyPaid_Per = (occupants_with_balance_jan / Jan) * 100 if Jan != 0 else 0
        Jan_PatiallyPaid_Per = int(round(Jan_PatiallyPaid_Per))

        Jan_Paid_Per = (occupants_with_zero_or_negative_balance_jan / Jan) * 100 if Jan != 0 else 0
        Jan_Paid_Per = int(round(Jan_Paid_Per))


        # Partially Paid and Paid in February
        occupant_bills_feb = Occupant.objects.filter(bill_details__created_at__icontains="2023-02")\
            .annotate(total_bills_feb=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_feb')\
            .distinct().order_by('person__last_name')

        occupant_payments_feb = Occupant.objects.filter(payment__created_at__icontains="2023-02")\
            .annotate(total_payments_feb=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_feb')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_feb = 0
        occupants_with_zero_or_negative_balance_feb = 0

        for occupant_bill_feb in occupant_bills_feb:
            total_payments_feb = 0
            for occupant_payment_feb in occupant_payments_feb:
                if occupant_payment_feb['id'] == occupant_bill_feb['id']:
                    total_payments_feb = occupant_payment_feb['total_payments_feb']
                    break
            remaining_balance_feb = occupant_bill_feb['total_bills_feb'] - total_payments_feb
            if remaining_balance_feb > 0:
                occupants_with_balance_feb += 1
            else:
                occupants_with_zero_or_negative_balance_feb += 1

        Feb_PatiallyPaid_Per = (occupants_with_balance_feb / Feb) * 100 if Feb != 0 else 0
        Feb_PatiallyPaid_Per = int(round(Feb_PatiallyPaid_Per))

        Feb_Paid_Per = (occupants_with_zero_or_negative_balance_feb / Feb) * 100 if Feb != 0 else 0
        Feb_Paid_Per = int(round(Feb_Paid_Per))


        # Partially Paid and Paid in March
        occupant_bills_mar = Occupant.objects.filter(bill_details__created_at__icontains="2023-03")\
            .annotate(total_bills_mar=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_mar')\
            .distinct().order_by('person__last_name')

        occupant_payments_mar = Occupant.objects.filter(payment__created_at__icontains="2023-03")\
            .annotate(total_payments_mar=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_mar')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_mar = 0
        occupants_with_zero_or_negative_balance_mar = 0

        for occupant_bill_mar in occupant_bills_mar:
            total_payments_mar = 0
            for occupant_payment_mar in occupant_payments_mar:
                if occupant_payment_mar['id'] == occupant_bill_mar['id']:
                    total_payments_mar = occupant_payment_mar['total_payments_mar']
                    break
            remaining_balance_mar = occupant_bill_mar['total_bills_mar'] - total_payments_mar
            if remaining_balance_mar > 0:
                occupants_with_balance_mar += 1
            else:
                occupants_with_zero_or_negative_balance_mar += 1

        Mar_PatiallyPaid_Per = (occupants_with_balance_mar / Mar) * 100 if Mar != 0 else 0
        Mar_PatiallyPaid_Per = int(round(Mar_PatiallyPaid_Per))

        Mar_Paid_Per = (occupants_with_zero_or_negative_balance_mar / Mar) * 100 if Mar != 0 else 0
        Mar_Paid_Per = int(round(Mar_Paid_Per))


        # Partially Paid and Paid in April
        occupant_bills_apr = Occupant.objects.filter(bill_details__created_at__icontains="2023-04")\
            .annotate(total_bills_apr=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_apr')\
            .distinct().order_by('person__last_name')

        occupant_payments_apr = Occupant.objects.filter(payment__created_at__icontains="2023-04")\
            .annotate(total_payments_apr=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_apr')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_apr = 0
        occupants_with_zero_or_negative_balance_apr = 0

        for occupant_bill_apr in occupant_bills_apr:
            total_payments_apr = 0
            for occupant_payment_apr in occupant_payments_apr:
                if occupant_payment_apr['id'] == occupant_bill_apr['id']:
                    total_payments_apr = occupant_payment_apr['total_payments_apr']
                    break
            remaining_balance_apr = occupant_bill_apr['total_bills_apr'] - total_payments_apr
            if remaining_balance_apr > 0:
                occupants_with_balance_apr += 1
            else:
                occupants_with_zero_or_negative_balance_apr += 1

        Apr_PatiallyPaid_Per = (occupants_with_balance_apr / Apr) * 100 if Apr != 0 else 0
        Apr_PatiallyPaid_Per = int(round(Apr_PatiallyPaid_Per))

        Apr_Paid_Per = (occupants_with_zero_or_negative_balance_apr / Apr) * 100 if Apr != 0 else 0
        Apr_Paid_Per = int(round(Apr_Paid_Per))


        # Partially Paid and Paid in May
        occupant_bills_may = Occupant.objects.filter(bill_details__created_at__icontains="2023-05")\
            .annotate(total_bills_may=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_may')\
            .distinct().order_by('person__last_name')

        occupant_payments_may = Occupant.objects.filter(payment__created_at__icontains="2023-05")\
            .annotate(total_payments_may=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_may')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_may = 0
        occupants_with_zero_or_negative_balance_may = 0
        
        for occupant_bill_may in occupant_bills_may:
            total_payments_may = 0
            for occupant_payment_may in occupant_payments_may:
                if occupant_payment_may['id'] == occupant_bill_may['id']:
                    total_payments_may = occupant_payment_may['total_payments_may']
                    break
            remaining_balance_may = occupant_bill_may['total_bills_may'] - total_payments_may
            if remaining_balance_may > 0:
                occupants_with_balance_may += 1
            else:
                occupants_with_zero_or_negative_balance_may += 1

        May_PatiallyPaid_Per = (occupants_with_balance_may / May) * 100 if May != 0 else 0
        May_PatiallyPaid_Per = int(round(May_PatiallyPaid_Per))

        May_Paid_Per = (occupants_with_zero_or_negative_balance_may / May) * 100 if May != 0 else 0
        May_Paid_Per = int(round(May_Paid_Per))

        
        # Partially Paid and Paid in June
        occupant_bills_jun = Occupant.objects.filter(bill_details__created_at__icontains="2023-06")\
            .annotate(total_bills_jun=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jun')\
            .distinct().order_by('person__last_name')

        occupant_payments_jun = Occupant.objects.filter(payment__created_at__icontains="2023-06")\
            .annotate(total_payments_jun=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jun')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jun = 0
        occupants_with_zero_or_negative_balance_jun = 0
        
        for occupant_bill_jun in occupant_bills_jun:
            total_payments_jun = 0
            for occupant_payment_jun in occupant_payments_jun:
                if occupant_payment_jun['id'] == occupant_bill_jun['id']:
                    total_payments_jun = occupant_payment_jun['total_payments_jun']
                    break
            remaining_balance_jun = occupant_bill_jun['total_bills_jun'] - total_payments_jun
            if remaining_balance_jun > 0:
                occupants_with_balance_jun += 1
            else:
                occupants_with_zero_or_negative_balance_jun += 1

        Jun_PatiallyPaid_Per = (occupants_with_balance_jun / Jun) * 100 if Jun != 0 else 0
        Jun_PatiallyPaid_Per = int(round(Jun_PatiallyPaid_Per))

        Jun_Paid_Per = (occupants_with_zero_or_negative_balance_jun / Jun) * 100 if Jun != 0 else 0
        Jun_Paid_Per = int(round(Jun_Paid_Per))


        # Partially Paid and Paid in July
        occupant_bills_jul = Occupant.objects.filter(bill_details__created_at__icontains="2023-07")\
            .annotate(total_bills_jul=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jul')\
            .distinct().order_by('person__last_name')

        occupant_payments_jul = Occupant.objects.filter(payment__created_at__icontains="2023-07")\
            .annotate(total_payments_jul=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jul')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jul = 0
        occupants_with_zero_or_negative_balance_jul = 0
        
        for occupant_bill_jul in occupant_bills_jul:
            total_payments_jul = 0
            for occupant_payment_jul in occupant_payments_jul:
                if occupant_payment_jul['id'] == occupant_bill_jul['id']:
                    total_payments_jul = occupant_payment_jul['total_payments_jul']
                    break
            remaining_balance_jul = occupant_bill_jul['total_bills_jul'] - total_payments_jul
            if remaining_balance_jul > 0:
                occupants_with_balance_jul += 1
            else:
                occupants_with_zero_or_negative_balance_jul += 1

        Jul_PatiallyPaid_Per = (occupants_with_balance_jul / Jul) * 100 if Jul != 0 else 0
        Jul_PatiallyPaid_Per = int(round(Jul_PatiallyPaid_Per))

        Jul_Paid_Per = (occupants_with_zero_or_negative_balance_jul / Jul) * 100 if Jul != 0 else 0
        Jul_Paid_Per = int(round(Jul_Paid_Per))


        # Partially Paid and Paid in August
        occupant_bills_aug = Occupant.objects.filter(bill_details__created_at__icontains="2023-08")\
            .annotate(total_bills_aug=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_aug')\
            .distinct().order_by('person__last_name')

        occupant_payments_aug = Occupant.objects.filter(payment__created_at__icontains="2023-08")\
            .annotate(total_payments_aug=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_aug')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_aug = 0
        occupants_with_zero_or_negative_balance_aug = 0

        for occupant_bill_aug in occupant_bills_aug:
            total_payments_aug = 0
            for occupant_payment_aug in occupant_payments_aug:
                if occupant_payment_aug['id'] == occupant_bill_aug['id']:
                    total_payments_aug = occupant_payment_aug['total_payments_aug']
                    break
            remaining_balance_aug = occupant_bill_aug['total_bills_aug'] - total_payments_aug
            if remaining_balance_aug > 0:
                occupants_with_balance_aug += 1
            else:
                occupants_with_zero_or_negative_balance_aug += 1

        Aug_PatiallyPaid_Per = (occupants_with_balance_aug / Aug) * 100 if Aug != 0 else 0
        Aug_PatiallyPaid_Per = int(round(Aug_PatiallyPaid_Per))

        Aug_Paid_Per = (occupants_with_zero_or_negative_balance_aug / Aug) * 100 if Aug != 0 else 0
        Aug_Paid_Per = int(round(Aug_Paid_Per))


        # Partially Paid and Paid in September
        occupant_bills_sep = Occupant.objects.filter(bill_details__created_at__icontains="2023-09")\
            .annotate(total_bills_sep=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_sep')\
            .distinct().order_by('person__last_name')

        occupant_payments_sep = Occupant.objects.filter(payment__created_at__icontains="2023-09")\
            .annotate(total_payments_sep=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_sep')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_sep = 0
        occupants_with_zero_or_negative_balance_sep = 0
        
        for occupant_bill_sep in occupant_bills_sep:
            total_payments_sep = 0
            for occupant_payment_sep in occupant_payments_sep:
                if occupant_payment_sep['id'] == occupant_bill_sep['id']:
                    total_payments_sep = occupant_payment_sep['total_payments_sep']
                    break
            remaining_balance_sep = occupant_bill_sep['total_bills_aug'] - total_payments_sep
            if remaining_balance_sep > 0:
                occupants_with_balance_sep += 1
            else:
                occupants_with_zero_or_negative_balance_sep += 1

        Sep_PatiallyPaid_Per = (occupants_with_balance_sep / Sep) * 100 if Sep != 0 else 0
        Sep_PatiallyPaid_Per = int(round(Sep_PatiallyPaid_Per))

        Sep_Paid_Per = (occupants_with_zero_or_negative_balance_sep / Sep) * 100 if Sep != 0 else 0
        Sep_Paid_Per = int(round(Sep_Paid_Per))


        # Partially Paid and Paid in October
        occupant_bills_oct = Occupant.objects.filter(bill_details__created_at__icontains="2023-10")\
            .annotate(total_bills_oct=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_oct')\
            .distinct().order_by('person__last_name')

        occupant_payments_oct = Occupant.objects.filter(payment__created_at__icontains="2023-10")\
            .annotate(total_payments_oct=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_oct')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_oct = 0
        occupants_with_zero_or_negative_balance_oct = 0
        
        for occupant_bill_oct in occupant_bills_oct:
            total_payments_oct = 0
            for occupant_payment_oct in occupant_payments_oct:
                if occupant_payment_oct['id'] == occupant_bill_oct['id']:
                    total_payments_oct = occupant_payment_oct['total_payments_oct']
                    break
            remaining_balance_oct = occupant_bill_oct['total_bills_oct'] - total_payments_oct
            if remaining_balance_oct > 0:
                occupants_with_balance_oct += 1
            else:
                occupants_with_zero_or_negative_balance_oct += 1

        Oct_PatiallyPaid_Per = (occupants_with_balance_oct / Oct) * 100 if Oct != 0 else 0
        Oct_PatiallyPaid_Per = int(round(Oct_PatiallyPaid_Per))

        Oct_Paid_Per = (occupants_with_zero_or_negative_balance_oct / Oct) * 100 if Oct != 0 else 0
        Oct_Paid_Per = int(round(Oct_Paid_Per))


        # Partially Paid and Paid in November
        occupant_bills_nov = Occupant.objects.filter(bill_details__created_at__icontains="2023-11")\
            .annotate(total_bills_nov=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_nov')\
            .distinct().order_by('person__last_name')

        occupant_payments_nov = Occupant.objects.filter(payment__created_at__icontains="2023-11")\
            .annotate(total_payments_nov=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_nov')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_nov = 0
        occupants_with_zero_or_negative_balance_nov = 0

        for occupant_bill_nov in occupant_bills_nov:
            total_payments_nov = 0
            for occupant_payment_nov in occupant_payments_nov:
                if occupant_payment_nov['id'] == occupant_bill_nov['id']:
                    total_payments_nov = occupant_payment_nov['total_payments_nov']
                    break
            remaining_balance_nov = occupant_bill_nov['total_bills_nov'] - total_payments_nov
            if remaining_balance_nov > 0:
                occupants_with_balance_nov += 1
            else:
                occupants_with_zero_or_negative_balance_nov += 1

        Nov_PatiallyPaid_Per = (occupants_with_balance_nov / Nov) * 100 if Nov != 0 else 0
        Nov_PatiallyPaid_Per = int(round(Nov_PatiallyPaid_Per))

        Nov_Paid_Per = (occupants_with_zero_or_negative_balance_nov / Nov) * 100 if Nov != 0 else 0
        Nov_Paid_Per = int(round(Nov_Paid_Per))


        # Partially Paid and Paid in December
        occupant_bills_dec = Occupant.objects.filter(bill_details__created_at__icontains="2023-12")\
            .annotate(total_bills_dec=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_dec')\
            .distinct().order_by('person__last_name')

        occupant_payments_dec = Occupant.objects.filter(payment__created_at__icontains="2023-12")\
            .annotate(total_payments_dec=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_dec')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_dec = 0
        occupants_with_zero_or_negative_balance_dec = 0
        
        for occupant_bill_dec in occupant_bills_dec:
            total_payments_dec = 0
            for occupant_payment_dec in occupant_payments_dec:
                if occupant_payment_dec['id'] == occupant_bill_dec['id']:
                    total_payments_dec = occupant_payment_dec['total_payments_dec']
                    break
            remaining_balance_dec = occupant_bill_dec['total_bills_dec'] - total_payments_dec
            if remaining_balance_dec > 0:
                occupants_with_balance_dec += 1
            else:
                occupants_with_zero_or_negative_balance_nov += 1

        Dec_PatiallyPaid_Per = (occupants_with_balance_dec / Dec) * 100 if Dec != 0 else 0
        Dec_PatiallyPaid_Per = int(round(Dec_PatiallyPaid_Per))

        Dec_Paid_Per = (occupants_with_zero_or_negative_balance_dec / Dec) * 100 if Dec != 0 else 0
        Dec_Paid_Per = int(round(Dec_Paid_Per))


        partiallypaid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        partiallypaid_monthly_occ_per = [Jan_PatiallyPaid_Per, Feb_PatiallyPaid_Per, Mar_PatiallyPaid_Per, Apr_PatiallyPaid_Per,
                                          May_PatiallyPaid_Per, Jun_PatiallyPaid_Per, Jul_PatiallyPaid_Per, Aug_PatiallyPaid_Per, 
                                          Sep_PatiallyPaid_Per, Oct_PatiallyPaid_Per, Nov_PatiallyPaid_Per, Dec_PatiallyPaid_Per]
        
        context['partiallypaid_monthly_occ_per_list'] = partiallypaid_monthly_occ_per_list
        context['partiallypaid_monthly_occ_per'] = partiallypaid_monthly_occ_per


        paid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        paid_monthly_occ_per = [Jan_Paid_Per, Feb_Paid_Per, Mar_Paid_Per, Apr_Paid_Per,
                                May_Paid_Per, Jun_Paid_Per, Jul_Paid_Per, Aug_Paid_Per, 
                                Sep_Paid_Per, Oct_Paid_Per, Nov_Paid_Per, Dec_Paid_Per]
        
        context['paid_monthly_occ_per_list'] = paid_monthly_occ_per_list
        context['paid_monthly_occ_per'] = paid_monthly_occ_per


        return context

# @method_decorator(login_required, name='dispatch')
class FDDashMaleVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'frontdesk/fd_dash_male_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(FDDashMaleVacantBed, self).get_queryset(*args, **kwargs)
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
class FDDashFemaleVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'frontdesk/fd_dash_female_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(FDDashFemaleVacantBed, self).get_queryset(*args, **kwargs)
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
class FDDashForeignVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'frontdesk/fd_dash_foreign_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(FDDashForeignVacantBed, self).get_queryset(*args, **kwargs)
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
class FDRegistrationList(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'frontdesk/fd_registration_list.html'
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
        qs = super(FDRegistrationList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-created_at").filter(Q(psu_email__icontains=query) | Q(last_name__icontains=query) | Q(first_name__icontains=query) 
            | Q(program__icontains=query) | Q(boarder_type__icontains=query)| Q(reg_status__iexact=query) | Q(gender__iexact=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class FDRegMonthRep(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'frontdesk/fd_reg_month_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = Person.objects.raw('SELECT * FROM dormitory_person WHERE MONTH(created_at) = MONTH(CURRENT_DATE()) AND YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')
        return context

# @method_decorator(login_required, name='dispatch')
class FDRegYearRep(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'frontdesk/fd_reg_year_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = Person.objects.raw('SELECT * FROM dormitory_person WHERE YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')
        return context

# @method_decorator(login_required, name='dispatch')
class FDRegistrationUpdateView(UpdateView):
    model = Person
    context_object_name = 'person'
    form_class = RegistrationForm
    template_name = 'frontdesk/fd_registration_update.html'
    success_url = "/fd_registration_list"

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
class FDRegistrationRegView(UpdateView):
    model = Person
    fields = "__all__"
    context_object_name = 'person'
    template_name = 'frontdesk/fd_registration_view.html'
    success_url = "/fd_registration_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Registration details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class FDOccupantList(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'frontdesk/fd_occupant_list.html'
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
        qs = super(FDOccupantList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-created_at").filter(Q(person__last_name__icontains=query) | Q(person__first_name__icontains=query)
            | Q(bed__bed_code__icontains=query) | Q(person__boarder_type__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class FDOccupantUpdateView(UpdateView):
    model = Occupant
    # fields = ['person','bed','start_date','end_date']
    context_object_name = 'occupant'
    form_class = OccupantFormEdit
    template_name = 'frontdesk/fd_occupant_update.html'
    success_url = "/fd_occupant_list"

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
        return "/fd_occupant_list"

    def form_valid(self, form):
      messages.success(self.request, "Occupant details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class FDOccupantView(UpdateView):
    model = Occupant
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'frontdesk/fd_occupant_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fetch_first_three'] = Bill_Details.objects.filter(occupant=self.object.id)[:3]
        context['billing_details'] = Bill_Details.objects.filter(occupant=self.object.id)[3:]
        context['total_bills_amount'] = Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['payment'] = Payment.objects.filter(occupant=self.object.id)
        context['total_payment_amount'] = Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['remaining_balance'] = (Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0)
        context['occupant_demerits'] = OccupantDemerit.objects.filter(occupant=self.object.id)

        cursor = connections['default'].cursor()
        query = f"UPDATE dormitory_occupantdemerit SET new_remarks = null "
        cursor.execute(query)

        return context

    def form_valid(self, form):
      messages.success(self.request, "Occupant details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class FDOccMonthRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'superadmin/occ_month_rep.html'
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
class FDOccYearRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'superadmin/occ_year_rep.html'
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
class FDOccupantDemeritList(ListView):
    model = OccupantDemerit
    context_object_name = 'occupant'
    template_name = 'frontdesk/fd_occupant_demerit_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['occupant_demerit'] = OccupantDemerit.objects.count()
        cursor = connections['default'].cursor()
        query = f"UPDATE dormitory_occupantdemerit SET new_remarks = null "
        cursor.execute(query)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(FDOccupantDemeritList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("occupant")
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(demerit_name__demerit_name__icontains=query)
            | Q(demerit_name__demerit_points__icontains=query) | Q(cur_date__icontains=query) | Q(prev_remarks__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class FDOccupantDemeritUpdateView(UpdateView):
    model = OccupantDemerit
    fields = ['prev_remarks', 'new_remarks']
    context_object_name = 'occupant'
    template_name = 'frontdesk/fd_occupant_demerit_update.html'
    success_url = "/fd_occupant_demerit_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Occupant demerit was updated successfully!")
      super().form_valid(form)

      occ_id = form.instance.id
      pre_r = form.cleaned_data.get('prev_remarks')
      new_r = form.cleaned_data.get('new_remarks')

      prev_plus_new = pre_r +" \n \n " + new_r

      cursor = connections['default'].cursor()
      query = "UPDATE dormitory_occupantdemerit SET prev_remarks = %s WHERE id = %s"
      params = (prev_plus_new, occ_id)
      cursor.execute(query, params)
      return HttpResponseRedirect(self.get_success_url())
  
# @method_decorator(login_required, name='dispatch')
class FDOccupantViewDemeritUpdate(UpdateView):
    model = OccupantDemerit
    fields = ['prev_remarks', 'new_remarks']
    context_object_name = 'occupant'
    template_name = 'frontdesk/fd_occupant_demerit_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('FDOccupantView', kwargs={'pk': self.object.occupant_id})

    def form_valid(self, form):
        messages.success(self.request, "Occupant demerit was updated successfully!")
        super().form_valid(form)

        occ_id = form.instance.id
        pre_r = form.cleaned_data.get('prev_remarks')
        new_r = form.cleaned_data.get('new_remarks')

        prev_plus_new = pre_r +" \n \n " + new_r

        cursor = connections['default'].cursor()
        query = "UPDATE dormitory_occupantdemerit SET prev_remarks = %s WHERE id = %s"
        params = (prev_plus_new, occ_id)
        cursor.execute(query, params)

        return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class FDRoomList(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'frontdesk/fd_room_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(FDRoomList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(room_name__iexact=query) | Q(floorlvl__icontains=query) 
                | Q(dorm_name__icontains=query) | Q(description__icontains=query))
        
        # Annotate the queryset after the search filter has been applied
        qs = qs.annotate(
            TotalBeds=Count('bed'), 
            TotalVacant=Count('bed', filter=Q(bed__bed_status='Vacant'))
        ).order_by('created_at')
        
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
class FDRoomListCard(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'frontdesk/fd_room_list_card.html'
    paginate_by = 9

    def get_queryset(self, *args, **kwargs):
        qs = super(FDRoomListCard, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(room_name__iexact=query) | Q(floorlvl__icontains=query) 
                | Q(dorm_name__icontains=query) | Q(description__icontains=query))
        
        # Annotate the queryset after the search filter has been applied
        qs = qs.annotate(
            TotalBeds=Count('bed'), 
            TotalVacant=Count('bed', filter=Q(bed__bed_status='Vacant')),
            TotalOccupied=Count('bed', filter=Q(bed__bed_status='Occupied')),
            TotalUnder=Count('bed', filter=Q(bed__bed_status='Under Maint.')),
        ).order_by('created_at')
        
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
class FDRoomUpdateView(UpdateView):
    model = Room
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'frontdesk/fd_room_update.html'
    success_url = "/fd_room_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Room details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class FDRoomCardUpdateView(UpdateView):
    model = Room
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'frontdesk/fd_room_update.html'
    success_url = "/fd_room_list_card"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Room details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class FDBedList(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'frontdesk/fd_bed_list.html'
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
        qs = super(FDBedList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("room_id")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("room_id").filter(Q(room__dorm_name__iexact=query) | Q(room__room_name__icontains=query)
            | Q(bed_code__icontains=query) | Q(price__icontains=query) | Q(bed_status__icontains=query))
        return qs
    
# @method_decorator(login_required, name='dispatch')
class FDBedUpdateView(UpdateView):
    model = Bed
    fields = "__all__"
    context_object_name = 'bed'
    template_name = 'frontdesk/fd_bed_update.html'
    success_url = "/fd_bed_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Bed details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class FDServiceList(ListView):
    model = Service
    context_object_name = 'service'
    template_name = 'frontdesk/fd_service_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services']= Service.objects.all().exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others').count()
        context['available'] = Service.objects.filter(status__iexact="Available").exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others').count()
        context['notavailable'] = Service.objects.filter(status__iexact="Not Available").count()
        context['services_limit']= Service.objects.all().exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others')
    
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(FDServiceList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("service_name").filter(Q(service_name__icontains=query) | Q(status__icontains=query)
            | Q(base_amount__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class FDServiceUpdateView(UpdateView):
    model = Service
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'frontdesk/fd_service_update.html'
    success_url = "/fd_service_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Service details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class FDDemeritList(ListView):
    model = Demerit
    context_object_name = 'demerit'
    template_name = 'frontdesk/fd_demerit_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demerit'] = Demerit.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(FDDemeritList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("demerit_points")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-demerit_points").filter(Q(demerit_name__icontains=query) 
            | Q(demerit_points__iexact=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class FDDemeritUpdateView(UpdateView):
    model = Demerit
    fields = "__all__"
    context_object_name = 'demerit'
    template_name = 'frontdesk/fd_demerit_update.html'
    success_url = "/fd_demerit_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Demerit details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())
 

# @method_decorator(login_required, name='dispatch')
class FDAdminProfile(ListView):
    model = Admin
    context_object_name = 'admin'
    template_name = "frontdesk/fd_admin_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global xy
        context ['acc'] = Admin.objects.filter(Q(username=xy)).values()
        return context

# @method_decorator(login_required, name='dispatch')
class FDAdminProfileUpdateView(UpdateView):
    model = Admin
    fields = ['firstname', 'lastname', 'username', 'password', 'security_question', 'security_answer', 'recovery_email']
    context_object_name = 'admin'
    template_name = 'frontdesk/fd_admin_profile_update.html'
    success_url = "/fd_admin_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Your Account Information was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# ===================================================
# End of Frontdesk
# ===================================================


# ===================================================
# Start of Accountingstaff
# ===================================================
# @method_decorator(login_required, name='dispatch')
class ASHomePageView(ListView):
    model = Room
    context_object_name = 'room'
    template_name = "landingpage/as_home.html"

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
            
        # Students Gender Charts
        male_no = Person.objects.filter(gender="Male").count()
        male_no = int(male_no)

        female_no = Person.objects.filter(gender="Female").count()
        female_no = int(female_no)

        lgbt_no = Person.objects.filter(gender="LGBTQIA+").count()
        lgbt_no = int(lgbt_no)

        gender_list = ['Male', 'Female', 'LGBTQIA+']
        gender_number = [male_no, female_no, lgbt_no]

        context['gender_list'] = gender_list
        context['gender_number'] = gender_number

                
        # Monthly Registration Charts
        Jan_Reg = Person.objects.filter(created_at__icontains="2023-01").count()
        Jan_Reg = int(Jan_Reg)

        Feb_Reg = Person.objects.filter(created_at__icontains="2023-02").count()
        Feb_Reg = int(Feb_Reg)

        Mar_Reg = Person.objects.filter(created_at__icontains="2023-03").count()
        Mar_Reg = int(Mar_Reg)

        Apr_Reg = Person.objects.filter(created_at__icontains="2023-04").count()
        Apr_Reg = int(Apr_Reg)

        May_Reg = Person.objects.filter(created_at__icontains="2023-05").count()
        May_Reg = int(May_Reg)

        Jun_Reg = Person.objects.filter(created_at__icontains="2023-06").count()
        Jun_Reg = int(Jun_Reg)

        Jul_Reg = Person.objects.filter(created_at__icontains="2023-07").count()
        Jul_Reg = int(Jul_Reg)

        Aug_Reg = Person.objects.filter(created_at__icontains="2023-08").count()
        Aug_Reg = int(Aug_Reg)

        Sep_Reg = Person.objects.filter(created_at__icontains="2023-09").count()
        Sep_Reg = int(Sep_Reg)

        Oct_Reg = Person.objects.filter(created_at__icontains="2023-10").count()
        Oct_Reg = int(Oct_Reg)

        Nov_Reg = Person.objects.filter(created_at__icontains="2023-11").count()
        Nov_Reg = int(Nov_Reg)

        Dec_Reg = Person.objects.filter(created_at__icontains="2023-12").count()
        Dec_Reg = int(Dec_Reg)

        monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_number = [Jan_Reg, Feb_Reg, Mar_Reg, Apr_Reg, May_Reg, Jun_Reg, Jul_Reg, Aug_Reg, Sep_Reg, Oct_Reg, Nov_Reg, Dec_Reg]

        context['monthly_list'] = monthly_list
        context['monthly_number'] = monthly_number


        # Monthly Occupant Charts
        Jan = Occupant.objects.filter(created_at__icontains="2023-01").count()
        Jan = int(Jan)

        Feb = Occupant.objects.filter(created_at__icontains="2023-02").count()
        Feb = int(Feb)

        Mar = Occupant.objects.filter(created_at__icontains="2023-03").count()
        Mar = int(Mar)

        Apr = Occupant.objects.filter(created_at__icontains="2023-04").count()
        Apr = int(Apr)

        May = Occupant.objects.filter(created_at__icontains="2023-05").count()
        May = int(May)

        Jun = Occupant.objects.filter(created_at__icontains="2023-06").count()
        Jun = int(Jun)

        Jul = Occupant.objects.filter(created_at__icontains="2023-07").count()
        Jul = int(Jul)

        Aug = Occupant.objects.filter(created_at__icontains="2023-08").count()
        Aug = int(Aug)

        Sep = Occupant.objects.filter(created_at__icontains="2023-09").count()
        Sep = int(Sep)

        Oct = Occupant.objects.filter(created_at__icontains="2023-10").count()
        Oct = int(Oct)

        Nov = Occupant.objects.filter(created_at__icontains="2023-11").count()
        Nov = int(Nov)

        Dec = Occupant.objects.filter(created_at__icontains="2023-12").count()
        Dec = int(Dec)

        occ_monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        occ_monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['occ_monthly_list'] = occ_monthly_list
        context['occ_monthly_number'] = occ_monthly_number


        # Monthly Male Charts
        Jan_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="Male").count()
        Jan_Male_Per = (Jan_Tot_Male / Jan) * 100 if Jan != 0 else 0
        Jan_Male_Per = int(round(Jan_Male_Per))

        Feb_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="Male").count()
        Feb_Male_Per = (Feb_Tot_Male / Feb) * 100 if Feb != 0 else 0
        Feb_Male_Per = int(round(Feb_Male_Per))

        Mar_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="Male").count()
        Mar_Male_Per = (Mar_Tot_Male / Mar) * 100 if Mar != 0 else 0
        Mar_Male_Per = int(round(Mar_Male_Per))

        Apr_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="Male").count()
        Apr_Male_Per = (Apr_Tot_Male / Apr) * 100 if Apr != 0 else 0
        Apr_Male_Per = int(round(Apr_Male_Per))

        May_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="Male").count()
        May_Male_Per = (May_Tot_Male / May) * 100 if May != 0 else 0
        May_Male_Per = int(round(May_Male_Per))

        Jun_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="Male").count()
        Jun_Male_Per = (Jun_Tot_Male / Jun) * 100 if Jun != 0 else 0
        Jun_Male_Per = int(round(Jun_Male_Per))

        Jul_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="Male").count()
        Jul_Male_Per = (Jul_Tot_Male / Jul) * 100 if Jul != 0 else 0
        Jul_Male_Per = int(round(Jul_Male_Per))

        Aug_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="Male").count()
        Aug_Male_Per = (Aug_Tot_Male / Aug) * 100 if Aug != 0 else 0
        Aug_Male_Per = int(round(Aug_Male_Per))

        Sep_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="Male").count()
        Sep_Male_Per = (Sep_Tot_Male / Sep) * 100 if Sep != 0 else 0
        Sep_Male_Per = int(round(Sep_Male_Per))

        Oct_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="Male").count()
        Oct_Male_Per = (Oct_Tot_Male / Oct) * 100 if Oct != 0 else 0
        Oct_Male_Per = int(round(Oct_Male_Per))

        Nov_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="Male").count()
        Nov_Male_Per = (Nov_Tot_Male / Nov) * 100 if Nov != 0 else 0
        Nov_Male_Per = int(round(Nov_Male_Per))

        Dec_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="Male").count()
        Dec_Male_Per = (Dec_Tot_Male / Dec) * 100 if Dec != 0 else 0
        Dec_Male_Per = int(round(Dec_Male_Per))

        male_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        male_monthly_occ_per = [Jan_Male_Per, Feb_Male_Per, Mar_Male_Per, Apr_Male_Per, May_Male_Per, Jun_Male_Per, 
                                Jul_Male_Per, Aug_Male_Per, Sep_Male_Per, Oct_Male_Per, Nov_Male_Per, Dec_Male_Per]
        
        context['male_monthly_occ_per_list'] = male_monthly_occ_per_list
        context['male_monthly_occ_per'] = male_monthly_occ_per
        

        # Monthly Female Charts
        Jan_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="Female").count()
        Jan_Female_Per = (Jan_Tot_Female / Jan) * 100 if Jan != 0 else 0
        Jan_Female_Per = int(round(Jan_Female_Per))

        Feb_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="Female").count()
        Feb_Female_Per = (Feb_Tot_Female / Feb) * 100 if Feb != 0 else 0
        Feb_Female_Per = int(round(Feb_Female_Per))

        Mar_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="Female").count()
        Mar_Female_Per = (Mar_Tot_Female / Mar) * 100 if Mar != 0 else 0
        Mar_Female_Per = int(round(Mar_Female_Per))

        Apr_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="Female").count()
        Apr_Female_Per = (Apr_Tot_Female / Apr) * 100 if Apr != 0 else 0
        Apr_Female_Per = int(round(Apr_Female_Per))

        May_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="Female").count()
        May_Female_Per = (May_Tot_Female / May) * 100 if May != 0 else 0
        May_Female_Per = int(round(May_Female_Per))

        Jun_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="Female").count()
        Jun_Female_Per = (Jun_Tot_Female / Jun) * 100 if Jun != 0 else 0
        Jun_Female_Per = int(round(Jun_Female_Per))

        Jul_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="Female").count()
        Jul_Female_Per = (Jul_Tot_Female / Jul) * 100 if Jul != 0 else 0
        Jul_Female_Per = int(round(Jul_Female_Per))

        Aug_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="Female").count()
        Aug_Female_Per = (Aug_Tot_Female / Aug) * 100 if Aug != 0 else 0
        Aug_Female_Per = int(round(Aug_Female_Per))

        Sep_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="Female").count()
        Sep_Female_Per = (Sep_Tot_Female / Sep) * 100 if Sep != 0 else 0
        Sep_Female_Per = int(round(Sep_Female_Per))

        Oct_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="Female").count()
        Oct_Female_Per = (Oct_Tot_Female/ Oct) * 100 if Oct != 0 else 0
        Oct_Female_Per = int(round(Oct_Female_Per))

        Nov_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="Female").count()
        Nov_Female_Per = (Nov_Tot_Female / Nov) * 100 if Nov != 0 else 0
        Nov_Female_Per = int(round(Nov_Female_Per))

        Dec_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="Female").count()
        Dec_Female_Per = (Dec_Tot_Female / Dec) * 100 if Dec != 0 else 0
        Dec_Female_Per = int(round(Dec_Female_Per))

        female_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        female_monthly_occ_per = [Jan_Female_Per, Feb_Female_Per, Mar_Female_Per, Apr_Female_Per, May_Female_Per, Jun_Female_Per, 
                                Jul_Female_Per, Aug_Female_Per, Sep_Female_Per, Oct_Female_Per, Nov_Female_Per, Dec_Female_Per]
        
        context['female_monthly_occ_per_list'] = female_monthly_occ_per_list
        context['female_monthly_occ_per'] = female_monthly_occ_per


        # Monthly LGBTQIA+ Charts
        Jan_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="LGBTQIA+").count()
        Jan_LGBTQIA_Per = (Jan_Tot_LGBTQIA / Jan) * 100 if Jan != 0 else 0
        Jan_LGBTQIA_Per = int(round(Jan_LGBTQIA_Per))

        Feb_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="LGBTQIA+").count()
        Feb_LGBTQIA_Per = (Feb_Tot_LGBTQIA / Feb) * 100 if Feb != 0 else 0
        Feb_LGBTQIA_Per = int(round(Feb_LGBTQIA_Per))

        Mar_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="LGBTQIA+").count()
        Mar_LGBTQIA_Per = (Mar_Tot_Female / Mar) * 100 if Mar != 0 else 0
        Mar_LGBTQIA_Per = int(round(Mar_LGBTQIA_Per))

        Apr_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="LGBTQIA+").count()
        Apr_LGBTQIA_Per = (Apr_Tot_LGBTQIA / Apr) * 100 if Apr != 0 else 0
        Apr_LGBTQIA_Per = int(round(Apr_LGBTQIA_Per))

        May_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="LGBTQIA+").count()
        May_LGBTQIA_Per = (May_Tot_LGBTQIA / May) * 100 if May != 0 else 0
        May_LGBTQIA_Per = int(round(May_LGBTQIA_Per))

        Jun_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="LGBTQIA+").count()
        Jun_LGBTQIA_Per = (Jun_Tot_LGBTQIA / Jun) * 100 if Jun != 0 else 0
        Jun_LGBTQIA_Per = int(round(Jun_LGBTQIA_Per))

        Jul_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="LGBTQIA+").count()
        Jul_LGBTQIA_Per = (Jul_Tot_LGBTQIA / Jul) * 100 if Jul != 0 else 0
        Jul_LGBTQIA_Per = int(round(Jul_LGBTQIA_Per))

        Aug_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="LGBTQIA+").count()
        Aug_LGBTQIA_Per = (Aug_Tot_LGBTQIA / Aug) * 100 if Aug != 0 else 0
        Aug_LGBTQIA_Per = int(round(Aug_LGBTQIA_Per))

        Sep_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="LGBTQIA+").count()
        Sep_LGBTQIA_Per = (Sep_Tot_LGBTQIA / Sep) * 100 if Sep != 0 else 0
        Sep_LGBTQIA_Per = int(round(Sep_LGBTQIA_Per))

        Oct_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="LGBTQIA+").count()
        Oct_LGBTQIA_Per = (Oct_Tot_LGBTQIA/ Oct) * 100 if Oct != 0 else 0
        Oct_LGBTQIA_Per = int(round(Oct_LGBTQIA_Per))

        Nov_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="LGBTQIA+").count()
        Nov_LGBTQIA_Per = (Nov_Tot_LGBTQIA / Nov) * 100 if Nov != 0 else 0
        Nov_LGBTQIA_Per = int(round(Nov_LGBTQIA_Per))

        Dec_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="LGBTQIA+").count()
        Dec_LGBTQIA_Per = (Dec_Tot_LGBTQIA / Dec) * 100 if Dec != 0 else 0
        Dec_LGBTQIA_Per = int(round(Dec_LGBTQIA_Per))

        LGBTQIA_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        LGBTQIA_monthly_occ_per = [Jan_LGBTQIA_Per, Feb_LGBTQIA_Per, Mar_LGBTQIA_Per, Apr_LGBTQIA_Per, May_LGBTQIA_Per, Jun_LGBTQIA_Per, 
                                    Jul_LGBTQIA_Per, Aug_LGBTQIA_Per, Sep_LGBTQIA_Per, Oct_LGBTQIA_Per, Nov_LGBTQIA_Per, Dec_LGBTQIA_Per]
        
        context['LGBTQIA_monthly_occ_per_list'] = LGBTQIA_monthly_occ_per_list
        context['LGBTQIA_monthly_occ_per'] = LGBTQIA_monthly_occ_per

        
        # Monthly Unpaid Charts
        Jan_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-01", payment__isnull=False).distinct().count()
        Jan_Unpaid_Per = (Jan_Unpaid_Occ / Jan) * 100 if Jan != 0 else 0
        Jan_Unpaid_Per = int(round(Jan_Unpaid_Per))

        Feb_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-02", payment__isnull=False).distinct().count()
        Feb_Unpaid_Per = (Feb_Unpaid_Occ / Feb) * 100 if Feb != 0 else 0
        Feb_Unpaid_Per = int(round(Feb_Unpaid_Per))

        Mar_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-03", payment__isnull=False).distinct().count()
        Mar_Unpaid_Per = (Mar_Unpaid_Occ / Mar) * 100 if Mar != 0 else 0
        Mar_Unpaid_Per = int(round(Mar_Unpaid_Per))

        Apr_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-04", payment__isnull=False).distinct().count()
        Apr_Unpaid_Per = (Apr_Unpaid_Occ / Apr) * 100 if Apr != 0 else 0
        Apr_Unpaid_Per = int(round(Apr_Unpaid_Per))

        May_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-05", payment__isnull=False).distinct().count()
        May_Unpaid_Per = (May_Unpaid_Occ / May) * 100 if May != 0 else 0
        May_Unpaid_Per = int(round(May_Unpaid_Per))

        Jun_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-06", payment__isnull=False).distinct().count()
        Jun_Unpaid_Per = (Jun_Unpaid_Occ / Jun) * 100 if Jun != 0 else 0
        Jun_Unpaid_Per = int(round(Jun_Unpaid_Per))

        Jul_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-07", payment__isnull=False).distinct().count()
        Jul_Unpaid_Per = (Jul_Unpaid_Occ / Jul) * 100 if Jul != 0 else 0
        Jul_Unpaid_Per = int(round(Jul_Unpaid_Per))

        Aug_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-08", payment__isnull=False).distinct().count()
        Aug_Unpaid_Per = (Aug_Unpaid_Occ / Aug) * 100 if Aug != 0 else 0
        Aug_Unpaid_Per = int(round(Aug_Unpaid_Per))

        Sep_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-09", payment__isnull=False).distinct().count()
        Sep_Unpaid_Per = (Sep_Unpaid_Occ / Sep) * 100 if Sep != 0 else 0
        Sep_Unpaid_Per = int(round(Sep_Unpaid_Per))

        Oct_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-10", payment__isnull=False).distinct().count()
        Oct_Unpaid_Per = (Oct_Unpaid_Occ / Oct) * 100 if Oct != 0 else 0
        Oct_Unpaid_Per = int(round(Oct_Unpaid_Per))

        Nov_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-11", payment__isnull=False).distinct().count()
        Nov_Unpaid_Per = (Nov_Unpaid_Occ / Nov) * 100 if Nov != 0 else 0
        Nov_Unpaid_Per = int(round(Nov_Unpaid_Per))

        Dec_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-12", payment__isnull=False).distinct().count()
        Dec_Unpaid_Per = (Dec_Unpaid_Occ / Dec) * 100 if Dec != 0 else 0
        Dec_Unpaid_Per = int(round(Dec_Unpaid_Per))


        unpaid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        unpaid_monthly_occ_per = [Jan_Unpaid_Per, Feb_Unpaid_Per, Mar_Unpaid_Per, Apr_Unpaid_Per, May_Unpaid_Per, Jun_Unpaid_Per, 
                                Jul_Unpaid_Per, Aug_Unpaid_Per, Sep_Unpaid_Per, Oct_Unpaid_Per, Nov_Unpaid_Per, Dec_Unpaid_Per]
        
        context['unpaid_monthly_occ_per_list'] = unpaid_monthly_occ_per_list
        context['unpaid_monthly_occ_per'] = unpaid_monthly_occ_per


        # Monthly Paid Charts

        # Partially Paid and Paid in January
        occupant_bills_jan = Occupant.objects.filter(bill_details__created_at__icontains="2023-01")\
            .annotate(total_bills_jan=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jan')\
            .distinct().order_by('person__last_name')

        occupant_payments_jan = Occupant.objects.filter(payment__created_at__icontains="2023-01")\
            .annotate(total_payments_jan=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jan')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jan = 0
        occupants_with_zero_or_negative_balance_jan = 0

        for occupant_bill_jan in occupant_bills_jan:
            total_payments_jan = 0
            for occupant_payment_jan in occupant_payments_jan:
                if occupant_payment_jan['id'] == occupant_bill_jan['id']:
                    total_payments_jan = occupant_payment_jan['total_payments_jan']
                    break
            remaining_balance_jan = occupant_bill_jan['total_bills_jan'] - total_payments_jan
            if remaining_balance_jan > 0:
                occupants_with_balance_jan += 1
            else:
                occupants_with_zero_or_negative_balance_jan += 1

        Jan_PatiallyPaid_Per = (occupants_with_balance_jan / Jan) * 100 if Jan != 0 else 0
        Jan_PatiallyPaid_Per = int(round(Jan_PatiallyPaid_Per))

        Jan_Paid_Per = (occupants_with_zero_or_negative_balance_jan / Jan) * 100 if Jan != 0 else 0
        Jan_Paid_Per = int(round(Jan_Paid_Per))


        # Partially Paid and Paid in February
        occupant_bills_feb = Occupant.objects.filter(bill_details__created_at__icontains="2023-02")\
            .annotate(total_bills_feb=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_feb')\
            .distinct().order_by('person__last_name')

        occupant_payments_feb = Occupant.objects.filter(payment__created_at__icontains="2023-02")\
            .annotate(total_payments_feb=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_feb')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_feb = 0
        occupants_with_zero_or_negative_balance_feb = 0

        for occupant_bill_feb in occupant_bills_feb:
            total_payments_feb = 0
            for occupant_payment_feb in occupant_payments_feb:
                if occupant_payment_feb['id'] == occupant_bill_feb['id']:
                    total_payments_feb = occupant_payment_feb['total_payments_feb']
                    break
            remaining_balance_feb = occupant_bill_feb['total_bills_feb'] - total_payments_feb
            if remaining_balance_feb > 0:
                occupants_with_balance_feb += 1
            else:
                occupants_with_zero_or_negative_balance_feb += 1

        Feb_PatiallyPaid_Per = (occupants_with_balance_feb / Feb) * 100 if Feb != 0 else 0
        Feb_PatiallyPaid_Per = int(round(Feb_PatiallyPaid_Per))

        Feb_Paid_Per = (occupants_with_zero_or_negative_balance_feb / Feb) * 100 if Feb != 0 else 0
        Feb_Paid_Per = int(round(Feb_Paid_Per))


        # Partially Paid and Paid in March
        occupant_bills_mar = Occupant.objects.filter(bill_details__created_at__icontains="2023-03")\
            .annotate(total_bills_mar=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_mar')\
            .distinct().order_by('person__last_name')

        occupant_payments_mar = Occupant.objects.filter(payment__created_at__icontains="2023-03")\
            .annotate(total_payments_mar=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_mar')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_mar = 0
        occupants_with_zero_or_negative_balance_mar = 0

        for occupant_bill_mar in occupant_bills_mar:
            total_payments_mar = 0
            for occupant_payment_mar in occupant_payments_mar:
                if occupant_payment_mar['id'] == occupant_bill_mar['id']:
                    total_payments_mar = occupant_payment_mar['total_payments_mar']
                    break
            remaining_balance_mar = occupant_bill_mar['total_bills_mar'] - total_payments_mar
            if remaining_balance_mar > 0:
                occupants_with_balance_mar += 1
            else:
                occupants_with_zero_or_negative_balance_mar += 1

        Mar_PatiallyPaid_Per = (occupants_with_balance_mar / Mar) * 100 if Mar != 0 else 0
        Mar_PatiallyPaid_Per = int(round(Mar_PatiallyPaid_Per))

        Mar_Paid_Per = (occupants_with_zero_or_negative_balance_mar / Mar) * 100 if Mar != 0 else 0
        Mar_Paid_Per = int(round(Mar_Paid_Per))


        # Partially Paid and Paid in April
        occupant_bills_apr = Occupant.objects.filter(bill_details__created_at__icontains="2023-04")\
            .annotate(total_bills_apr=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_apr')\
            .distinct().order_by('person__last_name')

        occupant_payments_apr = Occupant.objects.filter(payment__created_at__icontains="2023-04")\
            .annotate(total_payments_apr=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_apr')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_apr = 0
        occupants_with_zero_or_negative_balance_apr = 0

        for occupant_bill_apr in occupant_bills_apr:
            total_payments_apr = 0
            for occupant_payment_apr in occupant_payments_apr:
                if occupant_payment_apr['id'] == occupant_bill_apr['id']:
                    total_payments_apr = occupant_payment_apr['total_payments_apr']
                    break
            remaining_balance_apr = occupant_bill_apr['total_bills_apr'] - total_payments_apr
            if remaining_balance_apr > 0:
                occupants_with_balance_apr += 1
            else:
                occupants_with_zero_or_negative_balance_apr += 1

        Apr_PatiallyPaid_Per = (occupants_with_balance_apr / Apr) * 100 if Apr != 0 else 0
        Apr_PatiallyPaid_Per = int(round(Apr_PatiallyPaid_Per))

        Apr_Paid_Per = (occupants_with_zero_or_negative_balance_apr / Apr) * 100 if Apr != 0 else 0
        Apr_Paid_Per = int(round(Apr_Paid_Per))


        # Partially Paid and Paid in May
        occupant_bills_may = Occupant.objects.filter(bill_details__created_at__icontains="2023-05")\
            .annotate(total_bills_may=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_may')\
            .distinct().order_by('person__last_name')

        occupant_payments_may = Occupant.objects.filter(payment__created_at__icontains="2023-05")\
            .annotate(total_payments_may=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_may')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_may = 0
        occupants_with_zero_or_negative_balance_may = 0
        
        for occupant_bill_may in occupant_bills_may:
            total_payments_may = 0
            for occupant_payment_may in occupant_payments_may:
                if occupant_payment_may['id'] == occupant_bill_may['id']:
                    total_payments_may = occupant_payment_may['total_payments_may']
                    break
            remaining_balance_may = occupant_bill_may['total_bills_may'] - total_payments_may
            if remaining_balance_may > 0:
                occupants_with_balance_may += 1
            else:
                occupants_with_zero_or_negative_balance_may += 1

        May_PatiallyPaid_Per = (occupants_with_balance_may / May) * 100 if May != 0 else 0
        May_PatiallyPaid_Per = int(round(May_PatiallyPaid_Per))

        May_Paid_Per = (occupants_with_zero_or_negative_balance_may / May) * 100 if May != 0 else 0
        May_Paid_Per = int(round(May_Paid_Per))

        
        # Partially Paid and Paid in June
        occupant_bills_jun = Occupant.objects.filter(bill_details__created_at__icontains="2023-06")\
            .annotate(total_bills_jun=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jun')\
            .distinct().order_by('person__last_name')

        occupant_payments_jun = Occupant.objects.filter(payment__created_at__icontains="2023-06")\
            .annotate(total_payments_jun=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jun')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jun = 0
        occupants_with_zero_or_negative_balance_jun = 0
        
        for occupant_bill_jun in occupant_bills_jun:
            total_payments_jun = 0
            for occupant_payment_jun in occupant_payments_jun:
                if occupant_payment_jun['id'] == occupant_bill_jun['id']:
                    total_payments_jun = occupant_payment_jun['total_payments_jun']
                    break
            remaining_balance_jun = occupant_bill_jun['total_bills_jun'] - total_payments_jun
            if remaining_balance_jun > 0:
                occupants_with_balance_jun += 1
            else:
                occupants_with_zero_or_negative_balance_jun += 1

        Jun_PatiallyPaid_Per = (occupants_with_balance_jun / Jun) * 100 if Jun != 0 else 0
        Jun_PatiallyPaid_Per = int(round(Jun_PatiallyPaid_Per))

        Jun_Paid_Per = (occupants_with_zero_or_negative_balance_jun / Jun) * 100 if Jun != 0 else 0
        Jun_Paid_Per = int(round(Jun_Paid_Per))


        # Partially Paid and Paid in July
        occupant_bills_jul = Occupant.objects.filter(bill_details__created_at__icontains="2023-07")\
            .annotate(total_bills_jul=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jul')\
            .distinct().order_by('person__last_name')

        occupant_payments_jul = Occupant.objects.filter(payment__created_at__icontains="2023-07")\
            .annotate(total_payments_jul=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jul')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jul = 0
        occupants_with_zero_or_negative_balance_jul = 0
        
        for occupant_bill_jul in occupant_bills_jul:
            total_payments_jul = 0
            for occupant_payment_jul in occupant_payments_jul:
                if occupant_payment_jul['id'] == occupant_bill_jul['id']:
                    total_payments_jul = occupant_payment_jul['total_payments_jul']
                    break
            remaining_balance_jul = occupant_bill_jul['total_bills_jul'] - total_payments_jul
            if remaining_balance_jul > 0:
                occupants_with_balance_jul += 1
            else:
                occupants_with_zero_or_negative_balance_jul += 1

        Jul_PatiallyPaid_Per = (occupants_with_balance_jul / Jul) * 100 if Jul != 0 else 0
        Jul_PatiallyPaid_Per = int(round(Jul_PatiallyPaid_Per))

        Jul_Paid_Per = (occupants_with_zero_or_negative_balance_jul / Jul) * 100 if Jul != 0 else 0
        Jul_Paid_Per = int(round(Jul_Paid_Per))


        # Partially Paid and Paid in August
        occupant_bills_aug = Occupant.objects.filter(bill_details__created_at__icontains="2023-08")\
            .annotate(total_bills_aug=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_aug')\
            .distinct().order_by('person__last_name')

        occupant_payments_aug = Occupant.objects.filter(payment__created_at__icontains="2023-08")\
            .annotate(total_payments_aug=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_aug')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_aug = 0
        occupants_with_zero_or_negative_balance_aug = 0

        for occupant_bill_aug in occupant_bills_aug:
            total_payments_aug = 0
            for occupant_payment_aug in occupant_payments_aug:
                if occupant_payment_aug['id'] == occupant_bill_aug['id']:
                    total_payments_aug = occupant_payment_aug['total_payments_aug']
                    break
            remaining_balance_aug = occupant_bill_aug['total_bills_aug'] - total_payments_aug
            if remaining_balance_aug > 0:
                occupants_with_balance_aug += 1
            else:
                occupants_with_zero_or_negative_balance_aug += 1

        Aug_PatiallyPaid_Per = (occupants_with_balance_aug / Aug) * 100 if Aug != 0 else 0
        Aug_PatiallyPaid_Per = int(round(Aug_PatiallyPaid_Per))

        Aug_Paid_Per = (occupants_with_zero_or_negative_balance_aug / Aug) * 100 if Aug != 0 else 0
        Aug_Paid_Per = int(round(Aug_Paid_Per))


        # Partially Paid and Paid in September
        occupant_bills_sep = Occupant.objects.filter(bill_details__created_at__icontains="2023-09")\
            .annotate(total_bills_sep=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_sep')\
            .distinct().order_by('person__last_name')

        occupant_payments_sep = Occupant.objects.filter(payment__created_at__icontains="2023-09")\
            .annotate(total_payments_sep=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_sep')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_sep = 0
        occupants_with_zero_or_negative_balance_sep = 0
        
        for occupant_bill_sep in occupant_bills_sep:
            total_payments_sep = 0
            for occupant_payment_sep in occupant_payments_sep:
                if occupant_payment_sep['id'] == occupant_bill_sep['id']:
                    total_payments_sep = occupant_payment_sep['total_payments_sep']
                    break
            remaining_balance_sep = occupant_bill_sep['total_bills_aug'] - total_payments_sep
            if remaining_balance_sep > 0:
                occupants_with_balance_sep += 1
            else:
                occupants_with_zero_or_negative_balance_sep += 1

        Sep_PatiallyPaid_Per = (occupants_with_balance_sep / Sep) * 100 if Sep != 0 else 0
        Sep_PatiallyPaid_Per = int(round(Sep_PatiallyPaid_Per))

        Sep_Paid_Per = (occupants_with_zero_or_negative_balance_sep / Sep) * 100 if Sep != 0 else 0
        Sep_Paid_Per = int(round(Sep_Paid_Per))


        # Partially Paid and Paid in October
        occupant_bills_oct = Occupant.objects.filter(bill_details__created_at__icontains="2023-10")\
            .annotate(total_bills_oct=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_oct')\
            .distinct().order_by('person__last_name')

        occupant_payments_oct = Occupant.objects.filter(payment__created_at__icontains="2023-10")\
            .annotate(total_payments_oct=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_oct')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_oct = 0
        occupants_with_zero_or_negative_balance_oct = 0
        
        for occupant_bill_oct in occupant_bills_oct:
            total_payments_oct = 0
            for occupant_payment_oct in occupant_payments_oct:
                if occupant_payment_oct['id'] == occupant_bill_oct['id']:
                    total_payments_oct = occupant_payment_oct['total_payments_oct']
                    break
            remaining_balance_oct = occupant_bill_oct['total_bills_oct'] - total_payments_oct
            if remaining_balance_oct > 0:
                occupants_with_balance_oct += 1
            else:
                occupants_with_zero_or_negative_balance_oct += 1

        Oct_PatiallyPaid_Per = (occupants_with_balance_oct / Oct) * 100 if Oct != 0 else 0
        Oct_PatiallyPaid_Per = int(round(Oct_PatiallyPaid_Per))

        Oct_Paid_Per = (occupants_with_zero_or_negative_balance_oct / Oct) * 100 if Oct != 0 else 0
        Oct_Paid_Per = int(round(Oct_Paid_Per))


        # Partially Paid and Paid in November
        occupant_bills_nov = Occupant.objects.filter(bill_details__created_at__icontains="2023-11")\
            .annotate(total_bills_nov=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_nov')\
            .distinct().order_by('person__last_name')

        occupant_payments_nov = Occupant.objects.filter(payment__created_at__icontains="2023-11")\
            .annotate(total_payments_nov=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_nov')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_nov = 0
        occupants_with_zero_or_negative_balance_nov = 0

        for occupant_bill_nov in occupant_bills_nov:
            total_payments_nov = 0
            for occupant_payment_nov in occupant_payments_nov:
                if occupant_payment_nov['id'] == occupant_bill_nov['id']:
                    total_payments_nov = occupant_payment_nov['total_payments_nov']
                    break
            remaining_balance_nov = occupant_bill_nov['total_bills_nov'] - total_payments_nov
            if remaining_balance_nov > 0:
                occupants_with_balance_nov += 1
            else:
                occupants_with_zero_or_negative_balance_nov += 1

        Nov_PatiallyPaid_Per = (occupants_with_balance_nov / Nov) * 100 if Nov != 0 else 0
        Nov_PatiallyPaid_Per = int(round(Nov_PatiallyPaid_Per))

        Nov_Paid_Per = (occupants_with_zero_or_negative_balance_nov / Nov) * 100 if Nov != 0 else 0
        Nov_Paid_Per = int(round(Nov_Paid_Per))


        # Partially Paid and Paid in December
        occupant_bills_dec = Occupant.objects.filter(bill_details__created_at__icontains="2023-12")\
            .annotate(total_bills_dec=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_dec')\
            .distinct().order_by('person__last_name')

        occupant_payments_dec = Occupant.objects.filter(payment__created_at__icontains="2023-12")\
            .annotate(total_payments_dec=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_dec')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_dec = 0
        occupants_with_zero_or_negative_balance_dec = 0
        
        for occupant_bill_dec in occupant_bills_dec:
            total_payments_dec = 0
            for occupant_payment_dec in occupant_payments_dec:
                if occupant_payment_dec['id'] == occupant_bill_dec['id']:
                    total_payments_dec = occupant_payment_dec['total_payments_dec']
                    break
            remaining_balance_dec = occupant_bill_dec['total_bills_dec'] - total_payments_dec
            if remaining_balance_dec > 0:
                occupants_with_balance_dec += 1
            else:
                occupants_with_zero_or_negative_balance_nov += 1

        Dec_PatiallyPaid_Per = (occupants_with_balance_dec / Dec) * 100 if Dec != 0 else 0
        Dec_PatiallyPaid_Per = int(round(Dec_PatiallyPaid_Per))

        Dec_Paid_Per = (occupants_with_zero_or_negative_balance_dec / Dec) * 100 if Dec != 0 else 0
        Dec_Paid_Per = int(round(Dec_Paid_Per))


        partiallypaid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        partiallypaid_monthly_occ_per = [Jan_PatiallyPaid_Per, Feb_PatiallyPaid_Per, Mar_PatiallyPaid_Per, Apr_PatiallyPaid_Per,
                                          May_PatiallyPaid_Per, Jun_PatiallyPaid_Per, Jul_PatiallyPaid_Per, Aug_PatiallyPaid_Per, 
                                          Sep_PatiallyPaid_Per, Oct_PatiallyPaid_Per, Nov_PatiallyPaid_Per, Dec_PatiallyPaid_Per]
        
        context['partiallypaid_monthly_occ_per_list'] = partiallypaid_monthly_occ_per_list
        context['partiallypaid_monthly_occ_per'] = partiallypaid_monthly_occ_per


        paid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        paid_monthly_occ_per = [Jan_Paid_Per, Feb_Paid_Per, Mar_Paid_Per, Apr_Paid_Per,
                                May_Paid_Per, Jun_Paid_Per, Jul_Paid_Per, Aug_Paid_Per, 
                                Sep_Paid_Per, Oct_Paid_Per, Nov_Paid_Per, Dec_Paid_Per]
        
        context['paid_monthly_occ_per_list'] = paid_monthly_occ_per_list
        context['paid_monthly_occ_per'] = paid_monthly_occ_per


        return context


# @method_decorator(login_required, name='dispatch')
class ASDashMaleVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'accountingstaff/as_dash_male_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ASDashMaleVacantBed, self).get_queryset(*args, **kwargs)
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
class ASDashFemaleVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'accountingstaff/as_dash_female_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ASDashFemaleVacantBed, self).get_queryset(*args, **kwargs)
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
class ASDashForeignVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'accountingstaff/as_dash_foreign_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ASDashForeignVacantBed, self).get_queryset(*args, **kwargs)
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
class ASOccupantList(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'accountingstaff/as_occupant_list.html'
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
        qs = super(ASOccupantList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-created_at").filter(Q(person__last_name__icontains=query) | Q(person__first_name__icontains=query)
            | Q(bed__bed_code__icontains=query) | Q(person__boarder_type__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class ASOccupantView(UpdateView):
    model = Occupant
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'accountingstaff/as_occupant_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fetch_first_three'] = Bill_Details.objects.filter(occupant=self.object.id)[:3]
        context['billing_details'] = Bill_Details.objects.filter(occupant=self.object.id)[3:]
        context['total_bills_amount'] = Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['payment'] = Payment.objects.filter(occupant=self.object.id)
        context['total_payment_amount'] = Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['remaining_balance'] = (Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0)
        context['occupant_demerits'] = OccupantDemerit.objects.filter(occupant=self.object.id)

        cursor = connections['default'].cursor()
        query = f"UPDATE dormitory_occupantdemerit SET new_remarks = null "
        cursor.execute(query)

        return context

    def form_valid(self, form):
      messages.success(self.request, "Occupant details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class ASOccMonthRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'accountingstaff/as_occ_month_rep.html'
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
class ASOccYearRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'accountingstaff/as_occ_year_rep.html'
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
class ASBillingList(ListView):
    model = Bill_Details
    context_object_name = 'occupant'
    template_name = 'accountingstaff/as_billing_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bills'] = Bill_Details.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ASBillingList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(service__service_name__icontains=query)
            | Q(description__icontains=query) | Q(amount__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class ASPaymentList(ListView):
    model = Payment
    context_object_name = 'payment'
    template_name = 'accountingstaff/as_payment_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment'] = Payment.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ASPaymentList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(payment_date__icontains=query)
            | Q(amount__icontains=query) | Q(receipt_no__iexact=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class ASPaymentUpdateView(UpdateView):
    model = Payment
    fields = "__all__"
    context_object_name = 'payment'
    template_name = 'accountingstaff/as_payment_update.html'
    success_url = "/as_payment_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Payment details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class ASOccupantViewPaymentUpdate(UpdateView):
    model = Payment
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'accountingstaff/as_payment_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(f"ID {self.object.occupant_id}")
        return context

    def get_success_url(self):
        return reverse('ASOccupantView', kwargs={'pk': self.object.occupant_id})

    def form_valid(self, form):
      messages.success(self.request, "Occupant payment was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class ASServiceList(ListView):
    model = Service
    context_object_name = 'service'
    template_name = 'accountingstaff/as_service_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services']= Service.objects.all().exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others').count()
        context['available'] = Service.objects.filter(status__iexact="Available").exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others').count()
        context['notavailable'] = Service.objects.filter(status__iexact="Not Available").count()
        context['services_limit']= Service.objects.all().exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others')
    
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ASServiceList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("service_name").filter(Q(service_name__icontains=query) | Q(status__icontains=query)
            | Q(base_amount__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class ASAdminProfile(ListView):
    model = Admin
    context_object_name = 'admin'
    template_name = "accountingstaff/as_admin_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global ac
        context ['acc'] = Admin.objects.filter(Q(username=ac)).values()
        return context

# @method_decorator(login_required, name='dispatch')
class ASAdminProfileUpdateView(UpdateView):
    model = Admin
    fields = ['firstname', 'lastname', 'username', 'password', 'security_question', 'security_answer', 'recovery_email']
    context_object_name = 'admin'
    template_name = 'accountingstaff/as_admin_profile_update.html'
    success_url = "/as_admin_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Your Account Information was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# ===================================================
# End of Accountingstaff
# ===================================================

# ===================================================
# Start of Dormmanager
# ===================================================
# @method_decorator(login_required, name='dispatch')
class DMHomePageView(ListView):
    model = Room
    context_object_name = 'room'
    template_name = "landingpage/dm_home.html"

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
            
        # Students Gender Charts
        male_no = Person.objects.filter(gender="Male").count()
        male_no = int(male_no)

        female_no = Person.objects.filter(gender="Female").count()
        female_no = int(female_no)

        lgbt_no = Person.objects.filter(gender="LGBTQIA+").count()
        lgbt_no = int(lgbt_no)

        gender_list = ['Male', 'Female', 'LGBTQIA+']
        gender_number = [male_no, female_no, lgbt_no]

        context['gender_list'] = gender_list
        context['gender_number'] = gender_number

                
        # Monthly Registration Charts
        Jan_Reg = Person.objects.filter(created_at__icontains="2023-01").count()
        Jan_Reg = int(Jan_Reg)

        Feb_Reg = Person.objects.filter(created_at__icontains="2023-02").count()
        Feb_Reg = int(Feb_Reg)

        Mar_Reg = Person.objects.filter(created_at__icontains="2023-03").count()
        Mar_Reg = int(Mar_Reg)

        Apr_Reg = Person.objects.filter(created_at__icontains="2023-04").count()
        Apr_Reg = int(Apr_Reg)

        May_Reg = Person.objects.filter(created_at__icontains="2023-05").count()
        May_Reg = int(May_Reg)

        Jun_Reg = Person.objects.filter(created_at__icontains="2023-06").count()
        Jun_Reg = int(Jun_Reg)

        Jul_Reg = Person.objects.filter(created_at__icontains="2023-07").count()
        Jul_Reg = int(Jul_Reg)

        Aug_Reg = Person.objects.filter(created_at__icontains="2023-08").count()
        Aug_Reg = int(Aug_Reg)

        Sep_Reg = Person.objects.filter(created_at__icontains="2023-09").count()
        Sep_Reg = int(Sep_Reg)

        Oct_Reg = Person.objects.filter(created_at__icontains="2023-10").count()
        Oct_Reg = int(Oct_Reg)

        Nov_Reg = Person.objects.filter(created_at__icontains="2023-11").count()
        Nov_Reg = int(Nov_Reg)

        Dec_Reg = Person.objects.filter(created_at__icontains="2023-12").count()
        Dec_Reg = int(Dec_Reg)

        monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_number = [Jan_Reg, Feb_Reg, Mar_Reg, Apr_Reg, May_Reg, Jun_Reg, Jul_Reg, Aug_Reg, Sep_Reg, Oct_Reg, Nov_Reg, Dec_Reg]

        context['monthly_list'] = monthly_list
        context['monthly_number'] = monthly_number


        # Monthly Occupant Charts
        Jan = Occupant.objects.filter(created_at__icontains="2023-01").count()
        Jan = int(Jan)

        Feb = Occupant.objects.filter(created_at__icontains="2023-02").count()
        Feb = int(Feb)

        Mar = Occupant.objects.filter(created_at__icontains="2023-03").count()
        Mar = int(Mar)

        Apr = Occupant.objects.filter(created_at__icontains="2023-04").count()
        Apr = int(Apr)

        May = Occupant.objects.filter(created_at__icontains="2023-05").count()
        May = int(May)

        Jun = Occupant.objects.filter(created_at__icontains="2023-06").count()
        Jun = int(Jun)

        Jul = Occupant.objects.filter(created_at__icontains="2023-07").count()
        Jul = int(Jul)

        Aug = Occupant.objects.filter(created_at__icontains="2023-08").count()
        Aug = int(Aug)

        Sep = Occupant.objects.filter(created_at__icontains="2023-09").count()
        Sep = int(Sep)

        Oct = Occupant.objects.filter(created_at__icontains="2023-10").count()
        Oct = int(Oct)

        Nov = Occupant.objects.filter(created_at__icontains="2023-11").count()
        Nov = int(Nov)

        Dec = Occupant.objects.filter(created_at__icontains="2023-12").count()
        Dec = int(Dec)

        occ_monthly_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        occ_monthly_number = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

        context['occ_monthly_list'] = occ_monthly_list
        context['occ_monthly_number'] = occ_monthly_number


        # Monthly Male Charts
        Jan_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="Male").count()
        Jan_Male_Per = (Jan_Tot_Male / Jan) * 100 if Jan != 0 else 0
        Jan_Male_Per = int(round(Jan_Male_Per))

        Feb_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="Male").count()
        Feb_Male_Per = (Feb_Tot_Male / Feb) * 100 if Feb != 0 else 0
        Feb_Male_Per = int(round(Feb_Male_Per))

        Mar_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="Male").count()
        Mar_Male_Per = (Mar_Tot_Male / Mar) * 100 if Mar != 0 else 0
        Mar_Male_Per = int(round(Mar_Male_Per))

        Apr_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="Male").count()
        Apr_Male_Per = (Apr_Tot_Male / Apr) * 100 if Apr != 0 else 0
        Apr_Male_Per = int(round(Apr_Male_Per))

        May_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="Male").count()
        May_Male_Per = (May_Tot_Male / May) * 100 if May != 0 else 0
        May_Male_Per = int(round(May_Male_Per))

        Jun_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="Male").count()
        Jun_Male_Per = (Jun_Tot_Male / Jun) * 100 if Jun != 0 else 0
        Jun_Male_Per = int(round(Jun_Male_Per))

        Jul_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="Male").count()
        Jul_Male_Per = (Jul_Tot_Male / Jul) * 100 if Jul != 0 else 0
        Jul_Male_Per = int(round(Jul_Male_Per))

        Aug_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="Male").count()
        Aug_Male_Per = (Aug_Tot_Male / Aug) * 100 if Aug != 0 else 0
        Aug_Male_Per = int(round(Aug_Male_Per))

        Sep_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="Male").count()
        Sep_Male_Per = (Sep_Tot_Male / Sep) * 100 if Sep != 0 else 0
        Sep_Male_Per = int(round(Sep_Male_Per))

        Oct_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="Male").count()
        Oct_Male_Per = (Oct_Tot_Male / Oct) * 100 if Oct != 0 else 0
        Oct_Male_Per = int(round(Oct_Male_Per))

        Nov_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="Male").count()
        Nov_Male_Per = (Nov_Tot_Male / Nov) * 100 if Nov != 0 else 0
        Nov_Male_Per = int(round(Nov_Male_Per))

        Dec_Tot_Male = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="Male").count()
        Dec_Male_Per = (Dec_Tot_Male / Dec) * 100 if Dec != 0 else 0
        Dec_Male_Per = int(round(Dec_Male_Per))

        male_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        male_monthly_occ_per = [Jan_Male_Per, Feb_Male_Per, Mar_Male_Per, Apr_Male_Per, May_Male_Per, Jun_Male_Per, 
                                Jul_Male_Per, Aug_Male_Per, Sep_Male_Per, Oct_Male_Per, Nov_Male_Per, Dec_Male_Per]
        
        context['male_monthly_occ_per_list'] = male_monthly_occ_per_list
        context['male_monthly_occ_per'] = male_monthly_occ_per
        

        # Monthly Female Charts
        Jan_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="Female").count()
        Jan_Female_Per = (Jan_Tot_Female / Jan) * 100 if Jan != 0 else 0
        Jan_Female_Per = int(round(Jan_Female_Per))

        Feb_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="Female").count()
        Feb_Female_Per = (Feb_Tot_Female / Feb) * 100 if Feb != 0 else 0
        Feb_Female_Per = int(round(Feb_Female_Per))

        Mar_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="Female").count()
        Mar_Female_Per = (Mar_Tot_Female / Mar) * 100 if Mar != 0 else 0
        Mar_Female_Per = int(round(Mar_Female_Per))

        Apr_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="Female").count()
        Apr_Female_Per = (Apr_Tot_Female / Apr) * 100 if Apr != 0 else 0
        Apr_Female_Per = int(round(Apr_Female_Per))

        May_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="Female").count()
        May_Female_Per = (May_Tot_Female / May) * 100 if May != 0 else 0
        May_Female_Per = int(round(May_Female_Per))

        Jun_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="Female").count()
        Jun_Female_Per = (Jun_Tot_Female / Jun) * 100 if Jun != 0 else 0
        Jun_Female_Per = int(round(Jun_Female_Per))

        Jul_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="Female").count()
        Jul_Female_Per = (Jul_Tot_Female / Jul) * 100 if Jul != 0 else 0
        Jul_Female_Per = int(round(Jul_Female_Per))

        Aug_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="Female").count()
        Aug_Female_Per = (Aug_Tot_Female / Aug) * 100 if Aug != 0 else 0
        Aug_Female_Per = int(round(Aug_Female_Per))

        Sep_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="Female").count()
        Sep_Female_Per = (Sep_Tot_Female / Sep) * 100 if Sep != 0 else 0
        Sep_Female_Per = int(round(Sep_Female_Per))

        Oct_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="Female").count()
        Oct_Female_Per = (Oct_Tot_Female/ Oct) * 100 if Oct != 0 else 0
        Oct_Female_Per = int(round(Oct_Female_Per))

        Nov_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="Female").count()
        Nov_Female_Per = (Nov_Tot_Female / Nov) * 100 if Nov != 0 else 0
        Nov_Female_Per = int(round(Nov_Female_Per))

        Dec_Tot_Female = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="Female").count()
        Dec_Female_Per = (Dec_Tot_Female / Dec) * 100 if Dec != 0 else 0
        Dec_Female_Per = int(round(Dec_Female_Per))

        female_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        female_monthly_occ_per = [Jan_Female_Per, Feb_Female_Per, Mar_Female_Per, Apr_Female_Per, May_Female_Per, Jun_Female_Per, 
                                Jul_Female_Per, Aug_Female_Per, Sep_Female_Per, Oct_Female_Per, Nov_Female_Per, Dec_Female_Per]
        
        context['female_monthly_occ_per_list'] = female_monthly_occ_per_list
        context['female_monthly_occ_per'] = female_monthly_occ_per


        # Monthly LGBTQIA+ Charts
        Jan_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-01", person__gender__iexact="LGBTQIA+").count()
        Jan_LGBTQIA_Per = (Jan_Tot_LGBTQIA / Jan) * 100 if Jan != 0 else 0
        Jan_LGBTQIA_Per = int(round(Jan_LGBTQIA_Per))

        Feb_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-02", person__gender__iexact="LGBTQIA+").count()
        Feb_LGBTQIA_Per = (Feb_Tot_LGBTQIA / Feb) * 100 if Feb != 0 else 0
        Feb_LGBTQIA_Per = int(round(Feb_LGBTQIA_Per))

        Mar_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-03", person__gender__iexact="LGBTQIA+").count()
        Mar_LGBTQIA_Per = (Mar_Tot_Female / Mar) * 100 if Mar != 0 else 0
        Mar_LGBTQIA_Per = int(round(Mar_LGBTQIA_Per))

        Apr_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-04", person__gender__iexact="LGBTQIA+").count()
        Apr_LGBTQIA_Per = (Apr_Tot_LGBTQIA / Apr) * 100 if Apr != 0 else 0
        Apr_LGBTQIA_Per = int(round(Apr_LGBTQIA_Per))

        May_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-05", person__gender__iexact="LGBTQIA+").count()
        May_LGBTQIA_Per = (May_Tot_LGBTQIA / May) * 100 if May != 0 else 0
        May_LGBTQIA_Per = int(round(May_LGBTQIA_Per))

        Jun_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-06", person__gender__iexact="LGBTQIA+").count()
        Jun_LGBTQIA_Per = (Jun_Tot_LGBTQIA / Jun) * 100 if Jun != 0 else 0
        Jun_LGBTQIA_Per = int(round(Jun_LGBTQIA_Per))

        Jul_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-07", person__gender__iexact="LGBTQIA+").count()
        Jul_LGBTQIA_Per = (Jul_Tot_LGBTQIA / Jul) * 100 if Jul != 0 else 0
        Jul_LGBTQIA_Per = int(round(Jul_LGBTQIA_Per))

        Aug_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-08", person__gender__iexact="LGBTQIA+").count()
        Aug_LGBTQIA_Per = (Aug_Tot_LGBTQIA / Aug) * 100 if Aug != 0 else 0
        Aug_LGBTQIA_Per = int(round(Aug_LGBTQIA_Per))

        Sep_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-09", person__gender__iexact="LGBTQIA+").count()
        Sep_LGBTQIA_Per = (Sep_Tot_LGBTQIA / Sep) * 100 if Sep != 0 else 0
        Sep_LGBTQIA_Per = int(round(Sep_LGBTQIA_Per))

        Oct_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-10", person__gender__iexact="LGBTQIA+").count()
        Oct_LGBTQIA_Per = (Oct_Tot_LGBTQIA/ Oct) * 100 if Oct != 0 else 0
        Oct_LGBTQIA_Per = int(round(Oct_LGBTQIA_Per))

        Nov_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-11", person__gender__iexact="LGBTQIA+").count()
        Nov_LGBTQIA_Per = (Nov_Tot_LGBTQIA / Nov) * 100 if Nov != 0 else 0
        Nov_LGBTQIA_Per = int(round(Nov_LGBTQIA_Per))

        Dec_Tot_LGBTQIA = Occupant.objects.filter(start_date__icontains="2023-12", person__gender__iexact="LGBTQIA+").count()
        Dec_LGBTQIA_Per = (Dec_Tot_LGBTQIA / Dec) * 100 if Dec != 0 else 0
        Dec_LGBTQIA_Per = int(round(Dec_LGBTQIA_Per))

        LGBTQIA_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        LGBTQIA_monthly_occ_per = [Jan_LGBTQIA_Per, Feb_LGBTQIA_Per, Mar_LGBTQIA_Per, Apr_LGBTQIA_Per, May_LGBTQIA_Per, Jun_LGBTQIA_Per, 
                                    Jul_LGBTQIA_Per, Aug_LGBTQIA_Per, Sep_LGBTQIA_Per, Oct_LGBTQIA_Per, Nov_LGBTQIA_Per, Dec_LGBTQIA_Per]
        
        context['LGBTQIA_monthly_occ_per_list'] = LGBTQIA_monthly_occ_per_list
        context['LGBTQIA_monthly_occ_per'] = LGBTQIA_monthly_occ_per

        
        # Monthly Unpaid Charts
        Jan_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-01", payment__isnull=False).distinct().count()
        Jan_Unpaid_Per = (Jan_Unpaid_Occ / Jan) * 100 if Jan != 0 else 0
        Jan_Unpaid_Per = int(round(Jan_Unpaid_Per))

        Feb_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-02", payment__isnull=False).distinct().count()
        Feb_Unpaid_Per = (Feb_Unpaid_Occ / Feb) * 100 if Feb != 0 else 0
        Feb_Unpaid_Per = int(round(Feb_Unpaid_Per))

        Mar_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-03", payment__isnull=False).distinct().count()
        Mar_Unpaid_Per = (Mar_Unpaid_Occ / Mar) * 100 if Mar != 0 else 0
        Mar_Unpaid_Per = int(round(Mar_Unpaid_Per))

        Apr_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-04", payment__isnull=False).distinct().count()
        Apr_Unpaid_Per = (Apr_Unpaid_Occ / Apr) * 100 if Apr != 0 else 0
        Apr_Unpaid_Per = int(round(Apr_Unpaid_Per))

        May_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-05", payment__isnull=False).distinct().count()
        May_Unpaid_Per = (May_Unpaid_Occ / May) * 100 if May != 0 else 0
        May_Unpaid_Per = int(round(May_Unpaid_Per))

        Jun_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-06", payment__isnull=False).distinct().count()
        Jun_Unpaid_Per = (Jun_Unpaid_Occ / Jun) * 100 if Jun != 0 else 0
        Jun_Unpaid_Per = int(round(Jun_Unpaid_Per))

        Jul_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-07", payment__isnull=False).distinct().count()
        Jul_Unpaid_Per = (Jul_Unpaid_Occ / Jul) * 100 if Jul != 0 else 0
        Jul_Unpaid_Per = int(round(Jul_Unpaid_Per))

        Aug_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-08", payment__isnull=False).distinct().count()
        Aug_Unpaid_Per = (Aug_Unpaid_Occ / Aug) * 100 if Aug != 0 else 0
        Aug_Unpaid_Per = int(round(Aug_Unpaid_Per))

        Sep_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-09", payment__isnull=False).distinct().count()
        Sep_Unpaid_Per = (Sep_Unpaid_Occ / Sep) * 100 if Sep != 0 else 0
        Sep_Unpaid_Per = int(round(Sep_Unpaid_Per))

        Oct_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-10", payment__isnull=False).distinct().count()
        Oct_Unpaid_Per = (Oct_Unpaid_Occ / Oct) * 100 if Oct != 0 else 0
        Oct_Unpaid_Per = int(round(Oct_Unpaid_Per))

        Nov_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-11", payment__isnull=False).distinct().count()
        Nov_Unpaid_Per = (Nov_Unpaid_Occ / Nov) * 100 if Nov != 0 else 0
        Nov_Unpaid_Per = int(round(Nov_Unpaid_Per))

        Dec_Unpaid_Occ = Occupant.objects.exclude(payment__created_at__icontains="2023-12", payment__isnull=False).distinct().count()
        Dec_Unpaid_Per = (Dec_Unpaid_Occ / Dec) * 100 if Dec != 0 else 0
        Dec_Unpaid_Per = int(round(Dec_Unpaid_Per))


        unpaid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        unpaid_monthly_occ_per = [Jan_Unpaid_Per, Feb_Unpaid_Per, Mar_Unpaid_Per, Apr_Unpaid_Per, May_Unpaid_Per, Jun_Unpaid_Per, 
                                Jul_Unpaid_Per, Aug_Unpaid_Per, Sep_Unpaid_Per, Oct_Unpaid_Per, Nov_Unpaid_Per, Dec_Unpaid_Per]
        
        context['unpaid_monthly_occ_per_list'] = unpaid_monthly_occ_per_list
        context['unpaid_monthly_occ_per'] = unpaid_monthly_occ_per


        # Monthly Paid Charts

        # Partially Paid and Paid in January
        occupant_bills_jan = Occupant.objects.filter(bill_details__created_at__icontains="2023-01")\
            .annotate(total_bills_jan=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jan')\
            .distinct().order_by('person__last_name')

        occupant_payments_jan = Occupant.objects.filter(payment__created_at__icontains="2023-01")\
            .annotate(total_payments_jan=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jan')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jan = 0
        occupants_with_zero_or_negative_balance_jan = 0

        for occupant_bill_jan in occupant_bills_jan:
            total_payments_jan = 0
            for occupant_payment_jan in occupant_payments_jan:
                if occupant_payment_jan['id'] == occupant_bill_jan['id']:
                    total_payments_jan = occupant_payment_jan['total_payments_jan']
                    break
            remaining_balance_jan = occupant_bill_jan['total_bills_jan'] - total_payments_jan
            if remaining_balance_jan > 0:
                occupants_with_balance_jan += 1
            else:
                occupants_with_zero_or_negative_balance_jan += 1

        Jan_PatiallyPaid_Per = (occupants_with_balance_jan / Jan) * 100 if Jan != 0 else 0
        Jan_PatiallyPaid_Per = int(round(Jan_PatiallyPaid_Per))

        Jan_Paid_Per = (occupants_with_zero_or_negative_balance_jan / Jan) * 100 if Jan != 0 else 0
        Jan_Paid_Per = int(round(Jan_Paid_Per))


        # Partially Paid and Paid in February
        occupant_bills_feb = Occupant.objects.filter(bill_details__created_at__icontains="2023-02")\
            .annotate(total_bills_feb=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_feb')\
            .distinct().order_by('person__last_name')

        occupant_payments_feb = Occupant.objects.filter(payment__created_at__icontains="2023-02")\
            .annotate(total_payments_feb=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_feb')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_feb = 0
        occupants_with_zero_or_negative_balance_feb = 0

        for occupant_bill_feb in occupant_bills_feb:
            total_payments_feb = 0
            for occupant_payment_feb in occupant_payments_feb:
                if occupant_payment_feb['id'] == occupant_bill_feb['id']:
                    total_payments_feb = occupant_payment_feb['total_payments_feb']
                    break
            remaining_balance_feb = occupant_bill_feb['total_bills_feb'] - total_payments_feb
            if remaining_balance_feb > 0:
                occupants_with_balance_feb += 1
            else:
                occupants_with_zero_or_negative_balance_feb += 1

        Feb_PatiallyPaid_Per = (occupants_with_balance_feb / Feb) * 100 if Feb != 0 else 0
        Feb_PatiallyPaid_Per = int(round(Feb_PatiallyPaid_Per))

        Feb_Paid_Per = (occupants_with_zero_or_negative_balance_feb / Feb) * 100 if Feb != 0 else 0
        Feb_Paid_Per = int(round(Feb_Paid_Per))


        # Partially Paid and Paid in March
        occupant_bills_mar = Occupant.objects.filter(bill_details__created_at__icontains="2023-03")\
            .annotate(total_bills_mar=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_mar')\
            .distinct().order_by('person__last_name')

        occupant_payments_mar = Occupant.objects.filter(payment__created_at__icontains="2023-03")\
            .annotate(total_payments_mar=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_mar')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_mar = 0
        occupants_with_zero_or_negative_balance_mar = 0

        for occupant_bill_mar in occupant_bills_mar:
            total_payments_mar = 0
            for occupant_payment_mar in occupant_payments_mar:
                if occupant_payment_mar['id'] == occupant_bill_mar['id']:
                    total_payments_mar = occupant_payment_mar['total_payments_mar']
                    break
            remaining_balance_mar = occupant_bill_mar['total_bills_mar'] - total_payments_mar
            if remaining_balance_mar > 0:
                occupants_with_balance_mar += 1
            else:
                occupants_with_zero_or_negative_balance_mar += 1

        Mar_PatiallyPaid_Per = (occupants_with_balance_mar / Mar) * 100 if Mar != 0 else 0
        Mar_PatiallyPaid_Per = int(round(Mar_PatiallyPaid_Per))

        Mar_Paid_Per = (occupants_with_zero_or_negative_balance_mar / Mar) * 100 if Mar != 0 else 0
        Mar_Paid_Per = int(round(Mar_Paid_Per))


        # Partially Paid and Paid in April
        occupant_bills_apr = Occupant.objects.filter(bill_details__created_at__icontains="2023-04")\
            .annotate(total_bills_apr=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_apr')\
            .distinct().order_by('person__last_name')

        occupant_payments_apr = Occupant.objects.filter(payment__created_at__icontains="2023-04")\
            .annotate(total_payments_apr=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_apr')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_apr = 0
        occupants_with_zero_or_negative_balance_apr = 0

        for occupant_bill_apr in occupant_bills_apr:
            total_payments_apr = 0
            for occupant_payment_apr in occupant_payments_apr:
                if occupant_payment_apr['id'] == occupant_bill_apr['id']:
                    total_payments_apr = occupant_payment_apr['total_payments_apr']
                    break
            remaining_balance_apr = occupant_bill_apr['total_bills_apr'] - total_payments_apr
            if remaining_balance_apr > 0:
                occupants_with_balance_apr += 1
            else:
                occupants_with_zero_or_negative_balance_apr += 1

        Apr_PatiallyPaid_Per = (occupants_with_balance_apr / Apr) * 100 if Apr != 0 else 0
        Apr_PatiallyPaid_Per = int(round(Apr_PatiallyPaid_Per))

        Apr_Paid_Per = (occupants_with_zero_or_negative_balance_apr / Apr) * 100 if Apr != 0 else 0
        Apr_Paid_Per = int(round(Apr_Paid_Per))


        # Partially Paid and Paid in May
        occupant_bills_may = Occupant.objects.filter(bill_details__created_at__icontains="2023-05")\
            .annotate(total_bills_may=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_may')\
            .distinct().order_by('person__last_name')

        occupant_payments_may = Occupant.objects.filter(payment__created_at__icontains="2023-05")\
            .annotate(total_payments_may=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_may')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_may = 0
        occupants_with_zero_or_negative_balance_may = 0
        
        for occupant_bill_may in occupant_bills_may:
            total_payments_may = 0
            for occupant_payment_may in occupant_payments_may:
                if occupant_payment_may['id'] == occupant_bill_may['id']:
                    total_payments_may = occupant_payment_may['total_payments_may']
                    break
            remaining_balance_may = occupant_bill_may['total_bills_may'] - total_payments_may
            if remaining_balance_may > 0:
                occupants_with_balance_may += 1
            else:
                occupants_with_zero_or_negative_balance_may += 1

        May_PatiallyPaid_Per = (occupants_with_balance_may / May) * 100 if May != 0 else 0
        May_PatiallyPaid_Per = int(round(May_PatiallyPaid_Per))

        May_Paid_Per = (occupants_with_zero_or_negative_balance_may / May) * 100 if May != 0 else 0
        May_Paid_Per = int(round(May_Paid_Per))

        
        # Partially Paid and Paid in June
        occupant_bills_jun = Occupant.objects.filter(bill_details__created_at__icontains="2023-06")\
            .annotate(total_bills_jun=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jun')\
            .distinct().order_by('person__last_name')

        occupant_payments_jun = Occupant.objects.filter(payment__created_at__icontains="2023-06")\
            .annotate(total_payments_jun=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jun')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jun = 0
        occupants_with_zero_or_negative_balance_jun = 0
        
        for occupant_bill_jun in occupant_bills_jun:
            total_payments_jun = 0
            for occupant_payment_jun in occupant_payments_jun:
                if occupant_payment_jun['id'] == occupant_bill_jun['id']:
                    total_payments_jun = occupant_payment_jun['total_payments_jun']
                    break
            remaining_balance_jun = occupant_bill_jun['total_bills_jun'] - total_payments_jun
            if remaining_balance_jun > 0:
                occupants_with_balance_jun += 1
            else:
                occupants_with_zero_or_negative_balance_jun += 1

        Jun_PatiallyPaid_Per = (occupants_with_balance_jun / Jun) * 100 if Jun != 0 else 0
        Jun_PatiallyPaid_Per = int(round(Jun_PatiallyPaid_Per))

        Jun_Paid_Per = (occupants_with_zero_or_negative_balance_jun / Jun) * 100 if Jun != 0 else 0
        Jun_Paid_Per = int(round(Jun_Paid_Per))


        # Partially Paid and Paid in July
        occupant_bills_jul = Occupant.objects.filter(bill_details__created_at__icontains="2023-07")\
            .annotate(total_bills_jul=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_jul')\
            .distinct().order_by('person__last_name')

        occupant_payments_jul = Occupant.objects.filter(payment__created_at__icontains="2023-07")\
            .annotate(total_payments_jul=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_jul')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_jul = 0
        occupants_with_zero_or_negative_balance_jul = 0
        
        for occupant_bill_jul in occupant_bills_jul:
            total_payments_jul = 0
            for occupant_payment_jul in occupant_payments_jul:
                if occupant_payment_jul['id'] == occupant_bill_jul['id']:
                    total_payments_jul = occupant_payment_jul['total_payments_jul']
                    break
            remaining_balance_jul = occupant_bill_jul['total_bills_jul'] - total_payments_jul
            if remaining_balance_jul > 0:
                occupants_with_balance_jul += 1
            else:
                occupants_with_zero_or_negative_balance_jul += 1

        Jul_PatiallyPaid_Per = (occupants_with_balance_jul / Jul) * 100 if Jul != 0 else 0
        Jul_PatiallyPaid_Per = int(round(Jul_PatiallyPaid_Per))

        Jul_Paid_Per = (occupants_with_zero_or_negative_balance_jul / Jul) * 100 if Jul != 0 else 0
        Jul_Paid_Per = int(round(Jul_Paid_Per))


        # Partially Paid and Paid in August
        occupant_bills_aug = Occupant.objects.filter(bill_details__created_at__icontains="2023-08")\
            .annotate(total_bills_aug=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_aug')\
            .distinct().order_by('person__last_name')

        occupant_payments_aug = Occupant.objects.filter(payment__created_at__icontains="2023-08")\
            .annotate(total_payments_aug=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_aug')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_aug = 0
        occupants_with_zero_or_negative_balance_aug = 0

        for occupant_bill_aug in occupant_bills_aug:
            total_payments_aug = 0
            for occupant_payment_aug in occupant_payments_aug:
                if occupant_payment_aug['id'] == occupant_bill_aug['id']:
                    total_payments_aug = occupant_payment_aug['total_payments_aug']
                    break
            remaining_balance_aug = occupant_bill_aug['total_bills_aug'] - total_payments_aug
            if remaining_balance_aug > 0:
                occupants_with_balance_aug += 1
            else:
                occupants_with_zero_or_negative_balance_aug += 1

        Aug_PatiallyPaid_Per = (occupants_with_balance_aug / Aug) * 100 if Aug != 0 else 0
        Aug_PatiallyPaid_Per = int(round(Aug_PatiallyPaid_Per))

        Aug_Paid_Per = (occupants_with_zero_or_negative_balance_aug / Aug) * 100 if Aug != 0 else 0
        Aug_Paid_Per = int(round(Aug_Paid_Per))


        # Partially Paid and Paid in September
        occupant_bills_sep = Occupant.objects.filter(bill_details__created_at__icontains="2023-09")\
            .annotate(total_bills_sep=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_sep')\
            .distinct().order_by('person__last_name')

        occupant_payments_sep = Occupant.objects.filter(payment__created_at__icontains="2023-09")\
            .annotate(total_payments_sep=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_sep')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_sep = 0
        occupants_with_zero_or_negative_balance_sep = 0
        
        for occupant_bill_sep in occupant_bills_sep:
            total_payments_sep = 0
            for occupant_payment_sep in occupant_payments_sep:
                if occupant_payment_sep['id'] == occupant_bill_sep['id']:
                    total_payments_sep = occupant_payment_sep['total_payments_sep']
                    break
            remaining_balance_sep = occupant_bill_sep['total_bills_aug'] - total_payments_sep
            if remaining_balance_sep > 0:
                occupants_with_balance_sep += 1
            else:
                occupants_with_zero_or_negative_balance_sep += 1

        Sep_PatiallyPaid_Per = (occupants_with_balance_sep / Sep) * 100 if Sep != 0 else 0
        Sep_PatiallyPaid_Per = int(round(Sep_PatiallyPaid_Per))

        Sep_Paid_Per = (occupants_with_zero_or_negative_balance_sep / Sep) * 100 if Sep != 0 else 0
        Sep_Paid_Per = int(round(Sep_Paid_Per))


        # Partially Paid and Paid in October
        occupant_bills_oct = Occupant.objects.filter(bill_details__created_at__icontains="2023-10")\
            .annotate(total_bills_oct=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_oct')\
            .distinct().order_by('person__last_name')

        occupant_payments_oct = Occupant.objects.filter(payment__created_at__icontains="2023-10")\
            .annotate(total_payments_oct=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_oct')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_oct = 0
        occupants_with_zero_or_negative_balance_oct = 0
        
        for occupant_bill_oct in occupant_bills_oct:
            total_payments_oct = 0
            for occupant_payment_oct in occupant_payments_oct:
                if occupant_payment_oct['id'] == occupant_bill_oct['id']:
                    total_payments_oct = occupant_payment_oct['total_payments_oct']
                    break
            remaining_balance_oct = occupant_bill_oct['total_bills_oct'] - total_payments_oct
            if remaining_balance_oct > 0:
                occupants_with_balance_oct += 1
            else:
                occupants_with_zero_or_negative_balance_oct += 1

        Oct_PatiallyPaid_Per = (occupants_with_balance_oct / Oct) * 100 if Oct != 0 else 0
        Oct_PatiallyPaid_Per = int(round(Oct_PatiallyPaid_Per))

        Oct_Paid_Per = (occupants_with_zero_or_negative_balance_oct / Oct) * 100 if Oct != 0 else 0
        Oct_Paid_Per = int(round(Oct_Paid_Per))


        # Partially Paid and Paid in November
        occupant_bills_nov = Occupant.objects.filter(bill_details__created_at__icontains="2023-11")\
            .annotate(total_bills_nov=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_nov')\
            .distinct().order_by('person__last_name')

        occupant_payments_nov = Occupant.objects.filter(payment__created_at__icontains="2023-11")\
            .annotate(total_payments_nov=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_nov')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_nov = 0
        occupants_with_zero_or_negative_balance_nov = 0

        for occupant_bill_nov in occupant_bills_nov:
            total_payments_nov = 0
            for occupant_payment_nov in occupant_payments_nov:
                if occupant_payment_nov['id'] == occupant_bill_nov['id']:
                    total_payments_nov = occupant_payment_nov['total_payments_nov']
                    break
            remaining_balance_nov = occupant_bill_nov['total_bills_nov'] - total_payments_nov
            if remaining_balance_nov > 0:
                occupants_with_balance_nov += 1
            else:
                occupants_with_zero_or_negative_balance_nov += 1

        Nov_PatiallyPaid_Per = (occupants_with_balance_nov / Nov) * 100 if Nov != 0 else 0
        Nov_PatiallyPaid_Per = int(round(Nov_PatiallyPaid_Per))

        Nov_Paid_Per = (occupants_with_zero_or_negative_balance_nov / Nov) * 100 if Nov != 0 else 0
        Nov_Paid_Per = int(round(Nov_Paid_Per))


        # Partially Paid and Paid in December
        occupant_bills_dec = Occupant.objects.filter(bill_details__created_at__icontains="2023-12")\
            .annotate(total_bills_dec=Sum('bill_details__amount'))\
            .values('id', 'person__last_name', 'total_bills_dec')\
            .distinct().order_by('person__last_name')

        occupant_payments_dec = Occupant.objects.filter(payment__created_at__icontains="2023-12")\
            .annotate(total_payments_dec=Sum('payment__amount'))\
            .values('id', 'person__last_name', 'total_payments_dec')\
            .distinct().order_by('person__last_name')

        occupants_with_balance_dec = 0
        occupants_with_zero_or_negative_balance_dec = 0
        
        for occupant_bill_dec in occupant_bills_dec:
            total_payments_dec = 0
            for occupant_payment_dec in occupant_payments_dec:
                if occupant_payment_dec['id'] == occupant_bill_dec['id']:
                    total_payments_dec = occupant_payment_dec['total_payments_dec']
                    break
            remaining_balance_dec = occupant_bill_dec['total_bills_dec'] - total_payments_dec
            if remaining_balance_dec > 0:
                occupants_with_balance_dec += 1
            else:
                occupants_with_zero_or_negative_balance_nov += 1

        Dec_PatiallyPaid_Per = (occupants_with_balance_dec / Dec) * 100 if Dec != 0 else 0
        Dec_PatiallyPaid_Per = int(round(Dec_PatiallyPaid_Per))

        Dec_Paid_Per = (occupants_with_zero_or_negative_balance_dec / Dec) * 100 if Dec != 0 else 0
        Dec_Paid_Per = int(round(Dec_Paid_Per))


        partiallypaid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        partiallypaid_monthly_occ_per = [Jan_PatiallyPaid_Per, Feb_PatiallyPaid_Per, Mar_PatiallyPaid_Per, Apr_PatiallyPaid_Per,
                                          May_PatiallyPaid_Per, Jun_PatiallyPaid_Per, Jul_PatiallyPaid_Per, Aug_PatiallyPaid_Per, 
                                          Sep_PatiallyPaid_Per, Oct_PatiallyPaid_Per, Nov_PatiallyPaid_Per, Dec_PatiallyPaid_Per]
        
        context['partiallypaid_monthly_occ_per_list'] = partiallypaid_monthly_occ_per_list
        context['partiallypaid_monthly_occ_per'] = partiallypaid_monthly_occ_per


        paid_monthly_occ_per_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        paid_monthly_occ_per = [Jan_Paid_Per, Feb_Paid_Per, Mar_Paid_Per, Apr_Paid_Per,
                                May_Paid_Per, Jun_Paid_Per, Jul_Paid_Per, Aug_Paid_Per, 
                                Sep_Paid_Per, Oct_Paid_Per, Nov_Paid_Per, Dec_Paid_Per]
        
        context['paid_monthly_occ_per_list'] = paid_monthly_occ_per_list
        context['paid_monthly_occ_per'] = paid_monthly_occ_per


        return context

# @method_decorator(login_required, name='dispatch')
class DMDashMaleVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'dormmanager/dm_dash_male_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(DMDashMaleVacantBed, self).get_queryset(*args, **kwargs)
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
class DMDashFemaleVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'dormmanager/dm_dash_female_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(DMDashFemaleVacantBed, self).get_queryset(*args, **kwargs)
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
class DMDashForeignVacantBed(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'dormmanager/dm_dash_foreign_vacant_bed.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(DMDashForeignVacantBed, self).get_queryset(*args, **kwargs)
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
class DMRegistrationList(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'dormmanager/dm_registration_list.html'
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
        qs = super(DMRegistrationList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-created_at").filter(Q(psu_email__icontains=query) | Q(last_name__icontains=query) | Q(first_name__icontains=query) 
            | Q(program__icontains=query) | Q(boarder_type__icontains=query)| Q(reg_status__iexact=query) | Q(gender__iexact=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class DMRegMonthRep(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'dormmanager/dm_reg_month_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = Person.objects.raw('SELECT * FROM dormitory_person WHERE MONTH(created_at) = MONTH(CURRENT_DATE()) AND YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')
        return context

# @method_decorator(login_required, name='dispatch')
class DMRegYearRep(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'dormmanager/dm_reg_year_rep.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = Person.objects.raw('SELECT * FROM dormitory_person WHERE YEAR(created_at) = YEAR(CURRENT_DATE()) ORDER BY created_at DESC')
        return context

# @method_decorator(login_required, name='dispatch')
class DMRegistrationRegView(UpdateView):
    model = Person
    fields = "__all__"
    context_object_name = 'person'
    template_name = 'dormmanager/dm_registration_view.html'
    success_url = "/dm_registration_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Registration details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class DMOccupantList(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'dormmanager/dm_occupant_list.html'
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
        qs = super(DMOccupantList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-created_at").filter(Q(person__last_name__icontains=query) | Q(person__first_name__icontains=query)
            | Q(bed__bed_code__icontains=query) | Q(person__boarder_type__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class DMOccupantView(UpdateView):
    model = Occupant
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'dormmanager/dm_occupant_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fetch_first_three'] = Bill_Details.objects.filter(occupant=self.object.id)[:3]
        context['billing_details'] = Bill_Details.objects.filter(occupant=self.object.id)[3:]
        context['total_bills_amount'] = Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['payment'] = Payment.objects.filter(occupant=self.object.id)
        context['total_payment_amount'] = Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0
        context['remaining_balance'] = (Bill_Details.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0)
        context['occupant_demerits'] = OccupantDemerit.objects.filter(occupant=self.object.id)

        cursor = connections['default'].cursor()
        query = f"UPDATE dormitory_occupantdemerit SET new_remarks = null "
        cursor.execute(query)

        return context

    def form_valid(self, form):
      messages.success(self.request, "Occupant details was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

# @method_decorator(login_required, name='dispatch')
class DMOccMonthRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'dormmanager/dm_occ_month_rep.html'
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
class DMOccYearRep(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'dormmanager/dm_occ_year_rep.html'
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
class DMBillingList(ListView):
    model = Bill_Details
    context_object_name = 'occupant'
    template_name = 'dormmanager/dm_billing_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bills'] = Bill_Details.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DMBillingList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(service__service_name__icontains=query)
            | Q(description__icontains=query) | Q(amount__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class DMPaymentList(ListView):
    model = Payment
    context_object_name = 'payment'
    template_name = 'dormmanager/dm_payment_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment'] = Payment.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DMPaymentList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(payment_date__icontains=query)
            | Q(amount__icontains=query) | Q(receipt_no__iexact=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class DMOccupantDemeritList(ListView):
    model = OccupantDemerit
    context_object_name = 'occupant'
    template_name = 'dormmanager/dm_occupant_demerit_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['occupant_demerit'] = OccupantDemerit.objects.count()
        cursor = connections['default'].cursor()
        query = f"UPDATE dormitory_occupantdemerit SET new_remarks = null "
        cursor.execute(query)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DMOccupantDemeritList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("occupant")
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(demerit_name__demerit_name__icontains=query)
            | Q(demerit_name__demerit_points__icontains=query) | Q(cur_date__icontains=query) | Q(prev_remarks__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class DMRoomList(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'dormmanager/dm_room_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(DMRoomList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(room_name__iexact=query) | Q(floorlvl__icontains=query) 
                | Q(dorm_name__icontains=query) | Q(description__icontains=query))
        
        # Annotate the queryset after the search filter has been applied
        qs = qs.annotate(
            TotalBeds=Count('bed'), 
            TotalVacant=Count('bed', filter=Q(bed__bed_status='Vacant'))
        ).order_by('created_at')
        
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
class DMRoomListCard(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'dormmanager/dm_room_list_card.html'
    paginate_by = 9

    def get_queryset(self, *args, **kwargs):
        qs = super(DMRoomListCard, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(room_name__iexact=query) | Q(floorlvl__icontains=query) 
                | Q(dorm_name__icontains=query) | Q(description__icontains=query))
        
        # Annotate the queryset after the search filter has been applied
        qs = qs.annotate(
            TotalBeds=Count('bed'), 
            TotalVacant=Count('bed', filter=Q(bed__bed_status='Vacant')),
            TotalOccupied=Count('bed', filter=Q(bed__bed_status='Occupied')),
            TotalUnder=Count('bed', filter=Q(bed__bed_status='Under Maint.')),
        ).order_by('created_at')
        
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
class DMBedList(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'dormmanager/dm_bed_list.html'
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
        qs = super(DMBedList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("room_id")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("room_id").filter(Q(room__dorm_name__iexact=query) | Q(room__room_name__icontains=query)
            | Q(bed_code__icontains=query) | Q(price__icontains=query) | Q(bed_status__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class DMServiceList(ListView):
    model = Service
    context_object_name = 'service'
    template_name = 'dormmanager/dm_service_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services']= Service.objects.all().exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others').count()
        context['available'] = Service.objects.filter(status__iexact="Available").exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others').count()
        context['notavailable'] = Service.objects.filter(status__iexact="Not Available").count()
        context['services_limit']= Service.objects.all().exclude(service_name__iexact='Local Deposit').exclude(service_name__iexact='Local Advance').exclude(service_name__iexact='Foreign Deposit').exclude(service_name__iexact='Foreign Advance').exclude(service_name__iexact='Dorm ID').exclude(service_name__iexact='Others')
    
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DMServiceList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("created_at")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("service_name").filter(Q(service_name__icontains=query) | Q(status__icontains=query)
            | Q(base_amount__icontains=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class DMDemeritList(ListView):
    model = Demerit
    context_object_name = 'demerit'
    template_name = 'dormmanager/dm_demerit_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demerit'] = Demerit.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DMDemeritList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("demerit_points")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("-demerit_points").filter(Q(demerit_name__icontains=query) 
            | Q(demerit_points__iexact=query))
        return qs


# @method_decorator(login_required, name='dispatch')
class DMOccupantAccounts(ListView):
    model = User
    context_object_name = 'users'
    template_name = "dormmanager/dm_users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = User.objects.count()
        context['active'] = User.objects.filter(user_status__iexact="active").count()
        context['inactive'] = User.objects.filter(user_status__iexact="inactive").count()

        # cursor = connections['default'].cursor()
        # query = "DELETE FROM dormitory_user WHERE person_id NOT IN (SELECT person_id FROM dormitory_person)"
        # cursor.execute(query)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DMOccupantAccounts, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("lastname")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("lastname").filter(Q(last_name__icontains=query) | Q(first_name__icontains=query) 
            | Q(username__icontains=query) | Q(user_status__iexact=query) | Q(recovery_email__icontains=query))
        return qs

# @method_decorator(login_required, name='dispatch')
class DMOccupantAccountsUpdateView(UpdateView):
    model = User
    fields = ['username','password','security_question',
              'security_answer','recovery_email','user_status']
    context_object_name = 'user'
    template_name = 'dormmanager/dm_users_update.html'
    success_url = "/dm_users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Occupant account was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class DMAdminProfile(ListView):
    model = Admin
    context_object_name = 'admin'
    template_name = "dormmanager/dm_admin_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global dm
        context ['acc'] = Admin.objects.filter(Q(username=dm)).values()
        return context

# @method_decorator(login_required, name='dispatch')
class DMAdminProfileUpdateView(UpdateView):
    model = Admin
    fields = ['firstname', 'lastname', 'username', 'password', 'security_question', 'security_answer', 'recovery_email']
    context_object_name = 'admin'
    template_name = 'dormamanger/dm_admin_profile_update.html'
    success_url = "/dm_admin_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      messages.success(self.request, "Your Account Information was updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())


# ===================================================
# End of Dormmanager
# ===================================================

# ===================================================
# Functions for adding
# ===================================================
def add_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            form.save()
            email = request.POST['psu_email']

            html_body = render_to_string("superadmin/reg_email.html")

            message = EmailMultiAlternatives(
                subject='Registration confirmation email',
                body="mail testing",
                from_email='settings.EMAIL_HOST_USER',
                to=[email]
            )
            message.attach_alternative(html_body, "text/html")
            message.send(fail_silently=False)

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
        return render(request, 'superadmin/registration_add.html',  {'form': form})

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

            html_body = render_to_string("superadmin/occ_email.html")

            message = EmailMultiAlternatives(
                subject='Official Occupant confirmation email',
                body="mail testing",
                from_email='settings.EMAIL_HOST_USER',
                to=[email]
            )
            message.attach_alternative(html_body, "text/html")
            message.send(fail_silently=False)

            person_id = request.POST.get("person")

            if boarder_type == "Local":
                cursor = connections['default'].cursor()
                query_deposit_local = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '1500', 1, now(), {occ_id}, '1', 'None')"
                cursor.execute(query_deposit_local)

                cursor = connections['default'].cursor()
                query_advance_local = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '1500', 2, now(), {occ_id}, '1', 'None')"
                cursor.execute(query_advance_local)

                cursor = connections['default'].cursor()
                query_dorm_id = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '150', 3, now(), {occ_id}, '1', 'None')"
                cursor.execute(query_dorm_id)

            elif boarder_type == "Foreign":
                cursor = connections['default'].cursor()
                query_deposit_foreign = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '4500', 4, now(), {occ_id}, '1', 'None')"
                cursor.execute(query_deposit_foreign)

                cursor = connections['default'].cursor()
                query_advance_foreign = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '4500', 5, now(), {occ_id}, '1', 'None')"
                cursor.execute(query_advance_foreign)

                cursor = connections['default'].cursor()
                query_dorm_id = f"INSERT INTO dormitory_bill_details VALUES ('', now(), now(), 'None', '150', 3, now(), {occ_id}, '1', 'None')"
                cursor.execute(query_dorm_id)

            return redirect('OccupantAdd')

        else:
            
            messages.error(request, 'Please complete the required field.')
            # print()
            return redirect('OccupantAdd')
    else:
        form = OccupantForm()
        return render(request, 'superadmin/occupant_add.html',  {'form': form})

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
        return render(request, 'superadmin/occupant_renew.html',  {'form': form})  

def add_billing(request):
    if request.method == "POST":
        form = BillingForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            form.save()

            service = form.cleaned_data['service']
            service_service_name = service.service_name 
            quantity = form.cleaned_data['quantity']
            price = Service.objects.filter(service_name=service_service_name).first()
            total_amount = price.base_amount * quantity
            bill_id = form.instance.id
            
            # print(f'service: {service}')
            # print(f'quantity: {quantity}')
            # print(f'price: {price}')
            # print(f'bill_id: {bill_id}')
            # print(f'total_amount: {total_amount}')
            
            cursor = connections['default'].cursor()
            query = "UPDATE dormitory_bill_details SET amount = %s WHERE id = %s"
            cursor.execute(query, (total_amount, bill_id))
            
            messages.success(request, 'New bill added successfully!')
            return redirect('BillingAdd')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('BillingAdd')
    else:
        form = BillingForm()
        return render(request, 'superadmin/billing_add.html',  {'form': form})

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
        return render(request, 'superadmin/others_billing_add.html',  {'form': form})

def other_add(request):
    return render(request, 'superadmin/billing_list/other_billing_add.html', {} )

def other_update_billing(request, billing_id):
    billing = Bill_Details.objects.get(pk=billing_id)
    form = OtherBillingForm(request.POST or None, instance=billing)
    if form.is_valid():
        form.save()
        messages.success(request, 'Billing details was updated successfully!')
        return redirect('OccupantView', pk=billing.occupant_id)
        # return redirect(request.META.get('HTTP_REFERER'))
    return render (request, 'superadmin/others_billing_update.html', {'billing': billing, 'form': form})

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
        return render(request, 'superadmin/payment_add.html',  {'form': form})

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
        return render(request, 'superadmin/occupant_demerit_add.html',  {'form': form})

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
        return render(request, 'superadmin/room_add.html',  {'form': form})

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
        return render(request, 'superadmin/bed_add.html',  {'form': form})

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
        return render(request, 'superadmin/service_add.html',  {'form': form})

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
        return render(request, 'superadmin/demerit_add.html',  {'form': form})

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
        return render(request, 'superadmin/admin_add.html',  {'form': form})


def fd_add_registration(request):
    if request.method == "POST":

        email = request.POST['psu_email']

        html_body = render_to_string("frontdesk/fd_reg_email.html")

        message = EmailMultiAlternatives(
            subject='Registered Successfully',
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
            return redirect('FDRegistrationAdd')

        else:
            messages.error(request, 'Please complete the required field/s.')
            # print()
            return redirect('FDRegistrationAdd')
    else:
        form = RegistrationForm()
        return render(request, 'frontdesk/fd_registration_add.html',  {'form': form})

def fd_add_occupant(request):
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

            html_body = render_to_string("frontdesk/fd_occ_email.html")

            message = EmailMultiAlternatives(
                subject='Official Occupant of PSU Dormitory',
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

            return redirect('FDOccupantAdd')

        else:
            
            messages.error(request, 'Please complete the required field.')
            # print()
            return redirect('FDOccupantAdd')
    else:
        form = OccupantForm()
        return render(request, 'frontdesk/fd_occupant_add.html',  {'form': form})

def fd_renew_occupant(request):
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

            return redirect('FDOccupantRenew')

        else:
            
            messages.error(request, 'Please complete the required field.')
            # print()
            return redirect('FDOccupantRenew')
    else:
        form = OccupantRenewForm()
        return render(request, 'frontdesk/fd_occupant_renew.html',  {'form': form})  

def fd_add_occupant_demerit(request):
    if request.method == "POST":
        form = OccupantDemeritForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New demerit for occupant added successfully!')
            return redirect('FDOccupantDemeritAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('FDOccupantDemeritAdd')
    else:
        form = OccupantDemeritForm()
        return render(request, 'frontdesk/fd_occupant_demerit_add.html',  {'form': form})

def fd_add_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New room added successfully!')
            return redirect('FDRoomAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('FDRoomAdd')
    else:
        form = RoomForm()
        return render(request, 'frontdesk/fd_room_add.html',  {'form': form})

def fd_add_bed(request):
    if request.method == "POST":
        form = BedForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New bed added successfully!')
            return redirect('FDBedAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('FDBedAdd')
    else:
        form = BedForm()
        return render(request, 'frontdesk/fd_bed_add.html',  {'form': form})

def fd_add_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New service added successfully!')
            return redirect('FDServiceAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('FDServiceAdd')
    else:
        form = ServiceForm()
        return render(request, 'frontdesk/fd_service_add.html',  {'form': form})

def fd_add_demerit(request):
    if request.method == "POST":
        form = DemeritForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New demerit added successfully!')
            return redirect('FDDemeritAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('FDDemeritAdd')
    else:
        form = DemeritForm()
        return render(request, 'frontdesk/fd_demerit_add.html',  {'form': form})


def as_add_billing(request):
    if request.method == "POST":
        form = BillingForm(request.POST)
        if form.is_valid():
            form.save()

            service = form.cleaned_data['service']
            service_service_name = service.service_name 
            quantity = form.cleaned_data['quantity']
            price = Service.objects.filter(service_name=service_service_name).first()
            total_amount = price.base_amount * quantity
            bill_id = form.instance.id
            
            cursor = connections['default'].cursor()
            query = "UPDATE dormitory_bill_details SET amount = %s WHERE id = %s"
            cursor.execute(query, (total_amount, bill_id))
            
            messages.success(request, 'New bill added successfully!')
            return redirect('ASBillingAdd')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('ASBillingAdd')
    else:
        form = BillingForm()
        return render(request, 'accountingstaff/as_billing_add.html',  {'form': form})

def as_other_add_billing(request):
    if request.method == "POST":
        form = OtherBillingForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'New bill added successfully!')
            return redirect('as_other-add')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('as_other-add')
    else:
        form = OtherBillingForm()
        return render(request, 'accountingstaff/as_others_billing_add.html',  {'form': form})

def as_other_add(request):
    return render(request, 'accountingstaff/as_billing_list/other_billing_add.html', {} )

def as_add_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New payment added successfully!')
            return redirect('ASPaymentAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('ASPaymentAdd')
    else:
        form = PaymentForm()
        return render(request, 'accountingstaff/as_payment_add.html',  {'form': form})

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
        return render(request, 'user/user_login.html',  {'form': form})
        
def user_logout_view(request):
    logout(request)
    return redirect("user_login")


# @method_decorator(login_required, name='dispatch')
class User_Dashboard(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = "user/user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['per'] = Person.objects.filter(Q(psu_email=x)).values().order_by('-id')[:1]
        context ['occ'] = Occupant.objects.filter(Q(person__psu_email=x)).values('bed__bed_description', 'bed__price', 'person__boarder_type', 'bed__bed_code', 'bed__room__room_name', 'bed__room__dorm_name').order_by('-id')[:1]
        return context

# @method_decorator(login_required, name='dispatch')
class User_Account(ListView):
    model = User
    context_object_name = 'user'
    template_name = "user/user_account.html"

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
    template_name = 'user/user_account_update.html'
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
    template_name = "user/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global x
        context ['prof'] = Person.objects.filter(Q(psu_email=x)).values()
        return context

# @method_decorator(login_required, name='dispatch')
class User_Billing(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = "user/user_billing.html"

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
    template_name = 'user/user_contract_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global x
        
        # context ['contract'] = Occupant.objects.filter(Q(person__psu_email=x, id=self.object.id)).values('id','bed__bed_code', 'person__boarder_type', 'bed__bed_description', 'bedPrice', 'bed__room__room_name', 'bed__room__floorlvl', 'bed__room__dorm_name', 'start_date', 'end_date').order_by('-created_at')
        context['fetch_first_three'] = Bill_Details.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).values('bill_date', 'service__service_name', 'amount')[0:3]
        context['billing_details'] = Bill_Details.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).values('bill_date', 'service__service_name', 'service__title', 'service__description', 'quantity', 'amount')[3:]
        context['total_bills_amount'] = Bill_Details.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).aggregate(Sum('amount'))['amount__sum'] or 0
        context['payment'] = Payment.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).values('payment_date', 'amount', 'receipt_no')
        context['total_payment_amount'] = Payment.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).aggregate(Sum('amount'))['amount__sum'] or 0
        context['remaining_balance'] = (Bill_Details.objects.filter(Q(occupant__person__psu_email=x, occupant=self.object.id)).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=self.object.id).aggregate(Sum('amount'))['amount__sum'] or 0)
        return context

# @method_decorator(login_required, name='dispatch')
class User_Services(ListView):
    model = Service
    context_object_name = 'services'
    template_name = "user/user_services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global x
        
        # Get the current day
        current_day = datetime.datetime.now()
        final_y_m = current_day.strftime("%Y") + "-" + current_day.strftime("%m")

        # Filter the Bill_Details queryset for the current month
        bill_details_current_month = Bill_Details.objects.filter(
            Q(occupant__person__psu_email=x), created_at__icontains=final_y_m
        )[3:]

        total_bills_current_month = (Bill_Details.objects.filter(Q(occupant__person__psu_email=x), created_at__icontains=final_y_m).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(Q(occupant__person__psu_email=x), created_at__icontains=final_y_m).aggregate(Sum('amount'))['amount__sum'] or 0)

        # Add the count to the context
        context['total_availed_service'] = bill_details_current_month.count()
        context['total_bills_current_month'] = total_bills_current_month
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
            service_service_name = service.service_name 
            quantity = form.cleaned_data['quantity']
            price = Service.objects.filter(service_name=service_service_name).first()
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
        return render(request, 'user/user_service_avail.html',  {'form': form})

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
        return render(request, 'user/user_service_others.html',  {'form': form})

def user_other_add(request):
    return render(request, 'user/user_services/user_service_others.html', {} )

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
        return render(request, 'user/user_forgot_password.html',  {'form': form})

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
        return render(request, 'user/user_security_question.html',  {'form': form, 'security_question': security_question})

def user_show_password_form(request):
    global y

    # Retrieve the Occupant object for the given email address
    occ = User.objects.get(username=y)
    # Retrieve the password for the Occupant object
    password = occ.password
    return render(request, 'user/user_show_password.html', {'password': password})

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
                return redirect('fd_home')

            elif(test2 != 0):
                global ac
                ac = request.session['username'] = UN
                return redirect('as_home')

            elif(test3 != 0):
                global dm
                dm = request.session['username'] = UN
                return redirect('dm_home')

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

# def delete_reg(request, id):
#   room = Person.objects.get(id=id)
#   room.delete()
#   return HttpResponseRedirect(reverse('RegistrationList'))

# def delete_occupant(request, id):
#   occupant = Occupant.objects.get(id=id)
#   occupant.delete()
#   return HttpResponseRedirect(reverse('OccupantList'))

# def delete_room(request, id):
#   room = Room.objects.get(id=id)
#   room.delete()
#   return HttpResponseRedirect(reverse('RoomList'))

# def delete_bed(request, id):
#   bed = Bed.objects.get(id=id)
#   bed.delete()
#   return HttpResponseRedirect(reverse('BedList'))

# def delete_demerit(request, id):
#   demerit = Demerit.objects.get(id=id)
#   demerit.delete()
#   return HttpResponseRedirect(reverse('DemeritList'))

# def delete_user(request, id):
#   occupant = User.objects.get(id=id)
#   occupant.delete()
#   return HttpResponseRedirect(reverse('OccupantAccounts'))

# def delete_bill(request, id):
#   occupant = Bill_Details.objects.get(id=id)
#   occupant.delete()
#   return HttpResponseRedirect(reverse('BillingList'))

# def delete_payment(request, id):
#   occupant = Payment.objects.get(id=id)
#   occupant.delete()
#   return HttpResponseRedirect(reverse('PaymentList'))

# def delete_service(request, id):
#   occupant = Service.objects.get(id=id)
#   occupant.delete()
#   return HttpResponseRedirect(reverse('ServiceList'))

# ===================================================
# Functions for Exporting to PDF and EXCEL
# ===================================================
from django.template.loader import get_template
from xhtml2pdf import pisa

def RegPDF(request, pk):
    reg_person = Person.objects.get(id=pk)
    reg_lastname = Person.objects.filter(id=pk).values_list('last_name', flat=True).first()
    reg_firstname = Person.objects.filter(id=pk).values_list('first_name', flat=True).first()
    reg_middlename = Person.objects.filter(id=pk).values_list('middle_name', flat=True).first()
    reg_middleinitial = reg_middlename[0].upper() + '.' if reg_middlename else ''
    template_path = 'superadmin/reg_pdf.html'

    context = {
        'reg_person': reg_person,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{reg_lastname}, {reg_firstname} {reg_middleinitial} - Registration Details.pdf"'
    
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
    occ_lastname = Occupant.objects.filter(id=pk).values_list('person__last_name', flat=True).first()
    occ_firstname = Occupant.objects.filter(id=pk).values_list('person__first_name', flat=True).first()
    occ_middlename = Occupant.objects.filter(id=pk).values_list('person__middle_name', flat=True).first()
    occ_middleinitial = occ_middlename[0].upper() + '.' if occ_middlename else ''
    table1 = Bill_Details.objects.filter(occupant=pk)[0:3]
    table2 = Bill_Details.objects.filter(occupant=pk)[3:]
    table3 = Payment.objects.filter(occupant=pk)
    total_bills_amount = Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    payment = Payment.objects.filter(occupant=pk)
    total_payment_amount = Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_balance = (Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0)
    table4 = OccupantDemerit.objects.filter(occupant=pk)
    template_path = 'superadmin/occ_pdf.html'

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
    response['Content-Disposition'] = f'filename="{occ_lastname}, {occ_firstname} {occ_middleinitial} - Statement of Account.pdf"'
    
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

def FDRegPDF(request, pk):
    reg_person = Person.objects.get(id=pk)
    reg_lastname = Person.objects.filter(id=pk).values_list('last_name', flat=True).first()
    reg_firstname = Person.objects.filter(id=pk).values_list('first_name', flat=True).first()
    reg_middlename = Person.objects.filter(id=pk).values_list('middle_name', flat=True).first()
    reg_middleinitial = reg_middlename[0].upper() + '.' if reg_middlename else ''
    template_path = 'frontdesk/fd_reg_pdf.html'
    context = {
        'reg_person': reg_person,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{reg_lastname}, {reg_firstname} {reg_middleinitial} - Registration Details.pdf"'
    
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

def FDOccPDF(request, pk):
    occ_person = Occupant.objects.get(id=pk)
    occ_lastname = Occupant.objects.filter(id=pk).values_list('person__last_name', flat=True).first()
    occ_firstname = Occupant.objects.filter(id=pk).values_list('person__first_name', flat=True).first()
    occ_middlename = Occupant.objects.filter(id=pk).values_list('person__middle_name', flat=True).first()
    occ_middleinitial = occ_middlename[0].upper() + '.' if occ_middlename else ''
    table1 = Bill_Details.objects.filter(occupant=pk)[0:3]
    table2 = Bill_Details.objects.filter(occupant=pk)[3:]
    table3 = Payment.objects.filter(occupant=pk)
    total_bills_amount = Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    payment = Payment.objects.filter(occupant=pk)
    total_payment_amount = Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_balance = (Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0)
    table4 = OccupantDemerit.objects.filter(occupant=pk)
    template_path = 'frontdesk/fd_occ_pdf.html'

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
    response['Content-Disposition'] = f'filename="{occ_lastname}, {occ_firstname} {occ_middleinitial} - Statement of Account.pdf"'
    
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

def ASOccPDF(request, pk):
    occ_person = Occupant.objects.get(id=pk)
    occ_lastname = Occupant.objects.filter(id=pk).values_list('person__last_name', flat=True).first()
    occ_firstname = Occupant.objects.filter(id=pk).values_list('person__first_name', flat=True).first()
    occ_middlename = Occupant.objects.filter(id=pk).values_list('person__middle_name', flat=True).first()
    occ_middleinitial = occ_middlename[0].upper() + '.' if occ_middlename else ''
    table1 = Bill_Details.objects.filter(occupant=pk)[0:3]
    table2 = Bill_Details.objects.filter(occupant=pk)[3:]
    table3 = Payment.objects.filter(occupant=pk)
    total_bills_amount = Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    payment = Payment.objects.filter(occupant=pk)
    total_payment_amount = Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_balance = (Bill_Details.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0) - (Payment.objects.filter(occupant=pk).aggregate(Sum('amount'))['amount__sum'] or 0)
    table4 = OccupantDemerit.objects.filter(occupant=pk)
    template_path = 'accountingstaff/as_occ_pdf.html'

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
    response['Content-Disposition'] = f'filename="{occ_lastname}, {occ_firstname} {occ_middleinitial} - Statement of Account.pdf"'
    
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

def fd_reg_all_csv(request):
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

def fd_reg_month_csv(request):
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

def fd_reg_year_csv(request):
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

def fd_occ_all_csv(request):
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

def fd_occ_month_csv(request):
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

def fd_occ_year_csv(request):
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

def as_occ_all_csv(request):
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

def as_occ_month_csv(request):
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

def as_occ_year_csv(request):
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
    num_days_before_due_date = 7

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

    return render(request, 'superadmin/notification_list.html', {'messages': messages})

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

    return render(request, 'user/user_notifications.html', {'messages': messages})

def FDAdminNotifications(request):

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

    return render(request, 'frontdesk/fd_notification_list.html', {'messages': messages})

def ASAdminNotifications(request):

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

    return render(request, 'accountingstaff/as_notification_list.html', {'messages': messages})

def DMAdminNotifications(request):

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

    return render(request, 'dormmanager/dm_notification_list.html', {'messages': messages})

def UserRules(request):
    return render(request, 'user/user_rules.html')
# ===================================================
# start of Due Date Email Notifications
# ===================================================
# Get the current date and time
now = datetime.datetime.now()
from django.core.mail import EmailMultiAlternatives

# Calculate the date that is 1 week before the 30th of the month
if now.month == 2:  # February
    if now.day >= 23:
        occ_date = datetime.date(now.year, 3, 1) - datetime.timedelta(days=9)
    else:
        occ_date = datetime.date(now.year, 2, 30) - datetime.timedelta(days=7)
else:
    if now.day >= 25:
        next_month = now.replace(day=28) + datetime.timedelta(days=4)
        occ_date = next_month.replace(day=30) - datetime.timedelta(days=10)
    else:
        occ_date = now.replace(day=30) - datetime.timedelta(days=7)

# Check if the current date is equal to or after the calculated date
if now >= occ_date:
    # Get all the occupants
    occupants = Occupant.objects.all()

    # Determine which email template to use based on the date
    if now >= occ_date - datetime.timedelta(days=4):
        template_name = "due_1week_email.html"
        subject = "Due in 1 week"

    if now >= occ_date - datetime.timedelta(days=4):
        template_name = "due_3days_email.html"
        subject = "Due in 3 days"

    if now >= occ_date - datetime.timedelta(days=4):
        template_name = "due_1day_email.html"
        subject = "Due tomorrow"

    # Loop through the occupants and send an email to each one
    for occupant in occupants:
        # Get the PSU email address of the occupant
        email = occupant.person.psu_email.strip()

        # Skip any invalid email addresses
        if not email:
            continue

        # Render the HTML email template with occupant-specific data
        html_body = render_to_string(template_name, {'occupant': occupant})

        # Create and send the email to the occupant
        message = EmailMultiAlternatives(
            subject=subject,
            body="mail testing",
            from_email='settings.EMAIL_HOST_USER',
            to=[email]
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)

# Check if the current date is the 25th of the month
# if now.day == 25:
#     # Get all the occupants
#     occupants = Occupant.objects.all()

#     # Determine which email template to use based on the date
#     template_name = "due_1week_email.html"
#     subject = "Due in 1 week"

#     # Loop through the occupants and send an email to each one
#     for occupant in occupants:
#         # Get the PSU email address of the occupant
#         email = occupant.person.psu_email.strip()

#         # Skip any invalid email addresses
#         if not email:
#             continue

#         # Render the HTML email template with occupant-specific data
#         html_body = render_to_string(template_name, {'occupant': occupant})

#         # Create and send the email to the occupant
#         message = EmailMultiAlternatives(
#             subject=subject,
#             body="mail testing",
#             from_email='settings.EMAIL_HOST_USER',
#             to=[email]
#         )
#         message.attach_alternative(html_body, "text/html")
#         message.send(fail_silently=False)

# if now.day == 25:
#     # Get all the occupants
#     occupants = Occupant.objects.all()

#     # Determine which email template to use based on the date
#     template_name = "due_3days_email.html"
#     subject = "Due in 3 days"

#     # Loop through the occupants and send an email to each one
#     for occupant in occupants:
#         # Get the PSU email address of the occupant
#         email = occupant.person.psu_email.strip()

#         # Skip any invalid email addresses
#         if not email:
#             continue

#         # Render the HTML email template with occupant-specific data
#         html_body = render_to_string(template_name, {'occupant': occupant})

#         # Create and send the email to the occupant
#         message = EmailMultiAlternatives(
#             subject=subject,
#             body="mail testing",
#             from_email='settings.EMAIL_HOST_USER',
#             to=[email]
#         )
#         message.attach_alternative(html_body, "text/html")
#         message.send(fail_silently=False)

# if now.day == 25:
#     # Get all the occupants
#     occupants = Occupant.objects.all()

#     # Determine which email template to use based on the date
#     template_name = "due_1day_email.html"
#     subject = "Due in Tomorrow"

#     # Loop through the occupants and send an email to each one
#     for occupant in occupants:
#         # Get the PSU email address of the occupant
#         email = occupant.person.psu_email.strip()

#         # Skip any invalid email addresses
#         if not email:
#             continue

#         # Render the HTML email template with occupant-specific data
#         html_body = render_to_string(template_name, {'occupant': occupant})

#         # Create and send the email to the occupant
#         message = EmailMultiAlternatives(
#             subject=subject,
#             body="mail testing",
#             from_email='settings.EMAIL_HOST_USER',
#             to=[email]
#         )
#         message.attach_alternative(html_body, "text/html")
#         message.send(fail_silently=False)

# ===================================================
# end of Due Date Email Notifications
# ===================================================

# ===================================================
# start of End Date Email Notifications
# ===================================================
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
        # Render the email template
        html_body = render_to_string("end_1week_email.html", {'occupant': occupant})

        # Create the email message
        message = EmailMultiAlternatives(
            subject='End of contract in 1 week',
            body="mail testing",
            from_email='settings.EMAIL_HOST_USER',
            to=[occupant.person.psu_email]
        )
        message.attach_alternative(html_body, "text/html")

        # Send the email
        message.send(fail_silently=False)

    elif days_until_due_date == 3:
        # Render the email template
        html_body = render_to_string("end_3days_email.html", {'occupant': occupant})

        # Create the email message
        message = EmailMultiAlternatives(
            subject='End contract in 3 days',
            body="mail testing",
            from_email='settings.EMAIL_HOST_USER',
            to=[occupant.person.psu_email]
        )
        message.attach_alternative(html_body, "text/html")

        # Send the email
        message.send(fail_silently=False)

    elif days_until_due_date == 1:
        # Render the email template
        html_body = render_to_string("end_1day_email.html", {'occupant': occupant})

        # Create the email message
        message = EmailMultiAlternatives(
            subject='End of contract tomorrow',
            body="mail testing",
            from_email='settings.EMAIL_HOST_USER',
            to=[occupant.person.psu_email]
        )
        message.attach_alternative(html_body, "text/html")

        # Send the email
        message.send(fail_silently=False)

# ===================================================
# end of End Date Email Notifications
# ===================================================