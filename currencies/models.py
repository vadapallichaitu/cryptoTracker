from django.db import models
from django.conf import settings
from django import forms
from django.contrib.auth.models import User
# Create your models here.
class CryptoModel(models.Model):

    crypto_name = models.CharField(primary_key=True,max_length=200)
    crypto_symbol = models.CharField(max_length=10)
    last_traded_value = models.FloatField()
    Day_low = models.FloatField()
    Day_high = models.FloatField()

    class Meta:
        verbose_name_plural = "Cryptos"

    def __str__(self):
        return self.crypto_name

    
class PortfolioModel(models.Model):
    
    
    market = models.ForeignKey(CryptoModel,on_delete=models.SET_DEFAULT,default = 1)
    quantity = models.FloatField()
    bought_at = models.FloatField()

    class Meta:
        verbose_name_plural = "Items"

    def __str__(self):
        return self.market.crypto_name

class KeyFormModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    primary_key = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=200)
    

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Keys'



