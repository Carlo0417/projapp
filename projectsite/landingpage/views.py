from django.shortcuts import render, redirect

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from dormitory.models import Room, Service
from django import forms
from dormitory.forms import RoomForm, ServiceForm
from django.contrib import messages
from django.db.models import Q

class HomePageView(ListView):
    model = Room
    context_object_name = 'room'
    template_name = "landingpage/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


# ===================================================
# Functions for adding
# ===================================================
def add_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful.')
            return redirect('RoomAdd')

        else:
            messages.error(request, 'Please complete required field.')
            return redirect('RoomAdd')
    else:
        form = RoomForm()
        return render(request, 'room_add.html',  {'form': form})


def add_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful.')
            return redirect('ServiceAdd')

        else:
            messages.error(request, 'Please complete required field.')
            return redirect('ServiceAdd')
    else:
        form = ServiceForm()
        return render(request, 'service_add.html',  {'form': form})


