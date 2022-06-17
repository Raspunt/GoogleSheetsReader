from django.db import models




class Orders(models.Model):

    product_number = models.IntegerField()
    price_dollars = models.FloatField()
    price_rubles = models.FloatField()
    date = models.CharField(max_length=100)
