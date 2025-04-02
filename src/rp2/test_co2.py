import machine
import scd4x
from time import sleep

# Init SCD4X
i2c_scd4x = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=100000)
'''SDA (Serial Data) and SCL (Serial Clock) pins are used for I2C (Inter-Integrated Circuit) communication, 
a two-wire serial protocol, where SDA transmits data and SCL provides the clock signal for synchronization
SDA - blue wire - GP0 0
SCL - yellow wire - GP1 1'''

scd = scd4x.SCD4X(i2c_scd4x)
scd.start_periodic_measurement()

def update_scd4x_sensor():   
    current_temp = scd.temperature
    current_co2 = scd.co2
    current_humidity = scd.relative_humidity
        
    print(f"Temp:{current_temp}\n" +
            f"CO2:{current_co2}\n" +
            f"Humidity:{current_humidity}\n" +
            "---")

def main_loop():  

    while True: 
        update_scd4x_sensor()
        sleep(5)

if __name__ == "__main__":
    main_loop()