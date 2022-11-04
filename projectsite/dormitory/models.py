from tabnanny import verbose
from django.utils import timezone
from tkinter import CASCADE
from django.db import models
from pkg_resources import require


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Room(BaseModel):
    DORMNAME_CHOICES = (('Male Dorm','Male Dorm'), ('Female Dorm','Female Dorm'), ('Foreign Dorm','Foreign Dorm'))
    FLOOR_CHOICES = (('1','1'), ('2','2'), ('3','3'))
    room_name = models.CharField(max_length=25)
    floorlvl = models.CharField(max_length=25, verbose_name="Floor Level", choices=FLOOR_CHOICES)
    dorm_name = models.CharField(max_length=25, choices=DORMNAME_CHOICES)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Rooms"

    def __str__(self):
        return f"{self.room_name}"

class Service(BaseModel):
    STATUS_CHOICES = (('Available','Available'), ('Not Available','Not Available'))
    service_name = models.CharField(max_length=100)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    base_amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.service_name}"

class Bed(BaseModel):
    BED_STATUS_CHIOCES = (('Vacant','Vacant'), ('Occupied','Occupied'),('Under Maint.','Under Maint.'))
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_code = models.CharField(max_length=25, default="none", verbose_name="Bed Code")
    price = models.DecimalField(default=0, max_digits=6, decimal_places=0)
    bed_status = models.CharField(max_length=25, default="Vacant", verbose_name="Status",  choices=BED_STATUS_CHIOCES)

    class Meta:
        verbose_name_plural = "Beds"

    def __str__(self):
        return f"{self.bed_code}"


class User(BaseModel):

    SECQ_CHOICES = (('In what city were you born?','In what city were you born?'), 
                    ('What is the name of your favorite pet?','What is the name of your favorite pet?'),
                    ('What is your mother''s maiden name?','What is your mother''s maiden name?'),
                    ('What high school did you attend?','What high school did you attend?'),
                    ('What was the name of your elementary school?','What was the name of your elementary school?'),
                    ('What was your favorite food as a child?','What was your favorite food as a child?'),
                    ('What year was your father (or mother) born?','What year was your father (or mother) born?'))
    
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    security_question = models.CharField(max_length=250, choices=SECQ_CHOICES)
    security_answer = models.CharField(max_length=250)
    recovery_email = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.lastname}"
        

class Person(BaseModel):

    OFFICE_DEPT_CHOICES = (('Electrical Engineering Department','Electrical Engineering Department'),
                            ('Computer Studies Department','Computer Studies Department'),
                            ('Department of Physical Education','Department of Physical Education'),
                            ('Department of Secondary Education','Department of Secondary Education'),
                            ('Bio-Physical Science Department','Bio-Physical Science Department'),
                            ('Architecture Department','Architecture Department'),
                            ('Civil Engineering Department','Civil Engineering Department'),
                            ('Department of Elementary Education','Department of Elementary Education'),
                            ('Petroleum Engineering Department','Petroleum Engineering Department'),
                            ('Dapartment of Secondary Education','Dapartment of Secondary Education'),
                            ('Mechanical Engineering Department','Mechanical Engineering Department'),
                            ('Not yet included','Not yet included'),)

    PROGRAM_CHOICES = (('BAMC','BAMC'),('BSEE','BSEE'),('BSTM','BSTM'),('BSA','BSA'),('BSIT','BSIT'),('BSN','BSN'),
    ('BPED','BPED'),('BSCrim','BSCrim'),('BSED-3','BSED-3'),('BSM','BSM'),('BSMB','BSMB'),('BSBA-ECO','BSBA-ECO'),
    ('BSHM','BSHM'),('BSAr','BSAr'),('BSP','BSP'),('BAPolSci','BAPolSci'),('BSCE','BSCE'),('BSTM','BSTM'),('BSPA','BSPA'),
    ('BSCS','BSCS'),('DM','DM'),('BEED','BEED'),('BSED-2','BSED-2'),('BSSW','BSSW'),('BSPE','BSPE'),('BSBA-FM','BSBA-FM'),
    ('BSB-MB','BSB-MB'),('BSED-1','BSED-1'),('BAPS','BAPS'),('BSME','BSME'),('BSBA-MM','BSBA-MM'),('BSMA','BSMA'),('BSES','BSES'),
    ('BSE','BSE'),('BSBA-HRDM','BSBA-HRDM'),('BSB-MD','BSB-MD'),)

    MUNICIPALITIES_CHOICES = (('None','None'),('Aborlan','Aborlan'),('Agutaya','Agutaya'),('Araceli','Araceli'),('Balabac','Balabac'),
    ('Batazar','Batazar'), ('Brooke''s Point','Brooke''s Point'),('Busuanga','Busuanga'),('Cagayancillo','Cagayancillo'),
    ('Coron','Coron'),('Culion','Culion'),('Cuyo','Cuyo'),('Dumaran','Dumaran'),('El Nido','El Nido'),
    ('Iwahig Penal Colony','Iwahig Penal Colony'),('Kalayaan','Kalayaan'),('Linapacan','Linapacan'),('Magsaysay','Magsaysay'),
    ('Narra','Narra'),('Puerto Princesa City','Puerto Princesa City'), ('Aborlan','Aborlan'),('Quezon','Quezon'),('Roxas','Roxas'),
    ('Rizal','Rizal'),('San Vicente','San Vicente'),('Sofronio Española','Sofronio Española'),('Taytay','Taytay'),)

    GENDER_CHOICES = (('Male','Male'),('Female','Female'),('LGBTQIA+','LGBTQIA+'),)
    TYPE_CHOICES = (('Local','Local'),('Foreign','Foreign'),)

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    psu_email = models.EmailField(max_length=250, default="", verbose_name="PSU Email")
    last_name = models.CharField(max_length=250, default="")
    first_name = models.CharField(max_length=250, default="")
    middle_name = models.CharField(max_length=250, default="", null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    boarder_type = models.CharField(max_length=50, default="Local", choices =TYPE_CHOICES)
    program = models.CharField(max_length=250, choices=PROGRAM_CHOICES)
    office_dept = models.CharField(max_length=250, choices=OFFICE_DEPT_CHOICES, verbose_name="Office / Department")
    contact_no = models.CharField(max_length=20, default="", verbose_name="Contact Number")
    address = models.CharField(max_length=250, default="", verbose_name="Address")
    city = models.CharField(max_length=250, default="Puerto Princesa City", verbose_name="City")
    municipality = models.CharField(max_length=250, default="None", verbose_name="Municipality", choices=MUNICIPALITIES_CHOICES)
    province = models.CharField(max_length=250, default="Palawan", verbose_name="Province")
    country = models.CharField(max_length=250, default="Philippines", verbose_name="Country")
    guardian_first_name = models.CharField(max_length=250, default="", verbose_name="Guardian's First name")
    guardian_last_name= models.CharField(max_length=250, default="", verbose_name="Guardian's Last name")
    guardian_email_address = models.EmailField(max_length=250, default="", verbose_name="Guardian's Email")
    guardian_present_address = models.CharField(max_length=250, default="", verbose_name="Guardian's Address")
    guardian_contact_no = models.CharField(max_length=20, default="", verbose_name="Guardian's Contact Number")

    #Admission Requiremnets
    Field1 = models.BooleanField(default=False, verbose_name='Two pieces 2"x2" coloured ID pictures taken not more than six months prior to the signing of the contract')
    Field2 = models.BooleanField(default=False, verbose_name='Medical Certificate from the University physician')
    Field3 = models.BooleanField(default=False, verbose_name='Fully accomplished application form (form OIA-OID)')
    Field4 = models.BooleanField(default=False, verbose_name='Special power of attorney (SPA) for guardian')
    Field5 = models.BooleanField(default=False, verbose_name='Photocopy of the University Identification card valid on the school year enrolled')
    Field6 = models.BooleanField(default=False, verbose_name='Certificate of Enrollment')
    Field7 = models.BooleanField(default=False, verbose_name='Photocopy of the dormitory ID')

    reg_status = models.CharField(max_length=20, default="None", verbose_name="Status", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Persons"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class BedPriceHistory(BaseModel):
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = "Bed Price History"

    def __str__(self):
        return f"{self.bed}"

class Occupant(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    bedPrice = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    end_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Occupants"

    def __str__(self):
        return f"{self.person}"

class Bill(BaseModel):
    bill_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Bills"

    def __str__(self):
        return f"{self.occupant}"


class Bill_Details(BaseModel):
    # bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)
    bill_date = models.DateTimeField(default=timezone.now)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, null=True, blank=True)
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = "Bill Details"

    def __str__(self):
        return f"{self.service}"

class Payment(BaseModel):
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    receipt_no = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Payment"

    def __str__(self):
        return f"{self.occupant}"