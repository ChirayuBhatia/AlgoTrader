from main import db


class Order(db.Model):
    orderID = db.Column(db.String(), nullable=False, primary_key=True)
    time = db.Column(db.Time(), nullable=False)
    exgSegment = db.Column(db.String(length=3), nullable=False)
    sym = db.Column(db.String(length=20), nullable=False)
    transactionType = db.Column(db.String(length=1), nullable=False)
    qty = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    productType = db.Column(db.String(length=3), nullable=False)
    orderType = db.Column(db.String(length=3), nullable=False)
