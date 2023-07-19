from datetime import date, datetime 
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from oauth2_provider.models import AbstractApplication
from .managers import CustomUserManager

# AbstractUser
class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=50, unique=True, null=True, blank=True, verbose_name="Email Address")
    primary_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Primary phone number')
    nickname = models.CharField(_('nickname'), max_length=100, blank=True, null=True)
    local_name = models.CharField(_('local name'), max_length=100, blank=True, null=True)
    birthday = models.DateField(_('birthday'), null=True)
    age = models.IntegerField(_('age'), blank=True, default=0)
    gender = models.CharField(_('gender'), max_length=5, blank=True, null=True)
    biography = models.CharField(_('biography'), max_length=250, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # remove required fields

    objects = CustomUserManager()

    def __str__(self):
        return self.email
 
 #Pre_save Age by signal   
@receiver(pre_save, sender=User)
def update_age(sender, instance, **kwargs):
    today = date.today()

    if instance.birthday is not None:
        age = today.year - instance.birthday.year - ((today.month, today.day) < (instance.birthday.month, instance.birthday.day))
        
        if age < 0:
            age = 0
        
        instance.age = age
    
# Add related_name argument to avoid clashes with auth.User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set'  # Change 'custom_user_set' to your preferred related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set'  # Change 'custom_user_set' to your preferred related_name
    )


class AuthApplication(AbstractApplication):
    logo = models.ImageField(upload_to="applications/images", verbose_name="logo", blank=True, null=True)
    app_name = models.CharField(max_length=255, verbose_name="Application Name", blank=True)
    application_domain = models.CharField(max_length=255, blank=True, null=True, verbose_name="Application Domain")
    policy_url = models.URLField(blank=True, null=True, verbose_name="Policy URL")
    application_terms_url = models.URLField(blank=True, null=True, verbose_name="Policy URL")
    developer_mail = models.EmailField(max_length=250, blank=True, null=True, verbose_name="Developer E-mail")
    agree = models.BooleanField(_('agree'), default=False, help_text="Check if agree with our terms and conditions")
    
    def allows_grant_type(self, *grant_types):
        return bool(set([self.authorization_grant_type, self.GRANT_CLIENT_CREDENTIALS]) & grant_types)
