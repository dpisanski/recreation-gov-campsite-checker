import json
import random
import sys
import time
from twilio.rest import Client
from twilio.rest import Client as TwilioClient 

from hashlib import md5

from camping import SUCCESS_EMOJI

import twitter

MAX_TWEET_LENGTH = 279
DELAY_FILE_TEMPLATE = "next_{}.txt"
DELAY_TIME = 1800
CREDENTIALS_FILE = "twitter_credentials.json"


with open(CREDENTIALS_FILE) as f:
    tc = json.load(f)


def send_message(body):
    client = Client(tc["twilio_account_sid"], tc["twilio_auth_token"])
    message = client.messages.create(
            to=tc["twilio_to_number"], from_=tc["twilio_from_number"], body=body)
    print("The following was texted: ")
    print()
    print(body)


def create_tweet(tweet):
    tweet = tweet[:MAX_TWEET_LENGTH]
    api = twitter.Api(
        consumer_key=tc["consumer_key"],
        consumer_secret=tc["consumer_secret"],
        access_token_key=tc["access_token_key"],
        access_token_secret=tc["access_token_secret"],
    )
    resp = api.PostUpdate(tweet)
    # api.CreateFavorite(resp)
    print("The following was tweeted: ")
    print()
    print(tweet)

first_line = next(sys.stdin)
first_line_hash = md5(first_line.encode("utf-8")).hexdigest()

delay_file = DELAY_FILE_TEMPLATE.format(first_line_hash)
try:
    with open(delay_file, "r") as f:
        call_time = int(f.read().rstrip())
except:
    call_time = 0

if call_time + random.randint(DELAY_TIME-30, DELAY_TIME+30) > int(time.time()):
   print("It is too soon to tweet again") 
   sys.exit(0)


if "Something went wrong" in first_line:
    send_message("I'm broken! Please help :'(")
    sys.exit()


available_site_strings = []
for line in sys.stdin:
    line = line.strip()
    if SUCCESS_EMOJI in line:
        name = " ".join(line.split(":")[0].split(" ")[1:])
        available = line.split(":")[1][1].split(" ")[0]
        s = "{} site(s) available in {}".format(available, name)
        available_site_strings.append(s)

if available_site_strings:
    tweet = "Hey!!!"
    tweet += first_line.rstrip()
    tweet += " 🏕🏕🏕\n"
    tweet += "\n".join(available_site_strings)
    tweet += "\n" + "🏕" * random.randint(5, 20)  # To avoid duplicate tweets.
    send_message(tweet)
    with open(delay_file, "w") as f:
        f.write(str(int(time.time())))
    sys.exit(0)
else:
    print("No campsites available, not tweeting 😞")
    sys.exit(1)
