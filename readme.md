# Daily Pinboard

A python script that will send the user an email with a link to all their Pinboard bookmarks that were made on the date the script is run, in years past. Think, [TimeHop](https://www.timehop.com/) for [Pinboard](https://pinboard.in). If there were no links saved on that day, do not send an email.

I'm sure there are ways to optimize this code that are beyond my current skill level. If you discover any improvements, please let me know!

# Setup

## 1. Set Environmental variables
This code uses a `config.py` file in the same directory as the script that contains secrets. You'll want to set these secrets yourself if you're going to use this script:

| Config             | Description                                                                         |
|--------------------|-------------------------------------------------------------------------------------|
| PINBOARD_API_TOKEN | API Token from your Pinboard [Password page](https://pinboard.in/settings/password) |
| MSG_FROM           | Email address where the daily email should be sent from                             |
| MSG_TO             | Email address where you want the email sent                                         |
| SMTP_SERVER        | Your SMTP server address                                                            |
| SMTP_USERNAME      | Your SMTP server username                                                           |
| SMTP_PASS          | Your SMTP server password                                                           |
| FIRST_POST_YEAR    | The year in which you made your first Pinboard bookmark                             |

## 2. Set the script to run daily

You can do this with a cron job.

First, make sure `rundailypinboard.sh` and `daily-pinboard.py` are set as executable:

`chmod +x rundailypinboard.sh`
`chmod +x daily-pinboard.py`

Open your crontab file:

`crontab -e`

Then, add the following line to your crontab file:

`0 12 * * * /path/to/rundailypinboard.sh`

Make sure you replace `/path/to/rundailypinboard.sh` with the actual path to your rundailypinboard.sh script.

The cronjob code above runs the script daily at 7am ET. You can adjust that to your desired cadence and time.

---

## Links
- [Pinboard API](https://github.com/lionheart/pinboard.py)
- [Python datetime reference](https://stackoverflow.com/questions/5158160/python-get-datetime-for-3-years-ago-today)

## To Do
- [ ] improve the format of the email (make it pretty!)
- [ ] change API key and email password before making Repo public
- [x] successfully retrieve daily posts
- [x] test for when there are multiple results
- [x] save post to a variable, and retrieve name and content
- [x] figure out how to send via email (sendgrid?)
- [x] hide Pinboard API key
- [x] edit the code so that if the email is empty, it will not send

## Reference
the api returns this for a given date:

`{'date': datetime.datetime(2022, 6, 11, 21, 13, 49), 'user': 'dannberg', 'posts': [<Bookmark description="lionheart/pinboard.py: A full-featured Python wrapper (and command-line utility) for the Pinboard API. Built by the makers of Pushpin for Pinboard." url="github.com">]}`
