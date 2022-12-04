import pinboard
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import smtplib
from email.message import EmailMessage

# A special thank you to OpenAI's ChatGCP for the code assistance!

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

# Get current month and day as strings
current_date = datetime.now()
current_month = current_date.strftime('%B')
current_day = current_date.strftime('%d')

# Set up the email message
msg = EmailMessage()
msg['Subject'] = 'Pinboard Posts for ' + current_month + ' ' + current_day
msg['From'] = 'dann@dannberg.me'
msg['To'] = 'dann@dannb.org'

# Set email message body as content of datePosts array
# this doesn't work yet. datePosts is type `list`.
# Need to figure out how to add the year before each post, and then get all the text data out of the inner lists
email_body = ''
for inner_array in datePosts:
  email_body += '\n'.join(inner_array) + '\n'

# Set up the SMTP server and send the email
server = smtplib.SMTP('dannberg.me')
server.starttls()
server.login('dann@dannberg.me', 'glyiC)jac@vaSt%ul:')
server.send_message(msg)
server.quit()
