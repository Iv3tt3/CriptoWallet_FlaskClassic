from cripto_wallet import app
from flask import render_template, flash, request
from cripto_wallet.models import DAOSqlite
from cripto_wallet.forms import SelectCoins
from cripto_wallet.models import consult_to_apiio, calcul_amount_you_get

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
    

@app.route("/new_transaction", methods=["GET", "POST"])
def new_transaction():
    form = SelectCoins()
    rate = "To calculate"
    amount_youGet = "To calculate"
    if request.method == 'GET':
        return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", amount_youGet=amount_youGet)
    else:
        if form.validate():
            try:
                status, data, code, time = consult_to_apiio(form)
                if status:
                    amount_youGet = calcul_amount_you_get(form, data)
                    return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", rate=data, amount_youGet=amount_youGet)
                else:
                    flash(f"Hay un problema en el servidor de consultas: {data}")
                    return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", rate=data, amount_youGet=amount_youGet)
            except ValueError as e:
                flash("Hay un problema con el servidor de consultas:")
                flash(str(e))
                return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", rate=rate, amount_youGet=amount_youGet)
        else:
            return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", rate=rate, amount_youGet=amount_youGet)

@app.route("/status")
def status():
    return render_template("status.html",page="Wallet status", actual_page="status")