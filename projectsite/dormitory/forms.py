from django.forms import ModelForm

from .models import Room, Bed, Service, Occupant, Person

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

class RegistrationForm(forms.ModelForm):
    Field1 = forms.BooleanField()
    Field2 = forms.BooleanField()
    Field3 = forms.BooleanField()
    Field4 = forms.BooleanField()
    Field5 = forms.BooleanField()
    Field6 = forms.BooleanField()
    Field7 = forms.BooleanField()

    class Meta:
        model = Person
        fields = "__all__"

        

