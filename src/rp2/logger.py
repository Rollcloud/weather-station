from PicoAirQuality import KitronikBME688, KitronikRTC, KitronikDataLogger, KitronikOLED
import time

bme688 = KitronikBME688()
rtc = KitronikRTC()
log = KitronikDataLogger("log.txt", "semicolon")
oled = KitronikOLED()

bme688.setupGasSensor()
bme688.calcBaselines()

log.writeProjectInfo("Environmental Data Log", "", "")
log.nameColumnHeadings("Date", "Time", "Temperature (C)", "Pressure (Pa)", "Humidity (%)", "Air Quality (IAQ)", "eCO2 (ppm)")

rtc.getDateTime() 
rtc.setAlarm(rtc.hour, rtc.minute, True, 0, 1)


while True:
    
    if rtc.checkAlarm():
        oled.clearLine(3)
        oled.displayText("1 min weather", 3, 10)
        oled.displayText(rtc.readTimeString(), 4, 10)
        oled.show()
        
        bme688.measureData()
    
        date = rtc.readDateString()
        time_string = rtc.readTimeString()
        temperature = str(bme688.readTemperature())
        pressure = str(bme688.readPressure())
        humidity = str(bme688.readHumidity())
        air_quality = str(bme688.getAirQualityScore())
        co2 = str(bme688.readeCO2())
        
        log.storeDataEntry(date, time_string, temperature, pressure, humidity, air_quality, co2)
        
        time.sleep(5)
        rtc.silenceAlarm()
        oled.clearLine(3)
        oled.clearLine(4)
        oled.show()
    
        oled.displayText("Weather Station", 1, 2)
        oled.displayText("Temp " + str(bme688.readTemperature()) + " C", 2, 10)
        oled.displayText("Press " + str(bme688.readPressure()) + " Pa", 3, 10)
        oled.displayText("Hum " + str(bme688.readHumidity()) + " %", 4, 10)
        oled.displayText("IAQ " + str(bme688.getAirQualityScore()) + "/500", 5, 10)
        oled.displayText("eCO2 " + str(bme688.readeCO2()) + "ppm", 6, 10)
        oled.show()
        
        time.sleep(5)
        oled.clearLine(1)
        oled.clearLine(2)
        oled.clearLine(3)
        oled.clearLine(4)
        oled.clearLine(5)
        oled.clearLine(6)
        oled.show()

    