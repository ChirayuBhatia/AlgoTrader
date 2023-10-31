import pandas as pd
from neo_api_client import NeoAPI
from datetime import datetime, timedelta

# Credentials
consumer_key = "Xr32ear8vsfVF9aaFKEz_lNWAYga"
consumer_secret = "8VeA6prk8hmlQHuQkjDBzMgrI5Ma"

user_id = "YTOZC"
password = "@cB21s02"

mobileNumber = "+917987123695"


def on_message(message):
    print('[Res]: ', message)


def on_error(message):
    result = message
    print('[OnError]: ', result)


def on_open(message):
    print('[OnOpen]: ', message)


def on_close(message):
    print('[OnClose]: ', message)


client = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, environment='prod')
client.login(mobilenumber=mobileNumber, password=password)
otp = input("Please enter the OTP: ")
client.session_2fa(OTP=otp)
inst_tokens = [{"instrument_token": "52431", "exchange_segment": "nse_fo"},
               {"instrument_token": "52432", "exchange_segment": "nse_fo"},
               {"instrument_token": "52433", "exchange_segment": "nse_fo"},
               {"instrument_token": "52706", "exchange_segment": "nse_fo"}]

a = client.subscribe(instrument_tokens=inst_tokens)
print(a)

