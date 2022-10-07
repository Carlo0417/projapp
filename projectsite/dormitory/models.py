from django.utils import timezone
from tkinter import CASCADE
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Room(BaseModel):
    DORMNAME_CHOICES = (('Male Dorm','Male Dorm'), ('Female Dorm','Female Dorm'), ('Foreign Dorm','Foreign Dorm'))
    room_name = models.CharField(max_length=25)
    floorlvl = models.CharField(max_length=25, verbose_name="Floor Level")
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
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_no = models.CharField(max_length=5)
    price = models.CharField(max_length=25)
    bed_status = models.CharField(max_length=25, default="vacant", verbose_name="Status")

    class Meta:
        verbose_name_plural = "Beds"

    def __str__(self):
        return f"{self.bed_no}"


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

    OFFICE_DEPT_CHOICES = (('Computer Studies Department','Computer Studies Department'),
                            ('Math Department','Math Department'),
                            ('Science Department','Science Department'),
                            ('Physical Education Department','Physical Education Department'))

    PROGRAM_CHOICES = (('BSIT','BSIT'),('BSCS','BSCS'),('BSM','BSM'),('BSS','BSS'),('BSPE','BSPE'),('NULL','NULL'))

    GENDER_CHOICES = (('Male','Male'),('Female','Female'),('Gay','Gay'),('Lesbian','Lesbian'),('Transgender','Transgender'),)
    TYPE_CHOICES = (('Local','Local'),('Foreign','Foreign'))

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    psu_email = models.CharField(max_length=250, default="none", verbose_name="PSU Email")
    last_name = models.CharField(max_length=250, default="none")
    first_name = models.CharField(max_length=250, default="none")
    middle_name = models.CharField(max_length=250, default="none", null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    boarder_type = models.CharField(max_length=50, default='Local',choices =TYPE_CHOICES)
    program = models.CharField(max_length=250, choices=PROGRAM_CHOICES)
    office_dept = models.CharField(max_length=250, choices=OFFICE_DEPT_CHOICES, verbose_name="Office / Department")
    contact_no = models.CharField(max_length=20)
    address= models.CharField(max_length=250, default="none", verbose_name="address")
    city = models.CharField(max_length=250, default="Puerto Princesa City", verbose_name="city")
    municipality = models.CharField(max_length=250, default="none", verbose_name="municipality")
    province = models.CharField(max_length=250, default="Palawan", verbose_name="province")
    country = models.CharField(max_length=250, default="Philippines", verbose_name="country")
    guardian_first_name = models.CharField(max_length=250, default="none", verbose_name="Guardian's First name")
    guardian_last_name= models.CharField(max_length=250, default="none", verbose_name="Guardian's Last name")
    guardian_email_address = models.CharField(max_length=250, default="none", verbose_name="Guardian's Email")
    guardian_present_address = models.CharField(max_length=250, default="none", verbose_name="Guardian's Address")
    guardian_contact_no = models.CharField(max_length=20, default="none", verbose_name="Guardian's Contact Number")

        #Admission Requiremnets
    Field1 = models.BooleanField(default=False)
    Field2 = models.BooleanField(default=False)
    Field3 = models.BooleanField(default=False)
    Field4 = models.BooleanField(default=False)
    Field5 = models.BooleanField(default=False)
    Field6 = models.BooleanField(default=False)
    Field7 = models.BooleanField(default=False)


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
        return f"{self.bed.room_id}"

class Occupant(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    bedPrice = models.DecimalField(default=0, max_digits=6, decimal_places=2)
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