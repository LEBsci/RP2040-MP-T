import requests
import time

def read_temperature():
    url = "http://192.168.1.117"  # Replace <arduino_ip> with the actual IP address of your Arduino
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            print(response.text)
            # Extract the temperature from the response in line 1 as float
            temperature = float(response.text.split("\n")[0].split(" ")[1])
            # Extract the humidity from the response in line 2 as float
            humidity = float(response.text.split("\n")[1].split(" ")[1])
            
        else:
            print("Failed to get temperature data")
        time.sleep(600)  # Repeat every 10 seconds
    

if __name__ == "__main__":
    read_temperature()