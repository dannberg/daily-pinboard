import pinboard
from datetime import datetime, date, time, timezone
from dateutil.relativedelta import relativedelta

pb = pinboard.Pinboard('dannberg:351F526D563F33F2F9FC')

currentMonth = datetime.now().month
currentDay = datetime.now().day

three_yrs_ago = datetime.now() - relativedelta(years=3)
pb.posts.get(three_yrs_ago)
