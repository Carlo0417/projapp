from django.utils import timezone
from tkinter import CASCADE
from django.db import models

# Create your models here.
# ROOM
# Id	room_name	floor	dorm_name	description
# 1	101		1st	male dorm	4-bed spacer
# 2	102		1st	female dorm	2-bed spacer
# 3	103		1st	male dorm	4-bed spacer

class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Room(BaseModel):
    DORMNAME_CHOICES = (('Male Dorm','Male Dorm'), ('Female Dorm','Female Dorm'))
    room_name = models.CharField(max_length=25)
    floorlvl = models.CharField(max_length=25, verbose_name="Floor Level")
    dorm_name = models.CharField(max_length=25, choices=DORMNAME_CHOICES)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Rooms"

    def __str__(self):
        return f"{self.room_name}"

# SERVICE
# Id	service_name	is_offered      base_amount
# 1	    electricity		    1		      1000.00
# 2	    water			    1		      150.00
# 3	    laundry		        1		      400.00

class Service(BaseModel):
    STATUS_CHOICES = (('Available','Available'), ('Not Available','Not Available'))
    service_name = models.CharField(max_length=100)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    base_amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.service_name}"

# BED
# Id	room_id	    bed_no	   price
# 1	      101		  1		   1500.00
# 2	      101		  2		   1500.00
# 3	      101		  3		   1500.00
# 4	      102		  1		   2000.00
# 5	      102		  2		   2000.00
# 6	      103		  3		   1500.00

class Bed(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_no = models.CharField(max_length=5)
    price = models.CharField(max_length=25)
    bed_status = models.CharField(max_length=25, default="vacant", verbose_name="Status")

    class Meta:
        verbose_name_plural = "Beds"

    def __str__(self):
        return f"{self.bed_no}"


# USER
# Id	lastname	firstname	    psu_email	     username, password, secq, seca, recovery email
# 1	    martinez	kristine joy	kjmartinez@psu.palawan.edu.ph
# 2	    velasco	    kobe		    kobe@psu.palawan.edu.ph
# 3 	escurel	    carlo		    carlo@psu.palawan.edu.ph

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

# PERSON
# Id	userid*		office_dept		program	    rank		    gender		user_type, guardian, contact_no
# 1	      2		    ComStud Dept	BSIT		NULL				        occupant
# 2	      1		    Math Dept		NULL		Instructor I			    admin
# 3	      3		    ComStud Dept	BSIT		NULL				        occupant


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
    guardian_email_address = models.CharField(max_length=250, default="none", verbose_name="Guardian's email")
    guardian_present_address = models.CharField(max_length=250, default="none", verbose_name="Guardian's address")
    guardian_contact_no = models.CharField(max_length=20, default="none", verbose_name="Guardian's contact number")

    class Meta:
        verbose_name_plural = "Persons"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


    # BED_PRICE_HISTORY
    # bed_id*	start_date	price

class BedPriceHistory(BaseModel):
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = "Bed Price History"

    def __str__(self):
        return f"{self.bed.room_id}"

# OCCUPANT 
# Id person_id*     room_id  bed_id     start_date  end_date 
# 1     2              1      1       
# 2     3              1      2

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


# BILL 
# Id    bill_date   due_date    total    occupant_id* 
# 1     2022-04-12  2022-05-25  4000        2
# 2     2022-04-12  2022-05-25  4200        3

class Bill(BaseModel):
    bill_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Bills"

    def __str__(self):
        return f"{self.occupant}"


# BILL_DETAILS 
# Id    bill_id*   service_id*     description     amount 
# 1     1           1              room            2500.00 
# 2     1           1                              1000.00
# 3     1           2                               500.00 
# 4     2           1                              1500.00 
# 5     2           2                              1700.00 
# 6     2           3                              1000.00

class Bill_Details(BaseModel):
    # bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    bill_date = models.DateTimeField(default=timezone.now)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Bill Details"

    def __str__(self):
        return f"{self.bill}"


# PAYMENT
# Id    occupant_id*    payment_date    amount      receipt_no 
# 1     2               2022-05-20      3000        ABC10923 
# 2     2               2022-05-25      1000        DEF12243

class Payment(BaseModel):
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    receipt_no = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Payment"

    def __str__(self):
        return f"{self.occupant}"