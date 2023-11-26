from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from neo_api_client import NeoAPI
from main.forms import LoginForm
from main.models import Order, db
from datetime import datetime
from main import app


ex_seg = {"NSE": "nse_cm", "BSE": "bse_cm", "NFO": "nse_fo", "BFO": "bse_fo", "CDS": "cde_fo", "MCX": "mcx_fo"}
client = None


@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def login():
    global client
    loginForm = LoginForm()
    if request.method == 'POST':
        if loginForm.validate_on_submit():
            # client = NeoAPI(consumer_key=loginForm.consumerKey.data,
            #                 consumer_secret=loginForm.consumerSecret.data, environment='prod')
            # client.login(mobilenumber=loginForm.mobileNumber.data, password=loginForm.password.data)
            # client.session_2fa(OTP=loginForm.mpin.data)
            db.create_all()

            client = 1
        else:
            flash(f'Please fill correct details!', category='danger')

        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', loginForm=loginForm)


@app.route('/dashboard')
def dashboard():
    global client

    if client:
        orders = Order.query.all()
        return render_template("dashboard.html", logs=orders)

    return redirect(url_for('login'))


@app.route('/webhook', methods=["GET", "POST"])
def webhook():
    global client, ex_seg
    if request.method == 'POST':
        if client:
            dictionary = request.json

            new_log = {
                "Time": datetime.now().time(),
                "ExchangeSegment": ex_seg[dictionary["exchange_segment"]],
                "Symbol": dictionary["trading_symbol"]+"EQ",
                "TransactionType": "B" if dictionary["transaction_type"] == "buy" else "S",
                "Quantity": dictionary["quantity"],
                "Price": dictionary["price"],
                "ProductType": dictionary["product_type"],
                "OrderType": dictionary["order_type"],
                "Validity": "DAY"
            }

            # orderdet = client.place_order(
            #     exchange_segment=new_log["ExchangeSegment"], product=new_log["ProductType"],
            #     order_type=new_log["OrderType"], quantity=new_log["Quantity"], validity=new_log["Validity"],
            #     trading_symbol=new_log["Symbol"], price=new_log['Price'], transaction_type=new_log["TransactionType"]
            # )
            orderdet = {"nOrdNo": dictionary["orderid"]}
            db.session.add(Order(
                orderID=orderdet["nOrdNo"], time=new_log["Time"], exgSegment=new_log["ExchangeSegment"],
                sym=new_log["Symbol"], transactionType=new_log["TransactionType"], qty=new_log["Quantity"],
                price=new_log["Price"], productType=new_log["ProductType"], orderType=new_log["OrderType"]
            ))
            db.session.commit()

            return "Order Executed Successfully"
        else:
            return "Please Login First"

    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    global client
    db.drop_all()
    client.logout()
    client = None
    return redirect(url_for('login'))
