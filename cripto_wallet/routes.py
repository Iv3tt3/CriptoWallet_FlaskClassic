from cripto_wallet import app
from flask import render_template, flash, request, redirect, url_for
from cripto_wallet.models import dao, calculs
from cripto_wallet.forms import SelectCoins

#Instanciamos el dao en models.py para evitar import cruzados


@app.route("/")
def index():
    try:
        transactions_list, empty_list = dao.get_all_transactions() 
        return render_template("index.html", page="Transactions", transactions=transactions_list, empty_list=empty_list, actual_page="index")
    except ValueError as e:
        flash("Problems with our data file")
        flash(str(e))
        empty_list = "Contact with your bank"
        return render_template("index.html",page="Transactions", transactions=[], empty_list=empty_list, actual_page="index")
    except Exception as e:
        flash(f"Fatal error {str(e)}")
        return render_template("fatalerror.html",page="Fatal Error", actual_page="index")


@app.route("/new_transaction", methods=["GET", "POST"])
def new_transaction():
    try:
        form = SelectCoins()
        if request.method == 'GET':
            return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new")
        else:
            if form.validate():
                if form.order_button.data:
                    form.submit_button.data = True
                    return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", calculs=calculs)
                elif form.purchase_button.data:
                    dao.insert_transaction(calculs)
                    calculs.reset()
                    return redirect(url_for("index"))
                elif form.cancel_button.data:
                    form.submit_button.data = True
                    return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", calculs=calculs)
                else:
                    try:
                        status, error_info = calculs.get_rate(form.coinFrom.data, form.coinTo.data, form.amount.data)
                        if status:
                            return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", calculs=calculs)
                        else:
                            flash(f"There is a problem with the query server, please try again later {error_info}")
                            return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", calculs=calculs)
                    except ValueError as e:
                        flash(f"There is a problem with the query server:{str(e)}")
                        return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", calculs=calculs)
            else:
                form.submit_button.data = False 
                return render_template("form_new.html",page="New transaction", form=form, actual_page="form_new", calculs=calculs)
    except Exception as e:
        flash(f"Fatal error {str(e)}")
        return render_template("fatalerror.html",page="Fatal Error", actual_page="form_new")

@app.route("/status")
def status():
    cripto_list, total_value, euros_invested, euros_refund, investment_result, empty_list = dao.get_wallet_balance()
    return render_template("status.html",page="Wallet status", 
                           actual_page="status", 
                           cripto_list=cripto_list, 
                           total_value=total_value, 
                           euros_invested=euros_invested, 
                           euros_refund=euros_refund, 
                           investment_result=investment_result,
                           empty_list=empty_list)