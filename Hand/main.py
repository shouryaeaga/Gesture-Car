from machine import Pin, I2C
from utime import sleep_ms
from mpu6050 import MPU6050
from fusion import Fusion
scl = Pin(21)
sda = Pin(20)

offset_AX = -0.0002
offset_AY = 0.3302
offset_AZ = 10.8233 - 9.80665  # Adjusted for gravity
offset_GX = -3.2302
offset_GY = 0.4521
offset_GZ = -0.6837

i2c = I2C(0, scl=scl, sda=sda, freq=400000)
devices = i2c.scan()
if len(devices) != 0:
    for device in devices:
        print(f"Device found: {hex(device)}")

mpu = MPU6050(i2c)

axs = []
ays = []
azs = []
gxs = []
gys = []
gzs = []
count = 0

fusion = Fusion()

direction = "STOP"

while True:
    raw_ax, raw_ay, raw_az = mpu.read_accelerometer()
    raw_gx, raw_gy, raw_gz = mpu.read_gyroscope()

    # CALIBRATION SCRIPT
    # axs.append(raw_ax)
    # ays.append(raw_ay)
    # azs.append(raw_az)
    # gxs.append(raw_gx)
    # gys.append(raw_gy)
    # gzs.append(raw_gz)
    # count += 1
    # if count == 200:
    #     offset_AX = sum(axs) / len(axs)
    #     offset_AY = sum(ays) / len(ays)
    #     offset_AZ = sum(azs) / len(azs)
    #     offset_GX = sum(gxs) / len(gxs)
    #     offset_GY = sum(gys) / len(gys)
    #     offset_GZ = sum(gzs) / len(gzs)

    #     print(f"Offsets: AX={offset_AX:.4f}, AY={offset_AY:.4f}, AZ={offset_AZ:.4f}, GX={offset_GX:.4f}, GY={offset_GY:.4f}, GZ={offset_GZ:.4f}")
    #     break
    # END OF CALIBRATION SCRIPT 

    raw_ax -= offset_AX
    raw_ay -= offset_AY
    raw_az -= offset_AZ
    raw_gx -= offset_GX
    raw_gy -= offset_GY
    raw_gz -= offset_GZ

    fusion.update_nomag((raw_ax, raw_ay, raw_az), (raw_gx, raw_gy, raw_gz))

    # print(f"Heading: {fusion.heading:.2f} degrees, Pitch: {fusion.pitch:.2f} degrees, Roll: {fusion.roll:.2f} degrees")

    if fusion.pitch > 45:
        direction = "RIGHT"
    elif fusion.pitch < -45:
        direction = "LEFT"
    elif fusion.roll > 90:
        direction = "UP"
    elif fusion.roll < -90:
        direction = "DOWN"
    else:
        direction = "STOP"

    

    sleep_ms(5)