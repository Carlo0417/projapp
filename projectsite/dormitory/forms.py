from django.forms import ModelForm

from .models import Room, Bed, Service, Occupant

from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"

class BedForm(ModelForm):
    class Meta:
        model = Bed
        fields = ['room','bed_no','price']

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

class OccupantForm(ModelForm):
    class Meta:
        model = Occupant
        fields = ['person','bed','start_date','end_date']

        

