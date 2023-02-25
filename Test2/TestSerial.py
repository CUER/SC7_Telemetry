import serial
import time

serialPort = serial.Serial(
    port = "COM7",
    baudrate=9600,
    bytesize=8,
    stopbits=serial.STOPBITS_ONE
    )

t=time.localtime()
current_time = time.strftime("%H:%M:%S*", t)

serialPort.write(str.encode(current_time))

timeset=False
while(not(timeset)):
    current_time = time.strftime("%H:%M:%S*", time.localtime())
    #print(current_time)
    serialPort.write(str.encode(current_time))
    print(str.encode(current_time))
    if(serialPort.in_waiting != 0):
         x=serialPort.readline()
         x=str(x.decode("utf-8").strip().strip('\x00'))
         if (x=="set"):
            timeset=True
    time.sleep(1)

while(1):
        x = serialPort.readline()
        x=str(x.decode("utf-8").strip().strip('\x00'))
        print(x)
    
    #t=time.localtime()
    #current_time = time.strftime("%H:%M:%S", t)
    #x=serialPort.readline()
    #x=str(x.decode("utf-8").strip().strip('\x00'))
    #x=x.split(":")
    #stm32=[]
    #for item in x:
            #try:
              #  stm32.append(float(item))
           # except:
           #      pass
  #  python = current_time.split(":")
   # print("stm time: ", stm32)
   # print("Actual Time: ", python)
   # print("\n\n")

