import json
from time import localtime
import requests

from datetime import datetime, date



timestr = "2022-07-31"
love_date = datetime.strptime(timestr, "%Y-%m-%d").date()
print(love_date)
# love_date = date(2022, 7, 31)

year = localtime().tm_year
month = localtime().tm_mon
day = localtime().tm_mday
today = datetime.date(datetime(year=year, month=month, day=day))

print(str(today.__sub__(love_date)).split(" ")[0])
