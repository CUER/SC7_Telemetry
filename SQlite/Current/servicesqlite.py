import sqlite3 as sl
import pandas as pd
import os

# Currently the code uses raw SQL queries. This leads to uglyness like converting numbers to strings and then back again.
# Should be changed to directly use Pandas' sqlite integration.

# Here the code is using con.execute() directly, however to make the code portable a 'cursor' should first be created and 
# the execute statement run on that cursor.

# NOTES
# to view all tables: con.execute('select name from sqlite_master where type in ("table", "view")').fetchall()
# to view all column names in table: con.execute("pragma table_info(<table>)").fetchall()

# use normal requests for SELECT and transactions for everything else

class DB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.table_name = "CARDATA"
        self.column_names = ["timestamp", "car_speed", "temperature", "humidity"] # magic variables I'm using as placeholder examples of columns

        # sql tables start from index 1
        self.last_read_new_idx = 1

        if not os.path.isfile(db_name):
            self.con = sl.connect(db_name, check_same_thread=get_sqlite3_thread_safety())
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
            self.con = sl.connect(db_name, check_same_thread=get_sqlite3_thread_safety())

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
        return data

    def read_new(self, select_columns="*"):
        with self.con:
            data = pd.read_sql_query(f"SELECT {','.join(select_columns)} FROM {self.table_name} WHERE id >= {self.last_read_new_idx}", self.con)
        self.last_read_new_idx += len(data)
        return data

    def write(self, data):
        with self.con:
            self.con.execute(f"INSERT INTO {self.table_name} ({','.join(self.column_names)}) values ({','.join([str(x) for x in data])})")

# If this returns True, it means sqlite is running thread-safe, meaning check_same_thread can be set to False when connecting to a database.
# If not, sqlite is not running thread-safe so will throw an error if it it accessed from a different thread.
# taken from https://ricardoanderegg.com/posts/python-sqlite-thread-safety/
def get_sqlite3_thread_safety():

    # Mape value from SQLite's THREADSAFE to Python's DBAPI 2.0
    # threadsafety attribute.
    sqlite_threadsafe2python_dbapi = {0: 0, 2: 1, 1: 3}
    conn = sl.connect(":memory:")
    threadsafety = conn.execute(
        """
select * from pragma_compile_options
where compile_options like 'THREADSAFE=%'
"""
    ).fetchone()[0]
    conn.close()

    threadsafety_value = int(threadsafety.split("=")[1])

    threadsafe = sqlite_threadsafe2python_dbapi[threadsafety_value]

    if threadsafe == 3:
        check_same_thread = False
    else:
        check_same_thread = True

    return check_same_thread