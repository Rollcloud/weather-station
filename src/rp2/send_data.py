import network
import time
import urequests

SERVER_URL = 'localhost'+'/data'
WIFI_NAME = 'Wifi_name'
WIFI_PASSWORD = 'Wifi_password'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_NAME, WIFI_PASSWORD) # can set up to read these from a txt file
while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

# #GET
# r = urequests.get(SERVER_URL)
# print(r.content)
# r.close()
# wlan.status() # should be 3

# POST
# Data/payload needs to be in byte string format to send 
# Header needs to specify JSON to be received by server
payload = b'{"Timestamp":"value1-rp2", "Temperature (C)":"value2-rp2"}'
headers = {"Content-Type": "application/json"}
response = urequests.post(SERVER_URL, headers=headers, data=payload) 
response.status_code # Looking for 200; check weather.sqlite to see if data arrives :) 
