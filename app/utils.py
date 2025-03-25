from datetime import date
from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR

def calculate_working_days(start_date: date, end_date: date):
    days = rrule(
        DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR)
    )
    return len(list(days)) 