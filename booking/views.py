import logging
from datetime import date
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer,TimeSlot,Booking
from django.db import IntegrityError
from .utils import validate_time_slot,validate_name,validate_phone
from .cron import reset_time_slots

logger = logging.getLogger(__file__)

@api_view(['GET',])
def time_slot_list(request):
    """
    List all code time slots for the day.
    """
    context = {}
    if request.method == 'GET':
        # reset_time_slots() ## Remove the comment for this line to reset the time slots. Ideal for the dev environment 
        # Getting all the time slots
        slots = TimeSlot.objects.all().order_by('id')
        # When time slot table is empty
        if slots.count() == 0:
            # Create records for time slots from 7AM to 8PM.
            for i in range(7,21):
                start_t = str(i)+":00:00"
                end_t = str(i+1)+":00:00"
                TimeSlot.objects.create(start_time = start_t,end_time=end_t)    
        # Building context for the time slots
        for slot in slots:
            context[str(slot)] = {
                "available_slots": slot.available_slots,
                "slot_available": slot.is_slot_available
            }
        return Response(context,status=status.HTTP_200_OK)       
    return Response({"meaasge":"Please use GET request!"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerBookingAPI(APIView):
    """
    A class to create a booking for the customer 
    """
    parser_classes = (parsers.JSONParser,)

    def post(self, request):
        """
        Create a Booking for the customer for the selected slot.
        """
        try:
            name_val = request.data['name']
            phone_val = request.data['phone']
            time = request.data['time']
        except KeyError:
            logger.error(
                "%s: Request received with incomplete data.",
                self.__class__.__name__)
            return Response(
                {
                    "message": "All fields (phone, name and time_slot) are not provided"},
                status=status.HTTP_400_BAD_REQUEST)
        # validating all the input data.
        name = validate_name(name_val)
        phone = validate_phone(phone_val)
        time_slot = validate_time_slot(time)

        start_time = time_slot[0]
        end_time = time_slot[1]

        # checking if the provided input data is None
        if name == None:
            return Response(
                {"message": "Received an empty name. Please fill your name."},
                status=status.HTTP_400_BAD_REQUEST) 
        if phone == None:
            return Response(
                { "message": "Received incorrect phone number. Please fill your phone number."},
                status=status.HTTP_400_BAD_REQUEST)
        if start_time == None or end_time ==None:
            return Response(
                { "message": "Received incorrect time slots. Please provide time slot(ex:02PM-03PM)"},
                status=status.HTTP_400_BAD_REQUEST)

        # Checking if the provided time slot is available in Time Slot Table or Not 
        try:
            time = TimeSlot.objects.get(start_time=start_time,end_time=end_time)
        except TimeSlot.DoesNotExist:
            logger.error(
                "%s: Received incorrect slot time start: %s - end: %s for customer phone: %s.",
                self.__class__.__name__,
                start_time,
                end_time,
                phone)
            return Response(
                {"message": "Received incorrect time slot. Please provide time slot(ex:02PM-03PM)"},
                status=status.HTTP_400_BAD_REQUEST)


        try:
            # Checking if customer exists in the Customer Table or Not.
            customer = Customer.objects.get(name=name,phone=phone)
        except Customer.DoesNotExist:
            # if not there, then creating a customer record in the table.
            customer = Customer.objects.create(name=name,phone=phone)

        # Filtering the booking records for with the customer instance 
        bookings = Booking.objects.select_related('customer').filter(customer=customer,created_at__date=date.today())
        
        # if the customer has total 3 bookings then the customer can't book slot for today. 
        if bookings.count() >= 3:
            logger.error(
                "%s: No of bookings limit exceded for today for customer phone: %s",
                self.__class__.__name__,
                phone)
            return Response(
                {
                    "message": "You have exceded the booking limit."}, 
                status=status.HTTP_400_BAD_REQUEST)

        # Checking if the customer selected time slot is avaialble or not 
        if time.available_slots == 0:
            logger.error(
                "%s: Time slot %s has been already booked by other customer",
                self.__class__.__name__,
                time)
            return Response(
                {
                "message": "Selected time slot has been already booked by other customer. Please try a different one!"},
                status=status.HTTP_400_BAD_REQUEST)
        # To handle concurrency in booking
        with transaction.atomic():
            # Checking if there are no duplicates for the same slot.
            try:
                booking = Booking.objects.create(
                    customer = customer,
                    time_slot = time 
                )
            except IntegrityError:
                return Response({"message":"You have already booked a slot"})
            # Once booking is done, reducing the available_slots count by 1 
            time.available_slots -= 1
            # Checking if available_slots for a time slot is equal to 0   
            if time.available_slots == 0:
                # Updating the is_slot_available to False
                time.is_slot_available = False
            time.save()
        # if there is a successfull booking
        if booking:
            context = {
                "is_success":True,
                "slot_id":booking.booking_id
            }
            return Response(context,status=status.HTTP_201_CREATED)
        return Response({"is_success":False}, status=status.HTTP_400_BAD_REQUEST)
