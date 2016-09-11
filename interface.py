import serial
ser = serial.Serial('/dev/ttyUSB0')
ser.open();
print
    "Please enter command: "
command = ser.readline();
if command == 'exit':
    ser.close()
    exit()
ser.write(command + '\r\n')
out = ""
while ser.inWaiting() > 0:
    out += (ser.read(1) + " ")
if out != '':
    print ">> " + out
