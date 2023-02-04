import sqlite3 as sl
import pandas as pd
import os

# Here the code is using con.execute() directly, however to make the code portable a 'cursor' should first be created and 
# the execute statement run on that cursor.

# NOTES
# to view all tables: con.execute('select name from sqlite_master where type in ("table", "view")').fetchall()
# to view all column names in table: con.execute("pragma table_info(<table>)").fetchall()

# use normal requests for SELECT and transactions for everything else

# example. each item is a float. this includes the timestamp.
data = [1,2,3,4]

class DB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.table_name = "CARDATA"
        self.column_names = ["timestamp", "car_speed", "temperature", "humidity"] # magic variables I'm using as placeholder examples of columns

        if not os.path.isfile(db_name):
            self.con = sl.connect(db_name)
            # create blank database if none exists
            with self.con:
                print(f"No database with name {db_name} was found! Creating new blank database.")
                data = ",".join(f"{i} FLOAT" for i in self.column_names)
                with self.con:
                    self.con.execute(f"""
                        CREATE TABLE {self.table_name} (
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            {data}
                        );
                    """)
        else:
            self.con = sl.connect(db_name)

    def show_tables(self):
        print(db.con.execute('select name from sqlite_master where type in ("table", "view")').fetchall())

    def get_dataframe(self):
        return pd.read_sql_query(f"SELECT * FROM {self.table_name}", self.con)

    def read(self, select_columns="*", where=""):
        with self.con:
            if where:
                data = self.con.execute(f"SELECT {','.join(select_columns)} FROM {self.table_name} WHERE {where}")
            else:
                print(f"SELECT {','.join(select_columns)} FROM {self.table_name}")
                data = self.con.execute(f"SELECT {','.join(select_columns)} FROM {self.table_name}")
            for row in data:
                print(row)

    def write(self, data):
        with self.con:
            self.con.execute(f"INSERT INTO {self.table_name} ({','.join(self.column_names)}) values ({','.join([str(x) for x in data])})")

dir_path = os.path.dirname(os.path.realpath(__file__)) # path python file is located in. Which is DIFFERENT to current working directory (where the python file is being run from).
db = DB(dir_path + "\\test3.db")
# db.write(data)
# db.write(data)
# db.write(data)
db.show_tables()
a = db.get_dataframe()
print(a)

# db.write_table(1,1,1)
# db.read_table(1,1,1)