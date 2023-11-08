from flask import Flask, render_template, request, redirect, url_for
from neo_api_client import NeoAPI

ex_seg = {"NSE": "nse_cm", "BSE": "bse_cm", "NFO": "nse_fo", "BFO": "bse_fo", "CDS": "cde_fo", "MCX": "mcx_fo"}
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


@app.route('/webhook', methods=["GET", "POST"])
def webhook():
    global client, ex_seg
    print(client)
    if client and request.method == 'POST':
        dictionary = request.json
        return client.place_order(exchange_segment=ex_seg[dictionary["exchange_segment"]], product="NRML",
                                  order_type="MKT", quantity=dictionary["quantity"], validity="DAY",
                                  trading_symbol=f"{dictionary['trading_symbol']}-EQ",
                                  transaction_type="B" if dictionary["transaction_type"] == 'buy' else "S")

    else:
        return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
