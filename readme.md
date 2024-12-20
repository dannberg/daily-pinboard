# Daily Pinboard

A python script that will send the user an email with a link to all their Pinboard bookmarks that were made on the date the script is run, in years past. Think, [TimeHop](https://www.timehop.com/) for [Pinboard](https://pinboard.in). If there were no links saved on that day, do not send an email.

I'm sure there are ways to optimize this code that are beyond my current skill level. If you discover any improvements, please let me know!

# Setup

## 1. Install dependencies

If you haven't yet, make sure you install [pinboard.py](https://github.com/lionheart/pinboard.py):

`pip3 install "pinboard>=2.0"`

You may also need `dateutil`:

`pip3 install python-dateutil`

If you're missing anything else, you should get an error when you try and run the script saying something to the effect of: `ModuleNotFoundError: No module named '[module name]]'`. That means you need to install that module.

## 2. Set Environmental variables
This code uses a `config.py` file in the same directory as the script, which contains your secrets.

To use this, rename `config-example.py` to `config.py` and update all the variables:

| Config             | Description                                                                         |
|--------------------|-------------------------------------------------------------------------------------|
| MSG_FROM           | Email address where the daily email should be sent from                             |
| MSG_TO             | Email address where you want the email sent                                         |
| SMTP_SERVER        | Your SMTP server address                                                            |
| SMTP_USERNAME      | Your SMTP server username                                                           |
| FIRST_POST_YEAR    | The year in which you made your first Pinboard bookmark                             |

Also, add your Pinboard API token (from your [Pinboard password page](https://pinboard.in/settings/password)) and SMTP passwords as environmental variables (`/etc/environment`):

- `PINBOARD_API_TOKEN`
- `SMTP_PASS`

## 3. Set the script to run daily

You can do this with a cron job.

First, make sure `rundailypinboard.sh` and `daily-pinboard.py` are set as executable:

`chmod +x rundailypinboard.sh`
`chmod +x daily-pinboard.py`

Open your crontab file:

`crontab -e`

Then, add the following line to your crontab file:

`0 7 * * * /path/to/rundailypinboard.sh >> /home/dannberg/daily-pinboard/logs.txt 2>&1`

Make sure you replace `/path/to/rundailypinboard.sh` with the actual path to your rundailypinboard.sh script.

The cronjob code above runs the script daily at 7am ET (my server's set timezone). You can [adjust that](https://crontab.guru/#0_7_*_*_*) to your desired cadence and time. Logs are saved to a logs.txt file, which is ignored by this Github repo.

---

## Links
- [Pinboard API](https://github.com/lionheart/pinboard.py)
- [Python datetime reference](https://stackoverflow.com/questions/5158160/python-get-datetime-for-3-years-ago-today)

## To Do
- [ ] improve the format of the email (make it pretty!)
- [x] change API key and email password before making Repo public
- [x] successfully retrieve daily posts
- [x] test for when there are multiple results
- [x] save post to a variable, and retrieve name and content
- [x] figure out how to send via email (sendgrid?)
- [x] hide Pinboard API key
- [x] edit the code so that if the email is empty, it will not send

## Reference
the api returns this for a given date:

`{'date': datetime.datetime(2022, 6, 11, 21, 13, 49), 'user': 'dannberg', 'posts': [<Bookmark description="lionheart/pinboard.py: A full-featured Python wrapper (and command-line utility) for the Pinboard API. Built by the makers of Pushpin for Pinboard." url="github.com">]}`

# Thanks!
A special thank you to OpenAI's [ChatGPT](https://chat.openai.com/chat) for the code help! Damn, that tool is nifty.
