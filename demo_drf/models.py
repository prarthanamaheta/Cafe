from django.db import models



class Offer(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True, blank=True)
    state = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=0)

    def __str__(self):
        return self.name
