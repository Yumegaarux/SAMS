import network # type: ignore
import urequests # type: ignore
import time
import machine # type: ignore

#------------------------------#
# change based on wifi network #
#------------------------------#

#change based on wifi ssid and password
ssid = "OPPO A9 2020"
password = "12345678"

#-------------------#
#  Global Variables #
#-------------------#

#------------#
# ESP32 Pins #
#------------#

#---------------------------------#
# establish flask server endpoint #
#---------------------------------#

#change based on server endpoint
SERVER_URL = "http://192.168.99.220:5000/esp32_flask"

#connect to wifi 
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid, password)

#loop until connected to wifi
connection_attempts = 0
while not sta.isconnected() and connection_attempts < 10:
    print("Connecting to WiFi...")
    time.sleep(2)
    connection_attempts += 1

if sta.isconnected():
    print("Connected to WiFi, IP:", sta.ifconfig()[0])
else:
    print("Failed to connect to WiFi.")

#-----------#
# UARTSetup #
#-----------#
uart = machine.UART(2, baudrate=9600, rx=16)

#-------------------------------#
#   #-----------------------#   #
#   # Pre-Defined Functions #   #
#   #-----------------------#   #
#-------------------------------#

#---------------------------#
# pH Level Sensor Functions #
#---------------------------#

# Get pH value from Arduino
def receive_salinity():
    if uart.any():
        try:
            ppt = uart.readline().decode().strip()
            ppt = float(ppt)
            print("Salnity from Arduino:", ppt)
            return ppt
        except Exception as e:
            print("UART Error:", e)
    return None

# Get pH value from Arduino
def send_to_server(slnty_val):
    try:
        response = urequests.post(SERVER_URL, json={"salinity_value": slnty_val})
        print("Server responded:", response.text)
        response.close()
    except Exception as e:
        print("Failed to send to server:", e)


#--------------------------#
#   #------------------#   #
#   # Manual Functions #   #
#   #------------------#   #
#--------------------------#

#-----------------------------#
#   #---------------------#   #
#   # Automatic Functions #   #
#   #---------------------#   #
#-----------------------------#

#------#
# Main #
#------#

while True:
    salnty = receive_salinity()
    if salnty:
        send_to_server(salnty)
    time.sleep(1)
