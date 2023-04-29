# This file connects over serial to the radio module and receives data continuously.

import serial
import os
import servicesqlite as serv
import struct
import datetime, time
 
arduino = serial.Serial(
    port='COM8',
    baudrate = 9600,
    # parity=serial.PARITY_NONE,
    # stopbits=serial.STOPBITS_ONE,
    # bytesize=serial.EIGHTBITS,
    timeout=1
)

dir_path = os.path.dirname(os.path.realpath(__file__)) # path python file is located in. Which is DIFFERENT to current working directory (where the python file is being run from).
db_path = dir_path + "\\servicesqlite2.db"
db = serv.DB(dir_path + "\\servicesqlite2.db")

# RECEIVE FORMAT: 4-byte float: timestamp, 3x placeholder values. Terminate with EOL byte.

data_list = []
print(f"Listening on port {arduino.port} at {arduino.baudrate} baud")
# START sequence ensures sender and receiver are synchronised
print(f"Waiting for START sequence...")
while True:
    x = arduino.read(1)
    data_list += list(x)

    if data_list[-5:] == list(bytearray(b"START")):
        break

# the number of floats received each time
n_recv = 6

print(f"Start sequence received. Receiving data...")
while True:
    if arduino.in_waiting >= n_recv*4: # *4 because 4 bytes in a float
        x = arduino.read(n_recv*4)
        data = struct.unpack(f"{n_recv}f", x)
        # Converts first 3 bytes of data (hours, minutes, seconds) to UNIX time. Will need to record current day and year.
        # WSC regulations require us to send them timestamps in UNIX time.
        date_time = int(time.mktime(datetime.datetime(2023, 3, 4, int(data[0]), int(data[1]), int(data[2])).timetuple()))

        data = [date_time] + list(data[3:])
        print(data)
        db.write(data)