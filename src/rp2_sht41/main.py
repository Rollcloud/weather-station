import time
from machine import Pin, I2C
from micropython_sht4x import sht4x
import network
import urequests

WIFI_NAME = "Wifi_name"
WIFI_PASSWORD = "Wifi_password"
SERVER = "http://localhost:5000"
UPDATE_PERIOD = 60  # seconds


def connect_to_wifi(wifi_name, wifi_password):
    """Connect to WiFi network using the given SSID and password.

    Based on the example from the MicroPython documentation, 3.6. Connecting to a wireless network:
    https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf with LED feedback.

    The function will attempt to connect to the network and will toggle the onboard LED while waiting.
    If the connection is successful, the LED will turn off and the IP address will be printed.
    If the connection fails, the LED will turn on and an error will be raised.
    """
    led = Pin("LED", Pin.OUT)
    led.on()

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_name, wifi_password)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("waiting for connection...")
        led.toggle()
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        led.on()
        raise RuntimeError("network connection failed")
    else:
        led.off()
        print("connected")
        status = wlan.ifconfig()
        print("ip = " + status[0])

    return wlan


wlan = connect_to_wifi(WIFI_NAME, WIFI_PASSWORD)
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
    try:
        response = urequests.post(url=SERVER + "/data", headers=headers, json=payload)
        response.close()
    except Exception:
        # Reconnect to WiFi if the connection is lost
        if wlan.status() < 0 or wlan.status() >= 3:
            wlan.disconnect()
            wlan = connect_to_wifi(WIFI_NAME, WIFI_PASSWORD)

    time.sleep(UPDATE_PERIOD)
