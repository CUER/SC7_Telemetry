# This file connects over serial to the radio module and receives data continuously.

import serial
import os
import servicesqlite as serv
 
arduino = serial.Serial(
    port='COM8',
    baudrate = 9600,
    # parity=serial.PARITY_NONE,
    # stopbits=serial.STOPBITS_ONE,
    # bytesize=serial.EIGHTBITS,
    timeout=1
)

dir_path = os.path.dirname(os.path.realpath(__file__)) # path python file is located in. Which is DIFFERENT to current working directory (where the python file is being run from).
db_path = dir_path + "\\servicesqlite.db"
db = serv.DB(dir_path + "\\servicesqlite.db")
    
print(f"hhListening on port {arduino.port} at {arduino.baudrate} baud...")
while True:
    x = arduino.readline()

    if x:
        try:
            x = x.decode().split(",")
            y=[]
            for item in x:
                y.append(float(item))

            # print(y)
            if len(y) == 4:
                db.write(y)
            else:
                print("Error: Could not write data. Data is of wrong length")
        except:
            pass