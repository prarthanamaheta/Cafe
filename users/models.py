from django.db import models
from demo_django.managers import MyUserManager
from demo_django.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Create your models here.
class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    """
    User model
    """

    is_admin = models.BooleanField(default=False)
    email = models.EmailField(verbose_name="email_address", unique=True)
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    is_superuser = models.BooleanField(verbose_name="superuser", default=False)
    is_staff = models.BooleanField(verbose_name="staff", default=False)
    is_verified = models.BooleanField(default=False)

    # class Meta:
    #     unique_together = ("email", "cafe")

    def __str__(self):
        if self.first_name:
            return f"{self.first_name} {self.last_name}"
        return f"{self.email}"

    objects = MyUserManager()

    USERNAME_FIELD = "email"
