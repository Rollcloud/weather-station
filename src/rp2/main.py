import json
import time

import network
import ntptime
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

# Functions___________________________


def connect_wifi():
    """
    Connect to wifi.

    wlan.status() codes:
    define CYW43_LINK_DOWN         (0)     ///< link is down
    define CYW43_LINK_JOIN         (1)     ///< Connected to wifi
    define CYW43_LINK_NOIP         (2)     ///< Connected to wifi, but no IP address
    define CYW43_LINK_UP           (3)     ///< Connect to wifi with an IP address
    define CYW43_LINK_FAIL         (-1)    ///< Connection failed
    define CYW43_LINK_NONET        (-2)    ///< No matching SSID found (could be out of range, or down)
    define CYW43_LINK_BADAUTH      (-3)    ///< Authenticatation failure
    """
    # UNCONNECTED = 0
    CONNECTING_1 = 1
    CONNECTING_2 = 2
    CONNECTED = 3

    MAX_ATTEMPTS = 3
    attempts = 0
    print(wlan.status())

    if wlan.status() == CONNECTED:
        print("connected")
        return True

    while attempts < MAX_ATTEMPTS:
        print("trying to connect...")
        if wlan.status() not in [CONNECTING_1, CONNECTING_2]:
            wlan.disconnect()
            wlan.connect(WIFI_NAME, WIFI_PASSWORD)
            attempts += 1
            time.sleep(1)

    else:
        return False


def measure_data():
    #  returns -> Dict
    bme688.measureData()

    rtc_date = rtc.readDateString()
    # rtc_date = day + "/" + month + "/" + str(self.year)
    iso_date = rtc_date[6:10] + "/" + rtc_date[3:5] + "/" + rtc_date[0:2]
    time_string = rtc.readTimeString()

    data = {
        "timestamp": iso_date + " " + time_string,
        "temperature": str(bme688.readTemperature()),
        "pressure": str(bme688.readPressure()),
        "humidity": str(bme688.readHumidity()),
        "air_quality": str(bme688.getAirQualityScore()),
        "e_co2": str(bme688.readeCO2()),
    }

    return data


def display_data(data):
    # input type: Dict
    oled.clear()
    oled.displayText("Weather Station", 1, 2)
    oled.displayText("Temp " + data["temperature"] + " C", 2, 10)
    oled.displayText("Press " + data["pressure"] + " Pa", 3, 10)
    oled.displayText("Hum " + data["humidity"] + " %", 4, 10)
    oled.displayText("IAQ " + data["air_quality"] + "/500", 5, 10)
    oled.displayText("eCO2 " + data["e_co2"] + "ppm", 6, 10)
    oled.show()

    if int(data["air_quality"]) < 100:
        zipleds.setLED(0, zipleds.GREEN)
    else:
        zipleds.setLED(0, zipleds.RED)
    if int(data["e_co2"]) < 800:
        zipleds.setLED(2, zipleds.GREEN)
    else:
        zipleds.setLED(2, zipleds.RED)
    zipleds.setBrightness(10)
    zipleds.show()


def queue_data(buffered_data, data):
    # input types:  buffered_data: List[Dict], data: Dict
    buffered_data.append(data)


def send_data(buffered_data):
    # input type: List[Dict]
    # Data/payload needs to be in byte string format to send

    HTTP_OK = 200
    HTTP_CREATED = 201
    HTTP_ACCEPTED = 202

    while len(buffered_data) > 0:
        payload = json.dumps(buffered_data[0])
        headers = {"Content-Type": "application/json"}

        if connect_wifi() is True:
            try:
                print("sending...")
                response = urequests.post(SERVER_URL, headers=headers, data=payload)
                status = response.status_code
                print(status)
                response.close()
                if status in [HTTP_OK, HTTP_CREATED, HTTP_ACCEPTED]:
                    buffered_data.pop(0)
            except Exception as e:
                print("could not send!")
                print(e)
                zipleds.setLED(1, zipleds.CYAN)
                zipleds.setBrightness(10)
                zipleds.show()


# ___________________________

if __name__ == "__main__":
    connect_wifi()
    ntptime.settime()
    rtc.getDateTime()

    counter = 295  # Sends through first reading to server, then every 5 min
    buffered_data = []

    while True:
        while counter < 300:
            data = measure_data()
            display_data(data)
            counter += 5
            time.sleep(5)

        else:
            queue_data(buffered_data, data)
            send_data(buffered_data)
            counter = 0  # reset
