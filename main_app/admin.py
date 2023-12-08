from django.contrib import admin
# import your models here
from .models import Finch, Feeding

if not admin.site.is_registered(Finch):
    admin.site.register(Finch)

if not admin.site.is_registered(Feeding):
    admin.site.register(Feeding)