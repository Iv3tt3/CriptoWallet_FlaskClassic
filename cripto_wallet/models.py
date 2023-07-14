import sqlite3
from cripto_wallet import app
import requests
from datetime import datetime

coins = [("option","Select an option"),
         ("EUR","EUR"),
         ("BTC","BTC"), 
         ("BNB","BNB"),
         ("ETH","ETH"),
         ("USDT","USDT"),
         ("XRP","XRP"),
         ("ADA","ADA"),
         ("SOL","SOL"),
         ("DOT","DOT"),
         ("MATIC","MATIC")]

wallet_criptos = []
for value, coin in coins:
    if value != "option" and coin != "EUR":
        wallet_criptos.append(coin)


class Calculs:
    def __init__(self):
        self.coinFrom = ""
        self.coinTo = ""
        self.rate = ""
        self.amountFrom = ""
        self.amountTo = ""
    
    def get_rate(self, coinFrom, coinTo, amount):
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
                self.amountFrom = amount
                self.amountTo = float(amount) * float(self.rate)
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
        self.create_table_init()

    def create_table_init(self):    
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


    def get_all_transactions(self):
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
            empty_list="No transactions to display"
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

    def get_coin_amount(self, coinFrom):
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
    
    def get_wallet_balance2(self):
        balance_list = []
        for item in wallet_criptos:
            amount = self.get_coin_amount(item)
            if amount != 0:
                calculs.get_rate(item,"EUR",amount)
                value = calculs.rate * amount
                balance_list.append((item, amount, value))
        return balance_list
    
    def get_wallet_balance(self):
        transactions, empty_list = self.get_all_transactions()
        if len(transactions) == 0:
            empty_list = "Your wallet is empty"
        else:
            euros_invested, euros_refund, investment_result = self.calcul_investment(transactions)
            total_value = 0
            cripto_list = []
            for cripto in wallet_criptos:
                cripto_amount = 0
                cripto_value = 0
                for transaction in transactions:

                    From_Coin = transaction[2]
                    Amount_From = transaction[3]
                    To_Coin = transaction[4]
                    Amount_To = transaction[5]

                    if From_Coin == cripto:
                        cripto_amount -= Amount_From
                    if To_Coin == cripto:
                        cripto_amount += Amount_To

                if cripto_amount !=0:
                    calculs.get_rate(cripto,"EUR",cripto_amount)
                    cripto_value = calculs.rate * cripto_amount
                    total_value += cripto_value
                    cripto_list.append((cripto, cripto_amount, cripto_value)) 
            
        return cripto_list, total_value, euros_invested, euros_refund, investment_result, empty_list
                    
    
    def calcul_investment(self, transactions):
        euros_invested = 0
        euros_refund = 0
        for transaction in transactions:
            From_Coin = transaction[2]
            Amount_From = transaction[3]
            To_Coin = transaction[4]
            Amount_To = transaction[5]

            if From_Coin == "EUR":
                euros_invested -= Amount_From
            if To_Coin == "EUR":
                euros_refund += Amount_To
        investment_result = euros_refund - euros_invested
        return euros_invested, euros_refund, investment_result


        
    

dao = DAOSqlite(app.config.get("PATH_SQLITE"))
calculs = Calculs()