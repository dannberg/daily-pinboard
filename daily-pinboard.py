import pinboard
from datetime import datetime, timedelta

pb = pinboard.Pinboard('dannberg:351F526D563F33F2F9FC')
firstPostYear = 2012

# currentMonth = datetime.now().month
# currentDay = datetime.now().day
# one_year_ago = datetime.now() - timedelta(days=365)
# pb.posts.get(one_year_ago)

numOfYears = datetime.now().year - firstPostYear

year = datetime.now() - timedelta(days=365)

for x in range (0, numOfYears):
    pb.posts.get(year) # for some reason, year is being updated, but this always gets the post for current year
    print(year)
    year = year - timedelta(days=365)
