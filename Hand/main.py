from machine import Pin, I2C
from utime import sleep
from mpu6050 import MPU6050
scl = Pin(21)
sda = Pin(20)

i2c = I2C(0, scl=scl, sda=sda, freq=400000)
devices = i2c.scan()
if len(devices) != 0:
    for device in devices:
        print(f"Device found: {hex(device)}")

mpu = MPU6050(i2c)


while True:
    sleep(1)