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

### 2️⃣ Environment Variables

Create a `.env` file in the project root with the following variables:

```ini
PB_TOKEN=your_pinboard_api_token
MAILGUN_DOMAIN=your_mailgun_domain
MAILGUN_API_KEY=your_mailgun_api_key
TO_EMAIL=recipient@example.com
FROM_EMAIL=your_from_email@example.com
```

- `PB_TOKEN`: Pinboard API token (Get yours from [Pinboard Settings](https://pinboard.in/settings/password))
- `MAILGUN_DOMAIN`: Your Mailgun domain for sending emails
- `MAILGUN_API_KEY`: Mailgun API key
- `TO_EMAIL`: The recipient of the daily email
- `FROM_EMAIL`: The sender’s email

### 3️⃣ Running the Script

Execute the script manually:

```sh
python daily_pinboard.py
```

Or set up a cron job for daily execution:

```sh
0 8 * * * /usr/bin/python3 /path/to/daily_pinboard.py >> /path/to/logfile.log 2>&1
```

This runs the script every day at 8 AM.

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