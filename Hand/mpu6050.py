from machine import I2C
from utime import sleep_ms
_PWR_MGMT_1 = 0x6B
_GYRO_CONFIG = 0x1B

print("MPU6050 MODULE LOADED")

class MPU6050:
    def __init__(self, i2c: I2C, address=0x68):
        self.i2c = i2c
        self.address = address

        print("INITIATING MPU6050")

        try:
            i2c.writeto_mem(self.address, _PWR_MGMT_1, bytes([0x00]))
            sleep_ms(5)
        except Exception:
            print("Could not communicate with MPU6050")
            raise Exception

        self.gyro_config()
        
    def gyro_config(self):
        data = self.i2c.readfrom_mem(self.address, _GYRO_CONFIG, 1)
        print(data)