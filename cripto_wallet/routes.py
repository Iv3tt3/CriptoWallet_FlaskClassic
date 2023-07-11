from cripto_wallet import app
from flask import render_template, flash
from cripto_wallet.models import DAOSqlite

dao = DAOSqlite(app.config.get("PATH_SQLITE"))

@app.route("/")
def index():
    try:
        transactions_list, empty_list = dao.select_all() 
        return render_template("index.html", page="Transactions", transactions=transactions_list, empty_list=empty_list, actual_page="index")
    except ValueError as e:
        flash("Hay un problema en la base de datos")
        flash(str(e))
        empty_list = "Consulte con su banco"
        return render_template("index.html",page="Transactions", transactions=[], empty_list=empty_list, actual_page="index")