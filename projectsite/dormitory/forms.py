from django.forms import ModelForm

from .models import Room, Bed, Service

from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"

class BedForm(ModelForm):
    class Meta:
        model = Bed
        fields = ['room_id','bed_no','price']

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

        

