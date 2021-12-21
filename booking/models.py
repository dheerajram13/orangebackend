import uuid
from django.db import models


class Customer(models.Model):
    """ A model to create customer record in the DB"""
    name = models.CharField(max_length=30, null=False,blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return 'name: {} phone: {} '.format(self.name, self.phone)
    
    class Meta:
        unique_together = ('name', 'phone',)


class TimeSlot(models.Model):
    """ A model to create time slot in the DB"""
    start_time = start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    available_slots = models.PositiveIntegerField(default=3)
    is_slot_available = models.BooleanField(default=True)

    def __str__(self):
        return  str(self.start_time)+"-"+str(self.end_time)



class Booking(models.Model):
    """ A model to create a booking """
    booking_id = models.UUIDField(unique=True,default=uuid.uuid4, editable=False)
    time_slot = models.ForeignKey(TimeSlot,blank=True, null=True,on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer,blank=True, null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.booking_id)
    
    
    class Meta:
        # making customer & time slot unique together to avoid duplication for the time slot.
        unique_together = ('customer', 'time_slot')







