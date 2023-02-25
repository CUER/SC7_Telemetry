import serial
import os
import servicesqlite as serv
import struct
 
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
print(f"Waiting for START sequence...")
while True:
    x = arduino.read(1)
    data_list += list(x)

    if data_list[-5:] == list(bytearray(b"START")):
        break

print(f"Start sequence received. Receiving data...")
while True:
    x = arduino.read(16)
    data = struct.unpack("4f", x)
    # print(data)
    db.write(data)