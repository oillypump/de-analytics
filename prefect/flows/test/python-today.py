from datetime import date, datetime, timedelta

# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)
print("date", now.strftime("%d_%m_%Y"))

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)

# date = now.strftime("%d_%m_%Y")
# print("date ",date)

# Get today's date
today = date.today()
print("Today is: ", today)
 
# Get 2 days earlier
yesterday = today - timedelta(days = 1)
yesterday1 = now.strftime("%d_%m_%Y")
print("Day before yesterday was: ", yesterday)