from cripto_wallet import app

@app.route("/")
def index():
    return "Flask basic"