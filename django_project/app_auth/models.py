from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy
from django.core.validators import RegexValidator
from datetime import date, datetime
from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    # fields
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=gettext_lazy("Phone num format: '+999999999'. Up to 15 digits allowed."))
    SEX_CHOICES = (
        ('M', "Male"),
        ('F', "Female"),
        ('O', "Not to disclose"),
    )
    ID_PROOF = (
        ("socialid", "Social ID"),
        ('aadhar', "Aadhar"),
        ('pan', "PAN"),
        ("dl", "Driving License"),
        ("passport", "Passport"),
    )

    # Custom fields
    phone_number = models.CharField(max_length=17, null=True)
    image = models.ImageField(null=True)
    gender = models.CharField(max_length=1, null=True)
    whatsapp = models.BooleanField(default=False, null=True)
    watsapp_number = models.CharField(max_length=17, null=True)
    identification = models.CharField(max_length=20, null=True)
    identification_detail = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(null=True)
    # data_of_birth = models.CharField(max_length=20)
    occupation = models.CharField(max_length=100, null=True)
    address = models.TextField(max_length=256, null=True)
    state = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=20, null=True)
    education = models.CharField(max_length=20, null=True)
    pyma_activity = models.CharField(max_length=100, null=True)
    volunteering_week_hrs = models.DecimalField(max_digits=3, decimal_places=0, null=True)
    volunteering_brief = models.CharField(max_length=100, null=True)
    volunteering_detail = models.TextField(max_length=256, null=True)
    meditation_exp_years = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    meditation_brief = models.CharField(max_length=100, null=True)
    meditation_detail = models.TextField(max_length=256, null=True)
    contribution = models.CharField(max_length=100, null=True)
    hobbies = models.CharField(max_length=100, null=True)
    hobby_level = models.CharField(max_length=100, null=True)
    support = models.CharField(max_length=100, null=True)
    optional_details = models.TextField(max_length=256, null=True)
    pincode = models.DecimalField(max_digits=8, decimal_places=0, null=True)
    yfs_knowlege = models.CharField(max_length=15, null=True)
    comments_questions = models.TextField(max_length=256, null=True)

    # default fields / common settings
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['password']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def age(self):
        born = datetime.strptime(self.date_of_birth, "%Y-%m-%d").date()
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
