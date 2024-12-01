import os
import logging
import pinboard
import config
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import smtplib
from email.message import EmailMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pinboard_daily.log'),  # Log to file
        logging.StreamHandler()  # Also log to console
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Log start of script
        logger.info("Starting Pinboard daily email script")

        # Validate environment variables and config
        if not os.getenv("PINBOARD_API_TOKEN"):
            logger.error("PINBOARD_API_TOKEN environment variable is not set")
            return

        # Initialize Pinboard connection
        try:
            pb = pinboard.Pinboard(os.getenv("PINBOARD_API_TOKEN"))
            logger.info("Successfully connected to Pinboard")
        except Exception as e:
            logger.error(f"Failed to connect to Pinboard: {e}")
            return

        # Validate config
        required_config = ['FIRST_POST_YEAR', 'MSG_FROM', 'MSG_TO', 'SMTP_SERVER', 'SMTP_USERNAME']
        for cfg in required_config:
            if not hasattr(config, cfg):
                logger.error(f"Missing configuration: {cfg}")
                return

        # Calculate years of posts
        try:
            firstPostYear = int(config.FIRST_POST_YEAR)
            numOfYears = datetime.now().year - firstPostYear + 1
            logger.info(f"Searching for posts from {firstPostYear} to {datetime.now().year}")
        except ValueError:
            logger.error("Invalid FIRST_POST_YEAR in config")
            return

        # Collect posts
        email_body = ''
        for x in range(0, numOfYears):
            searchDate = datetime.now() - relativedelta(years=x)
            dayBeforeSearchDate = searchDate - timedelta(days=1)

            try:
                posts = pb.posts.all(start=0, results=20, fromdt=dayBeforeSearchDate, todt=searchDate)
                logger.info(f"Found {len(posts)} posts for {searchDate.year}")

                if posts:
                    year_str = str(searchDate.year)
                    email_body += f"Year: {year_str}\n"
                    for bookmark in posts:
                        description = bookmark.description
                        url = bookmark.url
                        email_body += f"{description}: {url}\n"
                    email_body += "\n\n"
            except Exception as e:
                logger.error(f"Error fetching posts for {searchDate.year}: {e}")

        # If no posts found, log and exit
        if not email_body:
            logger.info("No posts found for any year")
            return

        # Prepare email
        current_date = datetime.now()
        current_month = current_date.strftime('%B')
        current_day = current_date.strftime('%d')

        msg = EmailMessage()
        msg['Subject'] = f'Pinboard Posts for {current_month} {current_day}'
        msg['From'] = config.MSG_FROM
        msg['To'] = config.MSG_TO
        msg.set_content(email_body)

        # Send email
        try:
            with smtplib.SMTP(config.SMTP_SERVER) as server:
                server.starttls()

                # Log in with error handling
                try:
                    server.login(config.SMTP_USERNAME, os.getenv("SMTP_PASS"))
                except smtplib.SMTPAuthenticationError:
                    logger.error("SMTP Authentication failed. Check username and password.")
                    return

                # Send email
                server.send_message(msg)
                logger.info("Email sent successfully")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    except Exception as e:
        logger.error(f"Unexpected error in script: {e}")

if __name__ == "__main__":
    main()
