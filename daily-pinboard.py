import os
import pinboard
import config
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import smtplib
from email.message import EmailMessage

# A special thank you to OpenAI's ChatGCP for the code assistance!

pb = pinboard.Pinboard(os.getenv("PINBOARD_API_TOKEN"))

# Manually look to see what year you had your first Pinboard post
firstPostYear = int(config.FIRST_POST_YEAR)

numOfYears = datetime.now().year - firstPostYear + 1

year = datetime.now() - relativedelta(years=1)

datePosts = []
email_body = ''

# Loops through today's date for each year of Pinboard posts, if a post exists, adds it to datePosts array
for x in range(0, numOfYears):
    searchDate = datetime.now() - relativedelta(years=x)
    dayBeforeSearchDate = searchDate - timedelta(days=1)
    post = pb.posts.all(start=0, results=20, fromdt=dayBeforeSearchDate, todt=searchDate)
    if post:
        year_str = str(searchDate.year)
        email_body += f"Year: {year_str}\n"
        for bookmark in post:
            description = bookmark.description
            url = bookmark.url
            email_body += f"{description}: {url}\n"
        email_body += "\n\n"

# Get current month and day as strings
current_date = datetime.now()
current_month = current_date.strftime('%B')
current_day = current_date.strftime('%d')

# Set up the email message
msg = EmailMessage()
msg['Subject'] = 'Pinboard Posts for ' + current_month + ' ' + current_day
msg['From'] = config.MSG_FROM
msg['To'] = config.MSG_TO

# Set email message body as content of datePosts array
msg.set_content(email_body)

# Set up the SMTP server and send the email
server = smtplib.SMTP(config.SMTP_SERVER)
server.starttls()
server.login(config.SMTP_USERNAME, os.getenv("SMTP_PASS"))
if len(email_body) > 0:
    server.send_message(msg)
server.quit()
