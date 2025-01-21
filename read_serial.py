import serial

# Replace 'COM4' with your port
ser = serial.Serial('COM4', 115200)
while True:
    print(ser.readline().decode('utf-8').strip())
