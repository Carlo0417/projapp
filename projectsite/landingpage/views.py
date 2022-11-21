from atexit import register
from typing import List

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
# from material import Field

from dormitory.models import Room, Bed, Service, Occupant, Person, Bill_Details, Payment
from django import forms
from dormitory.forms import RoomForm, ServiceForm, BedForm, OccupantForm, RegistrationForm, BillingForm, OccupantFormEdit, BillingFormEdit, PaymentForm
from django.contrib import messages
from django.db.models import Q

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
        context['complete'] = Person.objects.filter(Field1__icontains=1, Field2__icontains=1, 
        Field3__icontains=1, Field4__icontains=1, Field5__icontains=1, Field6__icontains=1,
        Field7__icontains=1).count()
        context['incomplete'] =  Person.objects.filter(psu_email__isnull=False).count() - Person.objects.filter(Field1__icontains=1, Field2__icontains=1, 
        Field3__icontains=1, Field4__icontains=1, Field5__icontains=1, Field6__icontains=1,
        Field7__icontains=1).count()
        context['local'] = Occupant.objects.filter(person_id__boarder_type__icontains='Local').count()
        context['foreign'] = Occupant.objects.filter(person_id__boarder_type__icontains='Foreign').count()
        context['maledorm_bed'] = Bed.objects.filter(bed_status__icontains='vacant', 
        room_id__dorm_name__icontains="Male Dorm").exclude(room_id__dorm_name__icontains="Female Dorm").count()
        context['femaledorm_bed'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__icontains="Female Dorm").count()
        context['foreigndorm_bed'] = Bed.objects.filter(bed_status__icontains='vacant', room_id__dorm_name__icontains="Foreign Dorm").count()
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
        context['maledorm'] = Room.objects.filter(dorm_name__icontains="Male Dorm").exclude(dorm_name__icontains="Female Dorm").count()
        context['femaledorm'] = Room.objects.filter(dorm_name__icontains="Female Dorm").count()
        context['foreigndorm'] = Room.objects.filter(dorm_name__icontains="Foreign Dorm").count()
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
        context['services'] = Service.objects.count()
        context['available'] = Service.objects.filter(status__icontains="Available").exclude(status__icontains="Not Available").count()
        context['notavailable'] = Service.objects.filter(status__icontains="Not Available").count()
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
        context['occupants'] = Occupant.objects.count()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(OccupantList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("person")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("person").filter(Q(person__last_name__icontains=query) | Q(person__first_name__icontains=query))
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
        context['billing_details'] = Bill_Details.objects.filter(occupant=1)
      
        # cursor = connections['default'].cursor()
        # query = f"SELECT dormitory_bill_details.bill_date, dormitory_bill_details.description, dormitory_bill_details.service_id, dormitory_bill_details.quantity, dormitory_bill_details.amount FROM dormitory_bill_details INNER JOIN dormitory_occupant ON dormitory_bill_details.occupant_id=dormitory_occupant.id WHERE dormitory_occupant.id = {self.object.id}"
        # cursor.execute(query)

        # context['billing'] = Bill_Details.objects.raw('SELECT dormitory_bill_details.bill_date, dormitory_bill_details.description, dormitory_bill_details.service_id, dormitory_bill_details.quantity, dormitory_bill_details.amount FROM dormitory_bill_details INNER JOIN dormitory_occupant ON dormitory_bill_details.occupant_id=dormitory_occupant.id WHERE dormitory_occupant.id=dormitory_occupant.id')

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
        context['complete'] = Person.objects.filter(Field1__icontains=1, Field2__icontains=1, 
        Field3__icontains=1, Field4__icontains=1, Field5__icontains=1, Field6__icontains=1,
        Field7__icontains=1).count()
        context['incomplete'] =  Person.objects.filter(psu_email__isnull=False).count() - Person.objects.filter(Field1__icontains=1, Field2__icontains=1, 
        Field3__icontains=1, Field4__icontains=1, Field5__icontains=1, Field6__icontains=1,
        Field7__icontains=1).count()

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
            | Q(program__icontains=query) | Q(boarder_type__icontains=query)| Q(reg_status__icontains=query))
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
            | Q(occupant__person__first_name__icontains=query) | Q(service__service_name__icontains=query))
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
            | Q(amount__icontains=query) | Q(receipt_no__icontains=query))
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
            occ_id = request.POST.get("occupant")
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

            # adding Bills to occupant
            # cursor = connections['default'].cursor()
            # id, created_at, updated_at, description, amount, service_id, bill_date, occupant_id, status, quantity
            # query2 = f"INSERT INTO dormitory_bill_details (now(), now(), description, amount, service_id, bill_date, occupant_id, status, quantity) VALUES ('None', '1500', (SELECT id FROM dormitory_service WHERE service_name = 'Deposit'), now(), {occ_id}, 'None', '0')"
            # cursor.execute(query2)

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
            messages.success(request, 'New inqury registered successfully!')
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


# ===================================================
# Functions for deleting
# ===================================================
# def delete_occupant(request, id):
#   occupant = Occupant.objects.get(id=id)
#   occupant.delete()
#   return HttpResponseRedirect(reverse('OccupantList'))

# def delete_bed(request, id):
#   bed = Bed.objects.get(id=id)
#   bed.delete()
#   return HttpResponseRedirect(reverse('BedList'))

# def delete_reg(request, id):
#   room = Person.objects.get(id=id)
#   room.delete()
#   return HttpResponseRedirect(reverse('RegistrationList'))