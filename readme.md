# Daily Pinboard

A work-in-process application that will send the user an email every day with a link to all the pinboard bookmarks that were made on the same day in years past. Think, [TimeHop](https://www.timehop.com/) for [Pinboard](https://pinboard.in). If there were no links saved on that day, do not send an email.

---

## Links
- [Pinboard API](https://github.com/lionheart/pinboard.py)
- [Python datetime reference](https://stackoverflow.com/questions/5158160/python-get-datetime-for-3-years-ago-today)
- [Sendgrid Python Reference](https://github.com/sendgrid/sendgrid-python) - service for sending emails

## To Do
- [ ] test for when there are multiple resules
- [ ] save post to a variable, and retrieve name and content
- [ ] figure out how to send via email (sendgrid?)

## Reference
the api returns this for a given date:

`{'date': datetime.datetime(2022, 6, 11, 21, 13, 49), 'user': 'dannberg', 'posts': [<Bookmark description="lionheart/pinboard.py: A full-featured Python wrapper (and command-line utility) for the Pinboard API. Built by the makers of Pushpin for Pinboard." url="github.com">]}`
