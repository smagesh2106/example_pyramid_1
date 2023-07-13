from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy
from django.core.validators import RegexValidator
from datetime import date, datetime
from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    # fields
    username = None
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=gettext_lazy("Phone num format: '+999999999'. Up to 15 digits allowed."))
    SEX_CHOICES = (
        ('M', "Male"),
        ('F', "Female"),
        ('O', "Not to disclose"),
    )
    ID_PROOF = (
        ("social_id", "Social ID"),
        ('aadhar', "Aadhar"),
        ('pan', "PAN"),
        ("dl", "Driving License"),
        ("passport", "Passport"),
    )

    # fields
    email = models.EmailField(unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False, null=False)
    image = models.ImageField()
    gender = models.CharField(max_length=1, choices=SEX_CHOICES, default=None, required=True)
    whatsapp = models.BooleanField(default=False)
    whatsapp_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    identification = models.CharField(max_length=20, choices=ID_PROOF,
                                      default=None, required=True, null=False, blank=False)
    identification_detail = models.CharField(max_length=50, default=None, required=True, null=False, blank=False)
    data_of_birth = models.DateField()
    occupation = models.CharField(max_length=100)
    address = models.TextField(max_length=256)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    education = models.CharField(max_length=20)
    pyma_activity = models.CharField(max_length=100)
    volunteering_week_hrs = models.DecimalField(max_length=3)
    volunteering_brief = models.CharField(max_length=100)
    volunteering_detail = models.TextField(max_length=256)
    meditation_exp_years = models.DecimalField(max_length=2, decimal_places=0)
    meditation_brief = models.CharField(max_length=100)
    meditation_detail = models.TextField(max_length=256)
    contribution = models.CharField(max_length=100)
    hobbies = models.CharField(max_length=100)
    hobby_level = models.CharField(max_length=100)
    support = models.CharField(max_length=100)
    optional_details = models.TextField(max_length=256)
    pincode = models.DecimalField(max_length=8, decimal_places=0)
    yfs_knowlege = models.CharField(max_length=15)
    comments_questions = models.TextField(max_length=256)

    
    # common settings
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", ]
    objects = CustomUserManager

    def __str__(self):
        return self.email

    def age(self):
        born = datetime.strptime(self.data_of_birth, "%d/%m/%Y").date()
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
