from django.contrib import admin
from .models import CryptoModel,PortfolioModel,KeyFormModel
# Register your models here.
admin.site.register(CryptoModel)
admin.site.register(PortfolioModel)
admin.site.register(KeyFormModel)