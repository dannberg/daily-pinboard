import pinboard
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

pb = pinboard.Pinboard('dannberg:351F526D563F33F2F9FC')

# Manually look to see what year you had your first Pinboard post
firstPostYear = 2012

numOfYears = datetime.now().year - firstPostYear + 1

year = datetime.now() - relativedelta(years=1)

datePosts = []

# Loops through today's date for each year of Pinboard posts, if a post exists, adds it to datePosts array
for x in range(0, numOfYears):
    searchDate = datetime.now() - relativedelta(years=x)
    dayBeforeSearchDate = searchDate - timedelta(days=1)
    post = pb.posts.all(start=0, results=20, fromdt=dayBeforeSearchDate, todt=searchDate)
    if post:
        datePosts.append(post)
