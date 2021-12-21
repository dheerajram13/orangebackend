from django.contrib import admin
from .models import TimeSlot,Customer,Booking

admin.site.register(TimeSlot)
admin.site.register(Booking)
admin.site.register(Customer)