from datetime import date
import time

def get_current_time():
    """ Return the current date and time """
    today = date.today()
    current_time = time.strftime("%H:%M:%S", time.localtime())
    return today.strftime("%d/%m/%Y"), current_time
def get_last_n_years(n) -> list:
    last_n_years = []
    last_n_years.append(date.today().year)
    for i in range (1,n+1):
        last_n_years.append(date.today().year - i)
    return last_n_years

if __name__ == "__main__":
    print(get_last_n_years(3))