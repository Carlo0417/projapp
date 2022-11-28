from faulthandler import disable
from certifi import where
from django.forms import ModelForm

from .models import Room, Bed, Service, Occupant, Person, Bill_Details, Payment, Demerit, OccupantDemerit
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"

class BedForm(ModelForm):
    class Meta:
        model = Bed
        fields = ['room','bed_code','bed_description', 'price', 'bed_status']

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

class OccupantForm(ModelForm):
    class Meta:
        model = Occupant
        fields = ['person','bed','start_date','end_date']

    def __init__(self, *args, **kwargs):
        occupant = kwargs.pop('occupant', None)
        super(OccupantForm, self).__init__(*args, **kwargs)
        self.fields['bed'].queryset = Bed.objects.filter(bed_status__icontains='vacant')
        occupants_id = Occupant.objects.all().values_list('person_id')
        self.fields['person'].queryset = Person.objects.filter(Field1__icontains=1, Field2__icontains=1, 
        Field3__icontains=1, Field4__icontains=1, Field5__icontains=1, Field6__icontains=1,
        Field7__icontains=1).exclude(id__in=occupants_id)

class OccupantFormEdit(ModelForm):
    class Meta:
        model = Occupant
        fields = ['person','bed','start_date','end_date']

    def __init__(self, *args, **kwargs):
        occupant = kwargs.pop('occupant', None)
        super(OccupantFormEdit, self).__init__(*args, **kwargs)
        self.fields['person'].queryset = Person.objects.filter(Field1__icontains=1, Field2__icontains=1, 
        Field3__icontains=1, Field4__icontains=1, Field5__icontains=1, Field6__icontains=1,Field7__icontains=1)

        # self.fields['bed'] = Bed.objects.raw('SELECT dormitory_bed.bed_code FROM dormitory_bed WHERE dormitory_bed.bed_code="MF1R1-AU" UNION SELECT dormitory_bed.bed_code FROM dormitory_bed WHERE dormitory_bed.bed_status="Vacant"')
        # self.fields['bed'].queryset = Bed.objects.filter(bed_code='MF1R1-AU')

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['psu_email','last_name','first_name','middle_name','gender','boarder_type','program',
                  'office_dept','contact_no','address','city','municipality','province','country',
                  'guardian_first_name','guardian_last_name','guardian_email_address',
                  'guardian_present_address','guardian_contact_no','Field1','Field2','Field3',
                  'Field4','Field5','Field6','Field7']
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

    def __init__(self, *args, **kwargs):
        bill = kwargs.pop('bill', None)
        super(BillingForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(status__icontains='Available').exclude(status__icontains='Not Available')

class BillingFormEdit(ModelForm):
    class Meta:
        model = Bill_Details
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        bill = kwargs.pop('bill', None)
        super(BillingFormEdit, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(status__icontains='Available').exclude(status__icontains='Not Available')
        self.fields['amount'].queryset = Service.objects.filter(service=self.object.id)

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"

class DemeritForm(ModelForm):
    class Meta:
        model = Demerit
        fields = "__all__"

class OccupantDemeritForm(ModelForm):
    class Meta:
        model = OccupantDemerit
        fields = "__all__"
