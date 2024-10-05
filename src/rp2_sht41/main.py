import time
from machine import Pin, I2C
from micropython_sht4x import sht4x

i2c = I2C(0, sda=Pin(4), scl=Pin(5))
sht = sht4x.SHT4X(i2c)

sht.temperature_precision = sht4x.LOW_PRECISION

while True:
    temperature, relative_humidity = sht.measurements
    print(f"Temperature: {temperature:.2f}*C")
    print(f"Relative Humidity: {relative_humidity:.2f}%")
    print("")
    time.sleep(0.5)
