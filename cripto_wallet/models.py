import sqlite3
from cripto_wallet import app
import requests

apikey = '6FD88A14-4B8A-42A5-8884-EE08E9FDC460'
#apikey = app.config.get('COIN_IO_API_KEY')

def consult_to_apiio(form):
    coinFrom = form.coinFrom.data
    coinTo = form.coinTo.data
    url = f"https://rest.coinapi.io/v1/exchangerate/{coinFrom}/{coinTo}?apikey={apikey}"
    try: 
        consult_response = requests.get(url)
        data = consult_response.json() 
        if consult_response.status_code == 200:
            return True, data['rate'], consult_response.status_code, data['time']
        else:
            return False, data['error'], consult_response.status_code, consult_response.status_code      
    
    except requests.exceptions.RequestException as error_str:
        return False, str(error_str), url, url
            
def calcul_amount_you_get(form, data):
    amount = form.amount.data * data
    #Instanciamos una clase
    return amount









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


    def select_all(self):
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
    
    
    def insert(self, data_as_tuple):
        query = """
        INSERT INTO transactions
                (Date, Time, From_Coin, Amount_From, To_Coin, Amount_To)
                VALUES (?,?,?,?,?,?)
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        
        cur.execute(query, (data_as_tuple))
        conn.commit()
