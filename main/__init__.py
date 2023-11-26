from flask_sqlalchemy import SQLAlchemy
from flask import Flask

ex_seg = {"NSE": "nse_cm", "BSE": "bse_cm", "NFO": "nse_fo", "BFO": "bse_fo", "CDS": "cde_fo", "MCX": "mcx_fo"}
app = Flask(__name__, template_folder='Templates', static_folder='Static')
app.config['SECRET_KEY'] = "HelloCB"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)

from main import routes
