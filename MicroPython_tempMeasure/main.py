import dht
import machine
import time
import socket
import network

# Wi-Fi network configuration
WIFI_NETWORK = 'Your WiFi Network'
WIFI_PASSWORD = 'Your WiFi Password'


# WiFi connection setup
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_NETWORK, WIFI_PASSWORD)
    while not wlan.isconnected():
        pass
    print('Connected to ', WIFI_NETWORK)
    
    # Flash LED four times if connection is successful
    led = machine.Pin('LED', machine.Pin.OUT)
    for _ in range(4):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
    
    return wlan

# Connect to Wi-Fi
connect_wifi()

# Initialize DHT11 sensor
d = dht.DHT11(machine.Pin(25))

# Function to read temperature and humidity
def read_sensor():
    try:
        d.measure()
        temperature = d.temperature()
        humidity = d.humidity()
        return temperature, humidity
    except OSError as e:
        print("Sensor error:", e)
        return None, None
    
# Function to read temperature and humidity
def read_sensor():
    try:
        d.measure()
        temperature = d.temperature()
        humidity = d.humidity()
        return temperature, humidity
    except OSError as e:
        print("Sensor error:", e)
        return None, None

# Create a simple HTTP server
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break

        temperature, humidity = read_sensor()
        if temperature is not None and humidity is not None:
            response = """\
HTTP/1.1 200 OK

Temperature: {:.1f} C
Humidity: {:.1f} %
""".format(temperature, humidity)
        else:
            response = """\
HTTP/1.1 500 Internal Server Error

Failed to read sensor data.
"""

        cl.send(response)
        cl.close()

# Main loop to update sensor data every minute
def main():
    import _thread
    _thread.start_new_thread(start_server, ())

    while True:
        read_sensor()
        time.sleep(600)  # Update every 10 minutes
        # Check if the Wi-Fi connection is still active
        if not wlan.isconnected():
            print('WiFi connection lost. Reconnecting...')
            wlan = connect_wifi()

main()