from atexit import register
from typing import List
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from dormitory.models import Room, Bed, Service, Occupant, Person, Bill_Details
from django import forms
from dormitory.forms import RoomForm, ServiceForm, BedForm, OccupantForm, RegistrationForm, BillingForm, OccupantFormEdit, BillingFormEdit
from django.contrib import messages
from django.db.models import Q

from django.db import connections

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


class RoomUpdateView(UpdateView):
    model = Room
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'room_update.html'
    success_url = "/room_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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

class ServiceUpdateView(UpdateView):
    model = Service
    fields = "__all__"
    context_object_name = 'room'
    template_name = 'service_update.html'
    success_url = "/service_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BedList(ListView):
    model = Bed
    context_object_name = 'bed'
    template_name = 'bed_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BedList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("room_id")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("room_id").filter(Q(room__dorm_name__icontains=query) | Q(room__room_name__icontains=query)
            | Q(bed_code__icontains=query) | Q(price__icontains=query) | Q(bed_status__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beds'] = Bed.objects.count()
        context['vacant'] = Bed.objects.filter(bed_status__icontains='vacant').count()
        context['occupied'] = Bed.objects.filter(bed_status__icontains='occupied').count()
        return context
        

class BedUpdateView(UpdateView):
    model = Bed
    fields = "__all__"
    context_object_name = 'bed'
    template_name = 'bed_update.html'
    success_url = "/bed_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OccupantList(ListView):
    model = Occupant
    context_object_name = 'occupant'
    template_name = 'occupant_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(OccupantList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("person")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("person").filter(Q(person__last_name__icontains=query) | Q(person__first_name__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['occupants'] = Occupant.objects.count()
        return context


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
        query = f"UPDATE dormitory_bed SET bed_status = 'Occupied' WHERE `id` = {self.object.bed_id}"
        cursor.execute(query)
        return "/occupant_list"


class RegistrationList(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'registration_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(RegistrationList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("psu_email")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("psu_email").filter(Q(psu_email__icontains=query) | Q(last_name__icontains=query) 
            | Q(first_name__icontains=query) | Q(program__icontains=query) | Q(boarder_type__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registered'] = Person.objects.count()
        context['complete'] = Person.objects.filter(Field1__icontains=1, Field2__icontains=1, 
        Field3__icontains=1, Field4__icontains=1, Field5__icontains=1, Field6__icontains=1,
        Field7__icontains=1).count()
        context['incomplete'] =  Person.objects.filter(psu_email__isnull=False).count() - Person.objects.filter(Field1__icontains=1, Field2__icontains=1, 
        Field3__icontains=1, Field4__icontains=1, Field5__icontains=1, Field6__icontains=1,
        Field7__icontains=1).count()
        return context

class RegistrationUpdateView(UpdateView):
    model = Person
    fields = "__all__"
    context_object_name = 'person'
    template_name = 'registration_update.html'
    success_url = "/registration_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BillingList(ListView):
    model = Bill_Details
    context_object_name = 'occupant'
    template_name = 'billing_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BillingList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("occupant")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("occupant").filter(Q(occupant__person__last_name__icontains=query) 
            | Q(occupant__person__first_name__icontains=query) | Q(service__service_name__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bills'] = Bill_Details.objects.count()
        return context

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
            query = f"UPDATE dormitory_bed SET bed_status = 'Occupied' WHERE `id` = {bed_id}"
            cursor.execute(query)
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

# def delete_reg(request, id):
#   room = Person.objects.get(id=id)
#   room.delete()
#   return HttpResponseRedirect(reverse('RegistrationList'))

