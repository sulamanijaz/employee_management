from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import RegexValidator
# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', False)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=400)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=20)
    email = models.EmailField(max_length=140, unique=True)
    no_of_employees = models.IntegerField()
    time_zone = models.CharField(max_length=400)
    parent_user = models.IntegerField(blank=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = self.fullname
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.fullname

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Employees(models.Model):
    parent_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_parent', on_delete=models.CASCADE)
    employee_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_id', on_delete=models.CASCADE)
    check_intime = models.DateTimeField()
    check_outime = models.DateTimeField()
    total_hours = models.IntegerField()


class EmployeeSchedule(models.Model):
    parent_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='sch_parent', on_delete=models.CASCADE)
    employee_id = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='sch_employee', on_delete=models.CASCADE)
    # Day_date = models.DateTimeField()
    shift_start = models.DateTimeField()
    shift_ends = models.DateTimeField()
    availability = models.NullBooleanField(default=True)
    recurring = models.CharField(max_length=200)
