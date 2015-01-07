from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
    
class EndeavourUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)
 
    def create_superuser(self, email, password, first_name='', last_name='', **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

def validate_number(num):
    if len(num) < 10:
        raise ValidationError("Please specify at least a 10 digit phone number")
    
    
class EndeavourUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """    
    first_name = models.CharField(verbose_name='First Name', max_length=30, blank=True, default='')
    last_name = models.CharField(verbose_name='Last Name', max_length=30, blank=True, default='')
    email = models.EmailField(verbose_name='Email Address', max_length=254, unique=True, blank = False)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=20, blank=True, default='')
    
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
        
    objects = EndeavourUserManager()
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)
    
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
    
    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
    
    def __unicode__(self):
        return self.email