import datetime

today = datetime.date.today()
print(today)
yes = datetime.timedelta(days=-1)
yes = today+yes
print(yes)