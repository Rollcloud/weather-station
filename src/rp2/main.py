import json
import time

import network
import urequests
from PicoAirQuality import KitronikBME688, KitronikOLED, KitronikRTC, KitronikZIPLEDs

SERVER_URL = "localhost" + "/data"
WIFI_NAME = "Wifi_name"
WIFI_PASSWORD = "Wifi_password"

bme688 = KitronikBME688()
rtc = KitronikRTC()
bme688.setupGasSensor()
bme688.calcBaselines()
oled = KitronikOLED()  # Class for using the OLED display screen
zipleds = KitronikZIPLEDs(3)  # Class for using the ZIP LEDs (on-board and external connections)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_NAME, WIFI_PASSWORD)  # can set up to read these from a txt file
while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)


rtc.getDateTime()

while True:
    bme688.measureData()

    # rtc_date = day + "/" + month + "/" + str(self.year)

    rtc_date = rtc.readDateString()
    iso_date = rtc_date[6:10] + "/" + rtc_date[3:5] + "/" + rtc_date[0:2]
    time_string = rtc.readTimeString()
    temperature = str(bme688.readTemperature())
    pressure = str(bme688.readPressure())
    humidity = str(bme688.readHumidity())
    air_quality = str(bme688.getAirQualityScore())
    co2 = str(bme688.readeCO2())

    oled.clear()
    oled.displayText("Weather Station", 1, 2)
    oled.displayText("Temp " + temperature + " C", 2, 10)
    oled.displayText("Press " + pressure + " Pa", 3, 10)
    oled.displayText("Hum " + humidity + " %", 4, 10)
    oled.displayText("IAQ " + air_quality + "/500", 5, 10)
    oled.displayText("eCO2 " + co2 + "ppm", 6, 10)
    oled.show()

    if int(air_quality) < 100:
        zipleds.setLED(0, zipleds.GREEN)
    else:
        zipleds.setLED(0, zipleds.RED)
    if int(co2) < 800:
        zipleds.setLED(2, zipleds.GREEN)
    else:
        zipleds.setLED(2, zipleds.RED)
    zipleds.setBrightness(10)
    zipleds.show()

    # POST
    # Data/payload needs to be in byte string format to send
    payload_dict = {
        "Timestamp": iso_date + " " + time_string,
        "Temperature": temperature,
        "Pressure": pressure,
        "Humidity": humidity,
        "Air Quality": air_quality,
        "eCO2": co2,
    }
    payload = json.dumps(payload_dict)
    headers = {"Content-Type": "application/json"}
    response = urequests.post(SERVER_URL, headers=headers, data=payload)
    response.close()
    time.sleep(5)
