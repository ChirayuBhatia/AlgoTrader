from flask import Flask, render_template, request, redirect, url_for
from neo_api_client import NeoAPI

app = Flask(__name__)
client = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    global client

    consumer_key = request.form.get('consumer_key')
    consumer_secret = request.form.get('consumer_secret')
    passcode = request.form.get('passcode')
    mpin = request.form.get('mpin')

    # Initialize the NeoAPI client
    client = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, environment='prod')
    client.login(mobilenumber="+917987123695", password=passcode)
    client.session_2fa(OTP=mpin)
    # Redirect to a new route after successful login
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    global client

    if client:
        return "Logged in successfully!"

    return "Please login first."


@app.route('/webhook', methods=["POST"])
def webhook():
    global client
    if client and request.method == 'POST':
        dictionary = request.json
        print(dictionary)
        return request.json
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
