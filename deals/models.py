from django.db import models


class Deal(models.Model):
    customer = models.CharField(max_length=512)
    item = models.CharField(max_length=512)
    total = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField()
