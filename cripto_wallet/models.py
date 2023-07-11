import sqlite3

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
