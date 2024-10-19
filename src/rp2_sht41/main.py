"""
Send temperature, humidity data from a SHT4x sensor to a server.

The server address, WiFi credentials, and update period are defined as constants
at the beginning of the script and should be changed as required.

After sending the data, the script will enter deep sleep mode for the specified
period, before waking up and running the main.py script again.
"""

from machine import Pin, I2C, unique_id, deepsleep
from micropython_sht4x import sht4x
import urequests
import errno
from hardware import connect_to_wifi, read_vsys, deactivate_wifi, read_location
import time

start_time = time.ticks_ms()

# Constants
WIFI_NAME = "Wifi_name"
WIFI_PASSWORD = "Wifi_password"
SERVER = "http://localhost:5000"
UPDATE_PERIOD = 60  # seconds

uid = "".join("{:02x}".format(x) for x in unique_id())  # pico hardware-based unique ID

voltage = read_vsys()
location = read_location()

try:
    i2c = I2C(0, sda=Pin(4), scl=Pin(5))
    sht = sht4x.SHT4X(i2c)
    sht.temperature_precision = sht4x.LOW_PRECISION
    temperature, relative_humidity = sht.measurements
    temperature = round(temperature, 2)
    relative_humidity = round(relative_humidity, 2)
except Exception as e:
    print("Error reading SHT4x sensor:", e)
    temperature = None
    relative_humidity = None

wlan = connect_to_wifi(WIFI_NAME, WIFI_PASSWORD)

payload = {
    "UID": uid,
    "Location": location,
    "Voltage": voltage,
    "Temperature": temperature,
    "Humidity": relative_humidity,
}
headers = {"Content-Type": "application/json"}

try:
    # Send data to the server
    response = urequests.post(url=SERVER + "/data", headers=headers, json=payload)
    response.close()
    print("Payload successfully sent")
except OSError as e:
    if e.errno == errno.ECONNABORTED:
        print("Connection aborted (ECONNABORTED)")
        print("Server not found")
    else:
        print("Error sending payload:", e)
except Exception as e:
    print("Error sending payload:", e)
    print("could not connect (status = " + str(wlan.status()) + ")")

deactivate_wifi(wlan)

end_time = time.ticks_ms()
time_taken = time.ticks_diff(end_time, start_time)
time_sleep = UPDATE_PERIOD * 1000 - time_taken

print("Going to sleep for", time_sleep, "seconds")
deepsleep(time_sleep)