import network
import urequests
import time
import machine # type: ignore

# WiFi credentials
SSID = "OPPO A9 2020"
PASSWORD = "12345678"

# Relay pins
relay_ch1 = machine.Pin(33, machine.Pin.OUT)
relay_ch2 = machine.Pin(25, machine.Pin.OUT)
relay_ch3 = machine.Pin(32, machine.Pin.OUT)

# UART setup (TX=17, RX=16)
uart = machine.UART(2, baudrate=9600, tx=17, rx=16)

# Flask server endpoint
RELAY_CONTROL_URL = "http://192.168.31.220:5000/esp32_flask"

# Connect to WiFi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)

connection_attempts = 0
while not sta.isconnected() and connection_attempts < 10:
    text = f"Connecting to Wifi: attempt = {connection_attempts}" 
    print(text)
    time.sleep(2)
    connection_attempts += 1

if sta.isconnected():
    print("Connected to WiFi, IP:", sta.ifconfig()[0])
else:
    print("Failed to connect to WiFi.")

# Function to send servo command to Arduino
def activate_arduino_servo():
    uart.write("servo\n")
    print("Sent 'servo' command to Arduino.")

# Function to check commands
def check_relay_commands():
    try:
        res = urequests.get(RELAY_CONTROL_URL)
        command_data = res.json()
        print("Command received:", command_data)

        relay_ch1.value(1 if command_data.get("relay1") else 0)
        relay_ch2.value(1 if command_data.get("relay2") else 0)
        relay_ch3.value(1 if command_data.get("relay3") else 0)

        if command_data.get("servo"):
            activate_arduino_servo()

        res.close()
    except Exception as e:
        print("Relay check error:", e)

# Polling loop
while True:
    check_relay_commands()
    time.sleep(0.5)
