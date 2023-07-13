import sqlite3
from cripto_wallet import app
import requests
from datetime import datetime


class Calculs:
    def __init__(self):
        self.coinFrom = ""
        self.coinTo = ""
        self.rate = ""
        self.amountFrom = ""
        self.amountTo = ""
    
    def get_rate(self, form):
        coinFrom = form.coinFrom.data
        coinTo = form.coinTo.data
        apikey = app.config.get("COIN_IO_API_KEY")
        url = f"https://rest.coinapi.io/v1/exchangerate/{coinFrom}/{coinTo}?apikey={apikey}"
        try: 
            consult_response = requests.get(url)
            data = consult_response.json() 
            if consult_response.status_code == 200:
                self.rate = (data['rate'])
                self.coinFrom = coinFrom
                self.coinTo = coinTo
                self.time = data['time']
                self.amountFrom = form.amount.data
                self.amountTo = form.amount.data * self.rate
                return True, None
            else:
                return False, str(consult_response.status_code) + data['error']    
        
        except requests.exceptions.RequestException as error_str:
            return False, error_str + url
    
    def reset(self):
        self.coinFrom = self.coinTo = self.rate = self.amountFrom = self.amountTo = ""


class DAOSqlite:
    def __init__(self, data_path):
        self.path = data_path
        query = """
        CREATE TABLE IF NOT EXISTS "transactions" (
            "Id"	INTEGER,
            "Date"	TEXT NOT NULL,
            "Time"	TEXT NOT NULL,
            "From_Coin"	TEXT NOT NULL,
            "Amount_From"	REAL NOT NULL,
            "To_Coin"	TEXT NOT NULL,
            "Amount_To"	REAL NOT NULL,
            PRIMARY KEY("Id" AUTOINCREMENT)
        );
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        conn.close()


    def display_transactions(self):
        query = """
        SELECT Date, Time, From_Coin, Amount_From, To_Coin, Amount_To
        FROM transactions
        ORDER by date
        ;"""
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        transactions_list = cur.fetchall()
        empty_list=None
        if len(transactions_list) == 0:
            empty_list="No existen movimientos"
        return transactions_list,empty_list
        
        #Para probar el mensaje de error si esta corrupta la bd:
        #raise ValueError 

         ## FALTARIA COMPROBAR QUE LOS DATOS DE LA BD SON CORRECTOS y en caso que no #raise ValueError
    
    
    def insert_transaction(self, calculs):
        time_now = datetime.utcnow().isoformat()
        date = time_now[0:10]
        time = time_now[11:19]
        query = """
        INSERT INTO transactions
                (Date, Time, From_Coin, Amount_From, To_Coin, Amount_To)
                VALUES (?,?,?,?,?,?)
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        
        cur.execute(query, (date, time, calculs.coinFrom, calculs.amountFrom, calculs.coinTo, calculs.amountTo))
        conn.commit()

    def get_coin_in_wallet(self, coinFrom):
        query = """
        SELECT id, Amount_From
        FROM transactions
        where To_Coin = ?
        ORDER by date
        ;"""
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (coinFrom, ))
        list = cur.fetchall()
        conn.close()
        amount = 0
        for item in list:
            amount += item[1]
        return float(amount)
    

dao = DAOSqlite(app.config.get("PATH_SQLITE"))
calculs = Calculs()