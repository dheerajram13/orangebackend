import logging
from .models import TimeSlot
logger = logging.getLogger(__file__)



def reset_time_slots():
    # Loop through all the time slots and reset their values.
    time_slots = TimeSlot.objects.all()
    for t in time_slots:
        try:
            time  = TimeSlot.objects.get(id=t.id)
        except TimeSlot.DoesNotExist:
            continue
        time.available_slots = 3 
        time.is_slot_available = True
        time.save()
        logging.info("%s: Updating the time id: %s",
                    reset_time_slots.__name__, t.id,)


