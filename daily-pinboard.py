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

pb = pinboard.Pinboard(os.getenv("PINBOARD_API_TOKEN"))

# Add debug section after creating the Pinboard client
token = os.getenv("PINBOARD_API_TOKEN")
masked_token = token[:4] + "..." + token[-4:] if token else "None"
print(f"Using Pinboard API token: {masked_token}")

# Test basic API connectivity
print("Testing API connection with recent posts...")
recent_posts = pb.posts.recent(count=1)
print(f"Recent posts test: {recent_posts}")

# Manually look to see what year you had your first Pinboard post
firstPostYear = int(config.FIRST_POST_YEAR)

numOfYears = datetime.now().year - firstPostYear + 1
year = datetime.now() - relativedelta(years=1)

datePosts = []
email_body = []

# Get current month and day
current_date = datetime.now()
current_month = current_date.strftime('%m')  # Use %m for 2-digit month
current_day = current_date.strftime('%d')

# Modify the search loop
for x in range(0, numOfYears):
    year = datetime.now().year - x
    formatted_date = f"{year}-{current_month}-{current_day}"  # Format: YYYY-MM-DD
    print(f"\nSearching for posts on {formatted_date}")
    try:
        post = pb.posts.all(dt=formatted_date)
        print(f"API Response: {post}")
        print(f"Found {len(post)} posts for year {year}")
        if post:
            year_data = {
                'year': str(year),
                'bookmarks': [(b.description, b.url) for b in post]
            }
            email_body.append(year_data)
    except Exception as e:
        print(f"Error querying for date {formatted_date}: {str(e)}")

# Read the email template
with open('email_template.html', 'r') as template_file:
    html_template = template_file.read()

# Build the years content string
years_content = ''
for year_data in email_body:
    years_content += f'<h2>Year: {year_data["year"]}</h2>\n<ul>\n'
    for description, url in year_data['bookmarks']:
        years_content += f'<li>{description}: <a href="{url}">{url}</a></li>\n'
    years_content += '</ul>\n\n'

# Add debug logging
print(f"Found {len(email_body)} years with posts")
if len(email_body) == 0:
    print("No posts found for any year on this date")
    exit(0)

# Format the email content
html_content = html_template.format(
    month=current_month,
    day=current_day,
    years_content=years_content
)

# Set up the email message
msg = EmailMessage()
msg['Subject'] = 'Pinboard Posts for ' + current_month + ' ' + current_day
msg['From'] = config.MSG_FROM
msg['To'] = config.MSG_TO

# Set both plain text and HTML versions
plain_text = f"Pinboard Posts for {current_month} {current_day}\n\n"
for year_data in email_body:
    plain_text += f"Year: {year_data['year']}\n"
    for description, url in year_data['bookmarks']:
        plain_text += f"{description}: {url}\n"
    plain_text += "\n"

msg.set_content(plain_text)  # Plain text version
msg.add_alternative(html_content, subtype='html')  # HTML version

# Attempt to send the email, retrying if necessary
for attempt in range(MAX_RETRIES):
    try:
        print(f"Attempting to connect to SMTP server ({attempt + 1}/{MAX_RETRIES})...")
        server = smtplib.SMTP(config.SMTP_SERVER, timeout=10)
        server.set_debuglevel(1)  # Add debug logging for SMTP
        server.starttls()
        server.login(config.SMTP_USERNAME, os.getenv("SMTP_PASS"))

        print(f"Sending email to: {config.MSG_TO}")
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
        break
    except (socket.gaierror, OSError, smtplib.SMTPException) as e:
        print(f"SMTP connection failed: {e}. Retrying in {RETRY_INTERVAL} seconds...")
        if hasattr(e, 'smtp_error'):
            print(f"SMTP Error: {e.smtp_error}")
        time.sleep(RETRY_INTERVAL)
else:
    print("Failed to send email after multiple attempts. Exiting.")
    exit(1)
