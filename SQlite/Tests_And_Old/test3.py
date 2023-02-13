import sqlite3 as sl
import pandas as pd
import os
import numpy as np

# Currently the code uses raw SQL queries. This leads to uglyness like converting numbers to strings and then back again.
# Should be changed to directly use Pandas' sqlite integration.

# Here the code is using con.execute() directly, however to make the code portable a 'cursor' should first be created and 
# the execute statement run on that cursor.

# NOTES
# to view all tables: con.execute('select name from sqlite_master where type in ("table", "view")').fetchall()
# to view all column names in table: con.execute("pragma table_info(<table>)").fetchall()

# use normal requests for SELECT and transactions for everything else

def get_random_walk(n, step=1, start=0):
    ret = []
    for i in range(n):
        ret.append(start)
        start += np.random.randint(-step, step+1)
    
    return np.array(ret)

# example. each item is a float. this includes the timestamp.
n=100
sample_timestamp = np.linspace(0, 10, n)
sample_carspeed = get_random_walk(n)
sample_temperature = get_random_walk(n)
sample_humidity = get_random_walk(n)

sample_matrix = np.array([sample_timestamp, sample_carspeed, sample_temperature, sample_humidity]).T

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
        print(self.con.execute('select name from sqlite_master where type in ("table", "view")').fetchall())

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
for i in sample_matrix:
    db.write(i)
db.show_tables()
a = db.get_dataframe()
print(a)

# db.write_table(1,1,1)
# db.read_table(1,1,1)