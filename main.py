from flask import Flask, request, render_template
from neo_api_client import NeoAPI

app = Flask(__name__)


def on_message(message):
    print('[Res]: ', message)


def on_error(message):
    result = message
    print('[OnError]: ', result)


def on_open(message):
    print('[OnOpen]: ', message)


def on_close(message):
    print('[OnClose]: ', message)


client = NeoAPI(consumer_key="Xr32ear8vsfVF9aaFKEz_lNWAYga", consumer_secret="8VeA6prk8hmlQHuQkjDBzMgrI5Ma",
                environment='prod')
client.login(mobilenumber="+917987123695", password="@cB21s02")
client.session_2fa(OTP="053130")


def authenticate_and_get_api_data():
    return {'username': 'john_doe', 'email': 'john@example.com'}


@app.route("/")
def hello():
    return "You have successfully logged in"


@app.route("/webhook", methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(client)
        print('Webhook Received')
        request_json = request.json
        print('Payload: ', request_json['message'])
        return 'POST Message Received', 202
    else:
        return 'POST Method not supported', 405


if __name__ == "__main__":
    app.run(debug=True)
