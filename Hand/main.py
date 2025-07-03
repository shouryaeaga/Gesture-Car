from machine import Pin, I2C
import time
from mpu6050 import MPU6050
from lib.fusion import Fusion
from lib.umqtt import MQTTClient
import network


from config import wifi_ssid, wifi_password, mqtt_broker, mqtt_username, mqtt_password

def connect_wifi(ssid, password, timeout=10):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    print(f"Connecting to {ssid}...")
    for i in range(timeout):
        if wlan.status() == 3:
            print("Connected to WiFi!")
            print("IP address:", wlan.ifconfig()[0])
            return wlan
        else:
            print(f"Waiting ({i + 1}/{timeout})...")
            time.sleep(1)
    
    print("Connection failed with status:", wlan.status())
    raise RuntimeError("WiFi connection failed")

# Use it
wlan = connect_wifi(wifi_ssid, wifi_password)
    

try:
    print("HERE1")
    mqtt = MQTTClient("HAND_GESTURE", mqtt_broker, 8883, mqtt_username, mqtt_password, ssl=True, ssl_params={"server_hostname": mqtt_broker})
    print("HERE2")
    mqtt.connect()
    print("HERE3")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    raise

print("Connected to MQTT broker")
offset_AX = -0.0002
offset_AY = 0.3302
offset_AZ = 10.8233 - 9.80665  # Adjusted for gravity
offset_GX = -3.2302
offset_GY = 0.4521
offset_GZ = -0.6837

scl = Pin(21)
sda = Pin(20)

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
    elif fusion.roll > 45:
        direction = "UP"
    elif fusion.roll < -45:
        direction = "DOWN"
    else:
        direction = "STOP"

    mqtt.publish("gesture/direction", direction)
    time.sleep_ms(50)