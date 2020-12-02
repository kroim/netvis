import datetime

date_string = str(datetime.datetime.now())
cur_date = date_string.split('.')[0]
print(cur_date)
