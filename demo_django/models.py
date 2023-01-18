from django.utils.translation import gettext_lazy as _

from django.db import models

from django.contrib.postgres.fields import ArrayField

from demo_drf.models import Offer


class BaseModel(models.Model):
    """
    Base model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.URLField(max_length=400, null=True, blank=True)
    image = models.ImageField(upload_to='images/', default='')
    categorys = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='categorys')
    types = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True, related_name='types')
    items = ArrayField(models.CharField(max_length=100, null=True, blank=True, ),
                       null=True, blank=True, size=20, default=list)

    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        WAITING = 'waiting', _('Waiting')
        RECEIVED = 'received', _('Received')
        PROGRESS = 'progress', _('IN Progress')
        COMPLETED = 'completed', _('Completed')

    token = models.IntegerField(default=0)
    foods_ordered = ArrayField(models.CharField(max_length=100, null=True, blank=True, ),
                               null=True, blank=True, size=20, default=list)
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.WAITING,
    )
    total_payment = models.FloatField(default=0)
    payment_received = models.BooleanField(default=False)
    offers = models.ManyToManyField(Offer, blank=True, related_name='offers')
    payment_mode = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.token}'


class Visitor(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='orders')
    name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.IntegerField(max_length=10, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name}'
