from tabnanny import verbose
from django.utils import timezone
from tkinter import CASCADE
from django.db import models
from pkg_resources import require
from datetime import timedelta
from decimal import Decimal
from django.core.validators import MinValueValidator
from datetime import datetime, date
from phonenumber_field.modelfields import PhoneNumberField

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
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
    service_name = models.CharField(max_length=300)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    base_amount = models.DecimalField(default=0, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.service_name}"


class Bed(BaseModel):
    BED_STATUS_CHIOCES = (('Vacant','Vacant'), ('Occupied','Occupied'),('Under Maint.','Under Maint.'))
    BED_PRICE = ((1500,1500), (4500,4500))
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_code = models.CharField(max_length=25, default="", verbose_name="Bed Code")
    bed_description = models.CharField(max_length=250, default="", verbose_name="Description")
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2, choices=BED_PRICE)
    bed_status = models.CharField(max_length=25, default="Vacant", verbose_name="Status",  choices=BED_STATUS_CHIOCES)

    class Meta:
        verbose_name_plural = "Beds"

    def __str__(self):
        return f"{self.bed_code}"


class User(BaseModel):

    USER_STATUS_CHOICES = (('active','active'),('inactive','inactive'),)

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
    security_question = models.CharField(max_length=250, choices=SECQ_CHOICES, blank=True, null=True)
    security_answer = models.CharField(max_length=250, blank=True, null=True)
    recovery_email = models.CharField(max_length=250, blank=True, null=True)
    user_status = models.CharField(max_length=20, default="inactive", null=True, blank=True, choices=USER_STATUS_CHOICES)
    phone_number = models.CharField(max_length=20, default="", verbose_name="Contact Number")
    person_id = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.person_id}"


class Admin(BaseModel):

    ADMMIN_CLASS_CHOICES = (('Front Desk','Front Desk'),('Accounting Staff','Accounting Staff'), 
                            ('Super Administrator','Super Administrator'), ('Dorm Manager','Dorm Manager'),)

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
    security_question = models.CharField(max_length=250, choices=SECQ_CHOICES, blank=True, null=True)
    security_answer = models.CharField(max_length=250, blank=True, null=True)
    recovery_email = models.CharField(max_length=250, blank=True, null=True)
    admin_class = models.CharField(max_length=20, null=True, blank=True, choices=ADMMIN_CLASS_CHOICES)

    class Meta:
        verbose_name_plural = "Admins"

    def __str__(self):
        return f"{ self.admin_class}"

class Person(BaseModel):

    PROGRAM_CHOICES = (('Bachelor of Science in Social Work','Bachelor of Science in Social Work'),
                        ('Bachelor of Science in Psychology','Bachelor of Science in Psychology'),
                        ('Bachelor of Arts in Communication','Bachelor of Arts in Communication'),
                        ('Bachelor of Arts in Political Science','Bachelor of Arts in Political Science'),
                        ('Bachelor of Arts in Philippine Studies','Bachelor of Arts in Philippine Studies'),
                        ('Bachelor of Science in Biology Major in Medical Biology','Bachelor of Science in Biology Major in Medical Biology'),
                        ('Bachelor of Science in Marine Biology','Bachelor of Science in Marine Biology'),
                        ('Bachelor of Science in Environmental Science','Bachelor of Science in Environmental Science'),
                        ('Bachelor of Science in Information Technology','Bachelor of Science in Information Technology'),
                        ('Bachelor of Science in Computer Science','Bachelor of Science in Computer Science'),
                        ('Bachelor of Science in Physical Education','Bachelor of Science in Physical Education'),
                        ('Bachelor of Science in Elementary Education','Bachelor of Science in Elementary Education'),
                        ('Bachelor of Science in Secondary Education Major in Science','Bachelor of Science in Secondary Education Major in Science'),
                        ('Bachelor of Science in Secondary Education Major in Math','Bachelor of Science in Secondary Education Major in Math'),
                        ('Bachelor of Science in Secondary Education Major in English','Bachelor of Science in Secondary Education Major in English'),
                        ('Bachelor of Science in Secondary Education Major in Filipino','Bachelor of Science in Secondary Education Major in Filipino'),
                        ('Bachelor of Science in Secondary Education Major in Social Studies','Bachelor of Science in Secondary Education Major in Social Studies'),
                        ('Bachelor of Science in Secondary Education Major in Values','Bachelor of Science in Secondary Education Major in Values'),
                        ('Bachelor of Science in Accountancy','Bachelor of Science in Accountancy'),
                        ('Bachelor of Science in Management Accountancy','Bachelor of Science in Management Accountancy'),
                        ('Bachelor of Science in Entrepreneurship','Bachelor of Science in Entrepreneurship'),
                        ('Bachelor of Science in Business Administration  Major in Marketing Management','Bachelor of Science in Business Administration  Major in Marketing Management'),
                        ('Bachelor of Science in Business Administration  Major in Human Resource Management','Bachelor of Science in Business Administration  Major in Human Resource Management'),
                        ('Bachelor of Science in Hospitality Management','Bachelor of Science in Hospitality Management'),
                        ('Track - Culinary Arts and Kitchen Management','Track - Culinary Arts and Kitchen Management'),
                        ('Bachelor of Science in Tourism Management','Bachelor of Science in Tourism Management'),
                        ('Track - Hotel,Resort, and Club Management','Track - Hotel,Resort, and Club Management'),
                        ('Bachelor of Science in Civil Engineering','Bachelor of Science in Civil Engineering'),
                        ('Bachelor of Science in Mechanical Engineering','Bachelor of Science in Mechanical Engineering'),
                        ('Bachelor of Science in Electrical Engineering','Bachelor of Science in Electrical Engineering'),
                        ('Bachelor of Science in Petroleum Engineering','Bachelor of Science in Petroleum Engineering'),
                        ('Bachelor of Science in Architecture','Bachelor of Science in Architecture'),
                        ('Bachelor of Science in Nursing','Bachelor of Science in Nursing'),
                        ('Diploma in Midwifery','Diploma in Midwifery'),
                        ('Bachelor of Science in Midwifery','Bachelor of Science in Midwifery'),
                        ('Bachelor of Science in Criminology','Bachelor of Science in Criminology'),)

    MUNICIPALITIES_CHOICES = (('None','None'),('Aborlan','Aborlan'),('Agutaya','Agutaya'),('Araceli','Araceli'),('Balabac','Balabac'),
    ('Batazar','Batazar'), ('Brooke''s Point','Brooke''s Point'),('Busuanga','Busuanga'),('Cagayancillo','Cagayancillo'),
    ('Coron','Coron'),('Culion','Culion'),('Cuyo','Cuyo'),('Dumaran','Dumaran'),('El Nido','El Nido'),
    ('Iwahig Penal Colony','Iwahig Penal Colony'),('Kalayaan','Kalayaan'),('Linapacan','Linapacan'),('Magsaysay','Magsaysay'),
    ('Narra','Narra'),('Puerto Princesa City','Puerto Princesa City'), ('Quezon','Quezon'),('Roxas','Roxas'),
    ('Rizal','Rizal'),('San Vicente','San Vicente'),('Sofronio Española','Sofronio Española'),('Taytay','Taytay'),)

    GENDER_CHOICES = (('Male','Male'),('Female','Female'),('LGBTQIA+','LGBTQIA+'),)
    TYPE_CHOICES = (('Local','Local'),('Foreign','Foreign'),)

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    psu_email = models.EmailField(max_length=250, default="", verbose_name="PSU Email")
    last_name = models.CharField(max_length=250, default="")
    first_name = models.CharField(max_length=250, default="")
    middle_name = models.CharField(max_length=250, default="", null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    boarder_type = models.CharField(max_length=50, default="Local", choices=TYPE_CHOICES)
    program = models.CharField(max_length=250, choices=PROGRAM_CHOICES)
    office_dept = models.CharField(max_length=250, verbose_name="Office / Department", null=True, blank=True)
    contact_no = PhoneNumberField()
    address = models.CharField(max_length=250, default="", verbose_name="Address")
    city = models.CharField(max_length=250, default="Puerto Princesa City", verbose_name="City")
    municipality = models.CharField(max_length=250, default="None", verbose_name="Municipality", choices=MUNICIPALITIES_CHOICES)
    province = models.CharField(max_length=250, default="Palawan", verbose_name="Province")
    country = models.CharField(max_length=250, default="Philippines", verbose_name="Country")
    guardian_first_name = models.CharField(max_length=250, default="", verbose_name="Guardian's First name")
    guardian_last_name= models.CharField(max_length=250, default="", verbose_name="Guardian's Last name")
    guardian_email_address = models.EmailField(max_length=250, default="", verbose_name="Guardian's Email")
    guardian_present_address = models.CharField(max_length=250, default="", verbose_name="Guardian's Address")
    guardian_contact_no = PhoneNumberField()
    

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
    
    def save(self, *args, **kwargs):
        if not self.middle_name:
            self.middle_name = ""
        super().save(*args, **kwargs)


class BedPriceHistory(BaseModel):
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = "Bed Price History"

    def __str__(self):
        return f"{self.bed}"
        

def one_month_from_today():
    return timezone.now() + timedelta(days=30)

class Occupant(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    bedPrice = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    end_date = models.DateTimeField(default=one_month_from_today, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Occupants"

    def __str__(self):
        return f"{self.person}"

    @property
    def is_past_due(self):
        return date.today() > self.end_date


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
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE, null=True, blank=True)
    bill_date = models.DateTimeField(default=timezone.now)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=250,  default="None")
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,)
    let_ref = models.CharField(max_length=250,  default="None")
    class Meta:
        verbose_name_plural = "Bill Details"

    def __str__(self):
        return f"{self.service}"


class Payment(BaseModel):
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    receipt_no = models.CharField(max_length=250)
    pay_let_ref = models.CharField(max_length=250,  default="None")

    class Meta:
        verbose_name_plural = "Payment"

    def __str__(self):
        return f"{self.occupant}"


class Demerit(BaseModel):

    DEMERITS_CHOICES = (('Transfer to other rooms without permission','Transfer to other rooms without permission'),
                        ('Doing malicious conduct on dormitory premises','Doing malicious conduct on dormitory premises'),
                        ('Allowing opposite sex other than the parents to enter his/her room','Allowing opposite sex other than the parents to enter his/her room'),
                        ('Possessing inside the dormitory any firearm, bladed weapon, or any kind of dangerous and deadly weapon; Provided, that this shall not possess the in connection with their studies and have a permit for the purpose',
                        'Possessing inside the dormitory any firearm, bladed weapon, or any kind of dangerous and deadly weapon; Provided, that this shall not possess the in connection with their studies and have a permit for the purpose'),
                        ('Oral defamation against co-residents','Oral defamation against co-residents'),
                        ('Bullying','Bullying'),
                        ('Threatening or any attempt to any member of the dormitory with physical harm; unlawfully preventing or threatening the dormitory residents or other dormitory officials to enter the dormitory premises',
                        'Threatening or any attempt to any member of the dormitory with physical harm; unlawfully preventing or threatening the dormitory residents or other dormitory officials to enter the dormitory premises'),
                        ('Non-Securing of Dormitory forms i.e. curfew extension and renewal/clearance forms','Non-Securing of Dormitory forms i.e. curfew extension and renewal/clearance forms'),
                        ('Non-Compliance related to room checking procedures','Non-Compliance related to room checking procedures'),
                        ('Non-Compliance to the administrative and dormitory superintendents','Non-Compliance to the administrative and dormitory superintendents'),
                        ('Bringing of appliances without the approval of the dormitory parent','Bringing of appliances without the approval of the dormitory parent'),
                        ('Laundering of clothes inside the dormitory','Laundering of clothes inside the dormitory'),
                        ('Use electrical appliances, including ironing of clothes inside the dormitory','Use electrical appliances, including ironing of clothes inside the dormitory'),
                        ('Returning after curfew hour or very late from time in indicated on the curfew extension form','Returning after curfew hour or very late from time in indicated on the curfew extension form'),
                        ('Lending dormitory ID to the outsider and co-residents to enter the dormitory premises','Lending dormitory ID to the outsider and co-residents to enter the dormitory premises'),
                        ('Using other personal things without permission to the owner','Using other personal things without permission to the owner'),
                        ('Failure to do proper waste segregation and or throwing garbage in improper places','Failure to do proper waste segregation and or throwing garbage in improper places'),
                        ('Disturbing / Disrespect on the privacy of others including making noise after curfew hours and playing loud music inside the dormitory',
                        'Disturbing / Disrespect on the privacy of others including making noise after curfew hours and playing loud music inside the dormitory'),
                        ('Vandalism','Vandalism'),
                        ('Failure to register in logbook','Failure to register in logbook'),
                        ('Not turning off the fan, aircon, lights and faucet','Not turning off the fan, aircon, lights and faucet'),
                        ('Shouting and making nuisance inside the dormitory','Shouting and making nuisance inside the dormitory'),
                        ('Bringing pets in the dormitory','Bringing pets in the dormitory'),
                        ('Walking around beyond time limits (11:00 PM only)','Walking around beyond time limits (11:00 PM only)'),)

    POINTS_CHOICES = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),)

    demerit_name = models.CharField(max_length=500, choices=DEMERITS_CHOICES)
    demerit_points = models.CharField(max_length=2, choices=POINTS_CHOICES)

    class Meta:
        verbose_name_plural = "Demerits"

    def __str__(self):
        return f"{self.demerit_name}"


class OccupantDemerit(BaseModel):
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)
    demerit_name = models.ForeignKey(Demerit, on_delete=models.CASCADE)
    cur_date = models.DateTimeField(default=timezone.now)
    prev_remarks = models.TextField(max_length=500, default="None")
    new_remarks = models.TextField(max_length=500, default="", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Occupant Demerits"

    def __str__(self):
        return f"{self.occupant}"