from machine import I2C
from utime import sleep_ms
_PWR_MGMT_1 = 0x6B
_GYRO_CONFIG = 0x1B
_ACCEL_CONFIG = 0x1C

GYRO_FULL_SCALE_RANGE = 250
ACCEL_FULL_SCALE_RANGE = 2

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
        self.accel_config()
        
    def gyro_config(self):
        data = self.i2c.readfrom_mem(self.address, _GYRO_CONFIG, 1)
        fs_sel = (data[0] >> 3) & 0b11
        if fs_sel == 0:
            GYRO_FULL_SCALE_RANGE = 250
        elif fs_sel == 1:
            GYRO_FULL_SCALE_RANGE = 500
        elif fs_sel == 2:
            GYRO_FULL_SCALE_RANGE = 1000
        elif fs_sel == 3:
            GYRO_FULL_SCALE_RANGE = 2000
        print(f"Set gyro full scale range to {GYRO_FULL_SCALE_RANGE} degrees /s")

    def accel_config(self):
        data = self.i2c.readfrom_mem(self.address, _ACCEL_CONFIG, 1)
        afs_sel = (data[0] >> 3) & 0b11
        if afs_sel == 0:
            ACCEL_FULL_SCALE_RANGE = 2
        elif afs_sel == 1:
            ACCEL_FULL_SCALE_RANGE = 4
        elif afs_sel == 2:
            ACCEL_FULL_SCALE_RANGE = 8
        elif afs_sel == 3:
            ACCEL_FULL_SCALE_RANGE = 16
        print(f"Set accel full scale range to {ACCEL_FULL_SCALE_RANGE} g")