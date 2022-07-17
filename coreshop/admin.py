from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Tags)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)


