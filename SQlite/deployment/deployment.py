import serial
import threading
import time
 
arduino = serial.Serial(
    port='COM6',
    baudrate = 115200,
    # parity=serial.PARITY_NONE,
    # stopbits=serial.STOPBITS_ONE,
    # bytesize=serial.EIGHTBITS,
    timeout=1
)
    
print(f"Listening on port {arduino.port}")
# while True:
    # x = arduino.read()
    # print(x)
    
def get_readings():
    x = arduino.readline()

    # print(int.from_bytes(x, byteorder="little"))
    x= x.split(",")
    y=[]
    for item in x:
        y.append(int(item))
    
    return y


