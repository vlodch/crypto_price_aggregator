# models.py in your backend app

from django.db import models

class Currency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Change the max_digits and decimal_places as needed

    def __str__(self):
        return self.name
