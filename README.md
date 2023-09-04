# gmail_most_common_emails
Script to collect most common email senderes from the gmail account. This can be used for sorting emails before deleting.

Tested on python 3.11.

## To run:

Make sure you have the `creadentials.json` file (follow this explanation - https://developers.google.com/gmail/api/quickstart/python).

1. Run setup first with `$ sh setup.sh`
2. Run script with `$ python main.py`

The resulting dict `sender_count` contains the senders and their counts.
