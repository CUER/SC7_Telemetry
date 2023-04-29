# This file writes example dummy data to the database in a loop.

import os
import numpy as np
import pandas as pd
import time

import servicesqlite as serv

dir_path = os.path.dirname(os.path.realpath(__file__)) # path python file is located in. Which is DIFFERENT to current working directory (where the python file is being run from).

db = serv.DB(dir_path + "\\servicesqlite2.db")
print(db.show_tables())
dbf = pd.DataFrame(columns=["id", "timestamp", "car_speed", "temperature", "humidity"])

step=1
next_data = np.array([0,0,0,0])
while True:
    print(f"Writing {next_data}")
    db.write(next_data)
    a = np.random.randint(-step, step+1, size=4)
    a[0] = 1
    next_data += a
    time.sleep(0.01)