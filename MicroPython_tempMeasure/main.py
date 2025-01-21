import dht
import machine
import time
import socket
import network

# Flash LED four times to show the device loaded successfully
led = machine.Pin('LED', machine.Pin.OUT)
for _ in range(4):
    print('Script running...')
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)


# Function to load Wi-Fi credentials from a file
def load_wifi_credentials(filepath):
    print('Loading Wi-Fi credentials...')
    creds = {}
    with open(filepath, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            creds[key] = value
    return creds

# Load Wi-Fi credentials
creds = load_wifi_credentials('creds')
WIFI_NETWORK = creds['WIFI_NETWORK']
WIFI_PASSWORD = creds['WIFI_PASSWORD']

# WiFi connection setup
def connect_wifi():
    print('Connecting to Wi-Fi...')
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

    # Print the IP address
    print('Network config:', wlan.ifconfig())
    
    return wlan

def check_wifi_connection(wlan):
    if not wlan.isconnected():
        print('Wi-Fi connection lost. Resetting device...')
        machine.reset()

# Connect to Wi-Fi
wlan = connect_wifi()

# Initialize DHT11 sensor
d = dht.DHT11(machine.Pin(25))

# Function to read temperature and humidity
def read_sensor():
    try:
        d.measure()
        temperature = d.temperature()
        humidity = d.humidity()
        print('Temperature: {} C, Humidity: {} %'.format(temperature, humidity))
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

start_server()

