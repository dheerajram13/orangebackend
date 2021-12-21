
from datetime import datetime

# Created a function to validate the name
def validate_name(name):
    if len(name) == 0 or name == "":
        return None
    return name

# Created a function to validate the phone
def validate_phone(phone):
    if len(phone) == 0 or phone =="" or len(phone)>10:
        return None 
    return phone

# Created a function to validate the time slot 
def validate_time_slot(time):
    if time == "" or len(time) == 0 or len(time)!=9:
        return None,None
    tmp = time.split("-")
    start_am_or_pm = tmp[0][2:]
    end_am_or_pm = tmp[1][2:]
    # checking if start time is am or pm
    if start_am_or_pm.lower() == "am":
        start_time = str(tmp[0][0:2])+":00:00"
    elif start_am_or_pm.lower() == "pm" and int(tmp[0][0:2]) != 12:
        start_time = str(12+int(tmp[0][0:2]))+":00:00"
    else:
        start_time = str(tmp[0][0:2])+":00:00"
     # checking if start time is am or pm
    if end_am_or_pm.lower() == "am":
        end_time = str(tmp[1][0:2])+":00:00"
    elif end_am_or_pm.lower()=="pm" and int(tmp[1][0:2]) != 12:
        end_time = str(12+int(tmp[1][0:2]))+":00:00"
    else:
        end_time = str(tmp[1][0:2])+":00:00"
        
    FMT = '%H:%M:%S'
    # Calculating the time difference between end and start times.
    time_delta = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)
    # Converting hours to mins
    time_delta_in_mins = int(round(time_delta.total_seconds() / 60))
    # Checking if mins if diff is 1 hour
    if time_delta_in_mins == 60:
        return start_time,end_time
    return None,None
