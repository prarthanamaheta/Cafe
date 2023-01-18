from django.db import models
from django_tenants.models import TenantMixin

from demo_django.managers import MyUserManager
from demo_django.models import BaseModel
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin


# Create your models here.

class Customer(BaseModel, TenantMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    auto_create_schema = True
    auto_drop_schema = True

    def __str__(self):
        return self.name


class Domain(BaseModel):
    domain = models.CharField(max_length=300, unique=True, db_index=True)
    tenant = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='domains')
    is_primary = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.domain



