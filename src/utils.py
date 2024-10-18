from datetime import date
import time

def get_current_time():
    """ Return the current date and time """
    today = date.today()
    current_time = time.strftime("%H:%M:%S", time.localtime())
    return today.strftime("%d/%m/%Y"), current_time
