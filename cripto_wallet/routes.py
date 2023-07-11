from cripto_wallet import app
from flask import render_template
from cripto_wallet.models import DAOSqlite

dao = DAOSqlite(app.config.get("PATH_SQLITE"))

@app.route("/")
def index():
    transactions_list = dao.select_all()
    return render_template("index.html", page="Transactions", transactions=transactions_list)