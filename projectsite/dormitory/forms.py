from django.forms import ModelForm

from .models import Room, Bed, Service, Occupant, Person, Bill_Details
from django.utils.translation import gettext_lazy as _

from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"

class BedForm(ModelForm):
    class Meta:
        model = Bed
        fields = ['room','bed_code','price']

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

class OccupantForm(ModelForm):
    class Meta:
        model = Occupant
        fields = ['person','bed','start_date','end_date']
    
    def __init__(self, user=None, **kwargs):
        super(OccupantForm, self).__init__(**kwargs)
        self.fields['bed'].queryset = Bed.objects.filter(bed_status__icontains='vacant')

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        labels = {
            'Field1' : _('Two pieces 2"x2" coloured ID pictures taken not more than six months prior to the signing of the contract'),
            'Field2' : _('Medical Certificate from the University physician'),
            'Field3' : _('Fully accomplished application form (form OIA-OID)'),
            'Field4' : _('Special power of attorney (SPA) for guardian'),
            'Field5' : _('Photocopy of the University Identification card valid on the school year enrolled'),
            'Field6' : _('Certificate of Enrollment'),
            'Field7' : _('Photocopy of the dormitory ID'),
        }
        # widgets = {
        #     'Field1' : forms.CheckboxInput(attrs={'class': 'required checkbox form-control'}),   
        # }

class BillingForm(ModelForm):
    class Meta:
        model = Bill_Details
        fields = "__all__"   

