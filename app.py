from flask import Flask, render_template, request, redirect, url_for
from neo_api_client import NeoAPI
from flask_socketio import SocketIO
from datetime import datetime

ex_seg = {"NSE": "nse_cm", "BSE": "bse_cm", "NFO": "nse_fo", "BFO": "bse_fo", "CDS": "cde_fo", "MCX": "mcx_fo"}
app = Flask(__name__, template_folder='Templates', static_folder='Static')
socketio = SocketIO(app)
client = None


def on_message(message):
    print('[Res]: ', message)


def on_error(message):
    result = message
    print('[OnError]: ', result)


def on_open(message):
    print('[OnOpen]: ', message)


def on_close(message):
    print('[OnClose]: ', message)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global client

    mobilenumber = request.form.get('mobilenumber')
    consumer_key = request.form.get('consumer_key')
    consumer_secret = request.form.get('consumer_secret')
    passcode = request.form.get('passcode')
    mpin = request.form.get('mpin')

    # Initialize the NeoAPI client
    client = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, environment='prod')
    client.login(mobilenumber=f"+91{mobilenumber}", password=passcode)
    client.session_2fa(OTP=mpin)
    # Redirect to a new route after successful login
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    global client

    if client:
        return render_template("dashboard.html")

    return "Please login first."


@app.route('/logout')
def logout():
    global client
    client.logout()
    client = None
    return redirect(url_for('index'))


@app.route('/webhook', methods=["GET", "POST"])
def webhook():
    global client, ex_seg
    if client and request.method == 'POST':
        dictionary = request.json
        socketio.emit('new_log', f"{datetime.now().strftime('%H:%M:%S')} - "
                                 f'{"Bought" if dictionary["transaction_type"] == "buy" else "Sold"} '
                                 f'{dictionary["quantity"]} Quantity of {dictionary["trading_symbol"]} '
                                 f'@ {dictionary["price"]}')
        return client.place_order(exchange_segment=ex_seg[dictionary["exchange_segment"]], product="MIS",
                                  order_type="MKT", quantity=dictionary["quantity"], validity="DAY",
                                  trading_symbol=f"{dictionary['trading_symbol']}-EQ", price=dictionary['price'],
                                  transaction_type="B" if dictionary["transaction_type"] == 'buy' else "S")
    elif request.method == 'POST':
        return "Please Login First"
    else:
        return redirect(url_for("index"))


# if __name__ == '__main__':
#     app.run(debug=True)
