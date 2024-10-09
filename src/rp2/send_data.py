from PicoAirQuality import KitronikBME688, KitronikRTC
import network
import time
import urequests
import json

SERVER_URL = 'localhost'+'/data'
WIFI_NAME = 'Wifi_name'
WIFI_PASSWORD = 'Wifi_password'

bme688 = KitronikBME688()
rtc = KitronikRTC()
bme688.setupGasSensor()
bme688.calcBaselines()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_NAME, WIFI_PASSWORD) # can set up to read these from a txt file
while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)


rtc.getDateTime() 

# #GET
# r = urequests.get(SERVER_URL)
# print(r.content)
# r.close()
# wlan.status() # should be 3

while True:
    bme688.measureData()
    
    date = rtc.readDateString()
    time_string = rtc.readTimeString()
    temperature = str(bme688.readTemperature())
    pressure = str(bme688.readPressure())
    humidity = str(bme688.readHumidity())
    air_quality = str(bme688.getAirQualityScore())
    co2 = str(bme688.readeCO2())
        
        
    
    # POST
    # Data/payload needs to be in byte string format to send 
    # Header needs to specify JSON to be received by server
    # payload = b'{"Timestamp":"value1-rp2", "Temperature (C)":"value2-rp2"}'
    payload_dict = {'Timestamp': date + ' ' + time_string, 'Temperature':temperature,
                    'Pressure':pressure, 'Humidity':humidity, 'Air Quality':air_quality, 'eCO2':co2}
    payload = json.dumps(payload_dict)
    headers = {'Content-Type': 'application/json'}
    response = urequests.post(SERVER_URL, headers=headers, data=payload)
    # response.status_code # Looking for 200; check weather.sqlite to see if data arrives :)
    response.close()
    time.sleep(5)

