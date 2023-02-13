import serial
import threading
import time
import servicesqlite as serv
 
arduino = serial.Serial(
    port='COM6',
    baudrate = 115200,
    # parity=serial.PARITY_NONE,
    # stopbits=serial.STOPBITS_ONE,
    # bytesize=serial.EIGHTBITS,
    timeout=1
)
    
def get_readings():
    x = arduino.readline()

    # print(int.from_bytes(x, byteorder="little"))
    x= x.split(",")
    y=[]
    for item in x:
        y.append(float(item))
    
    return y

# def get_readings():
#     return [5,3,4,8]