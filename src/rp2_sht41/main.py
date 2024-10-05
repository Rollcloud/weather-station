import time
from machine import Pin, I2C
from micropython_sht4x import sht4x
import network
import urequests

WIFI_NAME = "Wifi_name"
WIFI_PASSWORD = "Wifi_password"
SERVER = "http://localhost:5000"
UPDATE_PERIOD = 60  # seconds

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_NAME, WIFI_PASSWORD)
while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

i2c = I2C(0, sda=Pin(4), scl=Pin(5))
sht = sht4x.SHT4X(i2c)

sht.temperature_precision = sht4x.LOW_PRECISION

while True:
    temperature, relative_humidity = sht.measurements
    temperature = round(temperature, 2)
    relative_humidity = round(relative_humidity, 2)

    payload = {
        "Timestamp": time.time(),
        "Temperature": temperature,
        "Pressure": None,
        "Humidity": relative_humidity,
        "Air Quality": None,
        "eCO2": None,
    }
    headers = {"Content-Type": "application/json"}
    res = urequests.post(url=SERVER + "/data", headers=headers, json=payload)

    time.sleep(UPDATE_PERIOD)
