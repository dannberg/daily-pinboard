from dotenv import load_dotenv
import os
import pinboard
import config
import smtplib
import time
import socket
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from email.message import EmailMessage

# A special thank you to OpenAI's ChatGCP for the code assistance!

# Load .env file if it exists
if load_dotenv():
    print("Loaded environment variables from .env file")
else:
    print("No .env file found, using system environment variables")

# Get variables with fallbacks
pinboard_token = os.getenv('PINBOARD_API_TOKEN')
smtp_pass = os.getenv('SMTP_PASS')

if not pinboard_token or not smtp_pass:
    raise ValueError("Required environment variables are not set")

MAX_RETRIES = 10
RETRY_INTERVAL = 10

def wait_for_network():
    """Retries until the network is available."""
    for attempt in range(MAX_RETRIES):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            print(f"Network unavailable. Retry {attempt + 1}/{MAX_RETRIES} in {RETRY_INTERVAL} seconds...")
            time.sleep(RETRY_INTERVAL)
    print("Network still unavailable after multiple attempts. Exiting.")
    exit(1)

# Ensure network is available before running
wait_for_network()

pb = pinboard.Pinboard(pinboard_token)

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
            email_body += f"{description}: <a href=\"{url}\">{url}</a>\n"
        email_body += "\n\n"

# Get current month and day as strings
current_date = datetime.now()
current_month = current_date.strftime('%B')
current_day = current_date.strftime('%d')

# Read the email template
with open('email_template.html', 'r') as template_file:
    html_template = template_file.read()

# Format the email content with HTML
formatted_content = email_body.replace('\n', '<br>')
html_content = html_template.format(
    month=current_month,
    day=current_day,
    content=formatted_content
)

# Set up the email message
msg = EmailMessage()
msg['Subject'] = 'Pinboard Posts for ' + current_month + ' ' + current_day
msg['From'] = config.MSG_FROM
msg['To'] = config.MSG_TO

# Set both plain text and HTML versions
msg.set_content(email_body)  # Plain text version
msg.add_alternative(html_content, subtype='html')  # HTML version

# Attempt to send the email, retrying if necessary
for attempt in range(MAX_RETRIES):
    try:
        print(f"Attempting to connect to SMTP server ({attempt + 1}/{MAX_RETRIES})...")
        server = smtplib.SMTP(config.SMTP_SERVER, timeout=10)
        server.starttls()
        server.login(config.SMTP_USERNAME, smtp_pass)

        if len(email_body) > 0:
            server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
        break  # Exit loop if successful
    except (socket.gaierror, OSError, smtplib.SMTPException) as e:
        print(f"SMTP connection failed: {e}. Retrying in {RETRY_INTERVAL} seconds...")
        time.sleep(RETRY_INTERVAL)
else:
    print("Failed to send email after multiple attempts. Exiting.")
    exit(1)