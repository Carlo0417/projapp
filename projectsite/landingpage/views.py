from django.shortcuts import render, redirect

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from dormitory.models import Room, Bed, Service, Occupant, Person
from django import forms
from dormitory.forms import RoomForm, ServiceForm, BedForm, OccupantForm, RegistrationForm
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
        context['occupied_bed'] = Bed.objects.filter(bed_status__icontains='occupied').count()
        
        return context


class RoomList(ListView):
    model = Room
    context_object_name = 'room'
    template_name = 'room_list.html'
    paginated_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(RoomList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("room_name")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("room_name").filter(Q(room_name__icontains=query))
        return qs

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
    paginated_by = 10

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
    paginated_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BedList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("room_id")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("room_id").filter(Q(room_id__icontains=query))
        return qs

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
    paginated_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(OccupantList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("person")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("person").filter(Q(person__icontains=query))
        return qs

class OccupantUpdateView(UpdateView):
    model = Occupant
    fields = "__all__"
    context_object_name = 'occupant'
    template_name = 'occupant_update.html'
    success_url = "/occupant_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RegistrationList(ListView):
    model = Person
    context_object_name = 'person'
    template_name = 'registration_list.html'
    paginated_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(RegistrationList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("psu_email")
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.order_by("psu_email").filter(Q(psu_email__icontains=query))
        return qs

class RegistrationUpdateView(UpdateView):
    model = Person
    fields = "__all__"
    context_object_name = 'person'
    template_name = 'registration_update.html'
    success_url = "/registration_list"

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
            messages.success(request, 'New Room Added Successfully.')
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
            messages.success(request, 'New Service Added Successfully.')
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
            messages.success(request, 'New Bed Added Successfully.')
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
        bed_id = request.POST.get("bed")
        print(request.POST)
        if form.is_valid():
            occ = form.save(commit=False)
            occ.pk = None
            occ.bedPrice = Bed.objects.filter(pk=bed_id).values_list('price')
            occ.save()

            messages.success(request, 'Occupant Added Successfully.')

            # update BED: bed_status to occupied after adding occupant
            cursor = connections['default'].cursor()
            query = f"UPDATE dormitory_bed SET bed_status = 'Occupied' WHERE `id` = {bed_id}"
            cursor.execute(query)
            return redirect('OccupantAdd')

        else:
            messages.error(request, 'Please complete the required field.')
            return redirect('OccupantAdd')
    else:
        form = OccupantForm()
        return render(request, 'occupant_add.html',  {'form': form})


def add_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Registered Successfully.')
            return redirect('RegistrationAdd')

        else:
            messages.error(request, 'Please complete the required field/s.')
            return redirect('RegistrationAdd')
    else:
        form = RegistrationForm()
        return render(request, 'registration_add.html',  {'form': form})

