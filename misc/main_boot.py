import network
import socket
import time
import machine  # type: ignore
import ujson
import urequests
import _thread
import struct

#===================#
#  Global Variables #
#===================#
dns_server = None
ap = None
connecting = False
uart = machine.UART(2, baudrate=9600, tx = 17, rx=16)

#===========================#
# Internal DNS Server Class #
#===========================#
class DNSServer:
    def __init__(self, redirect_ip):
        self.redirect_ip = redirect_ip
        self.running = True

    def start(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('0.0.0.0', 53))
            while self.running:
                try:
                    data, addr = sock.recvfrom(512)
                    request_id = data[0:2]
                    flags = b'\x81\x80'
                    qdcount = b'\x00\x01'
                    ancount = b'\x00\x01'
                    nscount = b'\x00\x00'
                    arcount = b'\x00\x00'

                    dns_header = request_id + flags + qdcount + ancount + nscount + arcount
                    dns_question = data[12:]
                    domain = ''
                    i = 0
                    length = data[12]
                    while length != 0:
                        domain += data[13+i:13+i+length].decode() + '.'
                        i += length + 1
                        length = data[12+i]

                    ip_parts = [int(i) for i in self.redirect_ip.split('.')]
                    dns_answer = b'\xc0\x0c' + b'\x00\x01' + b'\x00\x01' + b'\x00\x00\x00\x3c' + b'\x00\x04'
                    dns_answer += struct.pack('BBBB', *ip_parts)

                    response = dns_header + dns_question + dns_answer
                    sock.sendto(response, addr)
                except:
                    continue
        except OSError as e:
            print("DNS socket bind error:", e)

#=====================#
# HTML FORM for Setup #
#=====================#
html_form = """
<!DOCTYPE html>
<html>
<head>
  <title>WiFi Config</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f2f2f2;
      display: flex;
      flex-direction: columns;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }
    h2 {
      margin-bottom: 20px;
      color: #333;
    }
    form {
      background: #fff;
      padding: 20px 30px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      width: 100%;
      max-width: 320px;
      box-sizing: border-box;
    }
    input[type="text"],
    input[type="password"] {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 6px;
      box-sizing: border-box;
    }
    input[type="submit"] {
      width: 100%;
      padding: 10px;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    input[type="submit"]:hover {
      background-color: #0056b3;
    }
    input[type="submit"]:disabled {
      background-color: #ccc;
      cursor: not-allowed;
    }
  </style>
  <script>
    function disableSubmit() {
      document.getElementById('connectBtn').disabled = true;
    }
  </script>
</head>
<body>
  <h2>Enter WiFi Credentials</h2>
  <form action="/connect" method="get" onsubmit="disableSubmit()">
    <input name="ssid" type="text" placeholder="WiFi SSID" required />
    <input name="password" type="password" placeholder="Password" required />
    <input id="connectBtn" type="submit" value="Connect" />
  </form>
</body>
</html>
"""

#======================#
# Get WiFi Credentials #
#======================#

#Connect to Wifi
def run_wifi_config():
    global dns_server, ap, connecting

    while True:
        try:
            if ap:
                ap.active(False)
            if dns_server and hasattr(dns_server, 'running'):
                dns_server.running = False
        except:
            pass

        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid="ESP32_Setup", password="myaquaponics", authmode=3)
        ap_ip = ap.ifconfig()[0]
        print("AP active. Connect to ESP32_Setup:", ap_ip)

        dns_server = DNSServer(ap_ip)
        _thread.start_new_thread(dns_server.start, ())

        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 80))
        s.listen(1)

        while True:
            try:
                cl, addr = s.accept()
                print('Client connected from', addr)
                request = cl.recv(1024).decode()

                if "GET /connect?" in request:
                    query = request.split('GET /connect?')[1].split(' ')[0]
                    params = {}
                    for pair in query.split('&'):
                        if '=' in pair:
                            key, value = pair.split('=')
                            params[key] = value.replace('+', ' ')
                    ssid = params.get('ssid')
                    password = params.get('password')

                    # Reset and connect
                    sta = network.WLAN(network.STA_IF)
                    sta.active(True)
                    sta.disconnect()
                    time.sleep(1)
                    sta.connect(ssid, password)

                    try:
                        cl.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
                        cl.sendall("<h3>Connecting to WiFi...</h3>")
                        print("Connecting to:", ssid)

                        for _ in range(15):
                            if sta.isconnected():
                                break
                            time.sleep(1)

                        if sta.isconnected():
                            cl.sendall(f"<p>Connected! IP: {sta.ifconfig()[0]}</p>")
                            print("Connected successfully.")
                            cl.close()
                            s.close()
                            ap.active(False)
                            return sta
                        else:
                            cl.sendall("<p>Failed to connect. Please try again.</p>" + html_form)
                            print("Failed to connect. Restarting config mode...")
                    except OSError as e:
                        print("Socket send error:", e)
                    finally:
                        try:
                            cl.close()
                        except:
                            pass
                else:
                    try:
                        cl.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
                        cl.sendall(html_form)
                    except:
                        pass
                    finally:
                        try:
                            cl.close()
                        except:
                            pass
            except Exception as e:
                print("Client handling error:", e)
                time.sleep(1)

#Change WiFi / Reconfigure WiFi --> button to be added in frontend (soon to be tested)
def reconfigure_wifi():
    global sta_if
    print("Reconfiguring WiFi...")
    try:
        sta_if.disconnect()
        sta_if.active(False)
    except:
        pass
    sta_if = run_wifi_config()

#======================#
# Setup Flask Endpoint #
#======================#
SERVER_URL = "http://10.117.96.220:5000/esp32_flask"

#====================#
# Get Data Functions #
#====================#

# Get pH data from Arduino
def receive_sensor_data():
    global uart
    if uart.any():
        try:
            line = uart.readline().decode().strip()
            print("Raw UART:", line)
            parts = line.split(",")
            if len(parts) == 7:
                ph_val = float(parts[0])
                ppt_val = float(parts[1])
                rwl_val = float(parts[2])
                ftl_val = float(parts[3])
                phul_val = float(parts[4])
                phdl_val = float(parts[5])
                ffl_val = float(parts[6])

                print(f"""Received data:
                Water pH Level: {ph_val}
                Water Salinity (PPT): {ppt_val}
                Rainwater Collector Water Level: {rwl_val}%
                Fish Tank Water Level: {ftl_val}%
                pH Up Adjuster Level: {phul_val}%
                pH Down Adjuster Level: {phdl_val}%
                Fish Food Level: {ffl_val}%
                -------------------------------------------------""")

                return ph_val, ppt_val, rwl_val, ftl_val, phul_val, phdl_val, ffl_val
        except Exception as e:
            print("UART Error:", e)
    return None, None, None, None, None, None, None

#Send pH data to flask
def send_to_server(ph_val, ppt_val, rwl_val, ftl_val, phul_val, phdl_val, ffl_val):
    try:
        payload = {
            "ph_value": ph_val,
            "ppt_value": ppt_val,
            "rwl_value": rwl_val,
            "ftl_value": ftl_val,
            "phul_value": phul_val,
            "phdl_value": phdl_val,
            "ffl_value": ffl_val
        }
        #loop to try sending the data if ESP32 drops connection
        for i in range(3):
            try:
                response = urequests.post(SERVER_URL, json=payload)
                print("Server responded:", response.text)
                response.close()
                break
            except Exception as e:
                print(f"Attempt {i+1} failed:", e)
                time.sleep(1)
    except Exception as e:
        print("Failed to send to server:", e)

#======#
# Main #
#======#
while True:
    sta_if = run_wifi_config()
    if sta_if and sta_if.isconnected():
        print("Starting sensor reading loop...")
        while sta_if.isconnected():
            ph, ppt, rwl, ftl, phul, phdl, ffl = receive_sensor_data()
            if None not in (ph, ppt, rwl, ftl, phul, phdl, ffl):
                send_to_server(ph, ppt, rwl, ftl, phul, phdl, ffl)
            time.sleep(5)
    else:
        print("WiFi connection lost or failed. Restarting WiFi setup...")

