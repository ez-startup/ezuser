import random, string
from django.db import models
from usermanager.models import User
from django.utils.translation import gettext_lazy as _


class ProductType(models.Model):
    type_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created Date"))
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("Updated Date"))


class Product(models.Model):
    product_logo = models.ImageField(upload_to='product/images/', blank=True, null=True, verbose_name=_("Product Logo"))
    product_name = models.CharField(max_length=100, verbose_name=_('Product'))
    product_description = models.CharField(max_length=500, verbose_name=_("Product Description"))
    product_type = models.ForeignKey("ProductType", verbose_name=_("Product Type"), on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created Date"))
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("Updated Date"))

class License(models.Model):
    LICENSE_CHOICES = (
        ('M', 'Monthly'),
        ('A', 'Annual'),
        ('L', 'Lifetime'),
    )
    license_type = models.CharField(max_length=100, choices=LICENSE_CHOICES, default="Lifetime")
    product_key = models.CharField(max_length=50, unique=True, blank=True, editable=False, verbose_name=_("Product Key"))
    number = models.IntegerField(default=0, verbose_name=_("Number"))
    valid_date = models.DateTimeField(blank=True, verbose_name=_("Valid Date"))
    expired_date = models.DateTimeField(blank=True, null=True, verbose_name="Expired Date")
    product_id = models.ForeignKey("Product", verbose_name="Product ID", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created Date"))
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("Updated Date"))
    
    def save(self, *args, **kwargs):
        if not self.product_key:
            # Generate a random string of 5 characters
            chars = string.ascii_uppercase + string.digits
            key_parts = [random.choice(chars) for _ in range(5)]
            self.product_key = '-'.join(key_parts)
        super().save(*args, **kwargs)
    
class Device(models.Model):
    device_name = models.CharField(_("Device Name"), max_length=100, blank=True)
    ip_address = models.CharField(_("IP Address"), max_length=100, blank=True)
    mac_address = models.CharField(_("MAC Address"), max_length=30, blank=True)
    license_id = models.ForeignKey("License", verbose_name=_("License ID"), blank=True, null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created Date"))
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("Updated Date"))