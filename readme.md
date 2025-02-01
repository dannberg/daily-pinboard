# **Daily Pinboard**

📌 **Receive a daily email with all your past Pinboard bookmarks from this date in history. Like TimeHop, but for Pinboard.**

![GitHub](https://img.shields.io/github/license/dannberg/daily-pinboard?cacheSeconds=60)
![Python](https://img.shields.io/badge/Python-Script-blue)
![Pinboard](https://img.shields.io/badge/Pinboard-Integration-orange)

## 📖 Overview

Daily Pinboard is a Python script that emails you a list of all your Pinboard bookmarks made on this day in previous years. If no bookmarks exist for that date, no email is sent. This is a great way to rediscover old saved links over time.

---

## 🚀 **Setup**

### 1️⃣ Install Dependencies

Ensure you have the required Python packages installed.

```sh
pip install -r requirements.txt
```

### 2️⃣ Config and Environment Variables

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

```ini
PINBOARD_API_TOKEN=your_pinboard_api_token
SMTP_PASS=your_smtp_password
```

- `PINBOARD_API_TOKEN`: Pinboard API token (Get yours from [Pinboard Settings](https://pinboard.in/settings/password))
- `SMTP_PASS`: Your SMTP server password

**TIP:** *(optional)* If you want a simple and inexpensive way to forward and send emails with your domains, I've been a happy customer of [ForwardedEmail.net](https://forwardedemail.net) for a while now. This is not an ad, just a personal recommendation.


### 3️⃣ Running the Script

Execute the script manually:

```sh
python daily_pinboard.py
```

Or set up a cron job for daily execution:

1. Make the scripts executable:

```sh
chmod +x rundailypinboard.sh
chmod +x daily-pinboard.py
```

2. Open your crontab file:

```sh
crontab -e
```

3. Add the following line:

```sh
0 7 * * * /path/to/rundailypinboard.sh >> /path/to/daily-pinboard/logs.txt 2>&1
```

**Note:** Replace both `/path/to/` with the actual paths to your script and logs.txt file.

The cron job will run daily at 7 AM (server timezone). You can [adjust the schedule](https://crontab.guru/#0_7_*_*_*) to your preferred time. Logs are saved to `logs.txt`, which is ignored by this repository.

---

## 🤝 Contributing

If you have improvements or optimizations, feel free to submit a pull request!

Similarly, if you have any problems or bugs to report, please file an [issue](https://github.com/dannberg/daily-pinboard/issues).

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

## 📝 TODO

Curious about what I plan to do next? Here's the plan:

- [ ] Switch to Mailgun for email delivery
- [ ] Update code so email html is in separate file
- [ ] Use [beefree.io](https://beefree.io) to design better email