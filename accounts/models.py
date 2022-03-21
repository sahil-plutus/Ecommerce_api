from django.db import models
from django.contrib.auth.models import User

class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=122)
    address = models.CharField(max_length=122)
    locality = models.CharField(max_length=122)
    landmark = models.CharField(max_length=122)
    contact_number = models.CharField(max_length=12)