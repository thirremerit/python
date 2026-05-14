import datetime

currentDate = datetime.datetime.now()


print("year: ", currentDate.year)
print("month: ", currentDate.month)
print("day: ", currentDate.day)
print("hour: ", currentDate.hour)
print("minute: ", currentDate.minute)
print("second: ", currentDate.second)
print("microsecond: ", currentDate.microsecond)


print("---------------------")

currentDate2 = datetime.datetime.now().date()

print("Year:", currentDate2.year)
print("day:", currentDate2.day)
print("month:", currentDate2.month)


timeObject = datetime.time(12,30,45,123456)


print("ora: ", timeObject.hour)
print("minute: ", timeObject.minute)
print("second: ", timeObject.second)
print("microsecond: ", timeObject.microsecond)


specific_datetime = datetime.datetime(2024,1,1,12,25,1,2235)

formatdate =specific_datetime.strftime('%d-%m-%Y')

print(formatdate)


utc_time = datetime.datetime.now(datetime.timezone.utc)

print("cureent time:",utc_time)


custom = datetime.timedelta(hours=3)
