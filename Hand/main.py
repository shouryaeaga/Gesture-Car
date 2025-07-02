from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)
while True:
    try:
        pin.toggle()  # Toggle the LED state
        sleep(0.5)    # Wait for 0.5 seconds
        print("LED toggled")  # Print a message to the console
    except KeyboardInterrupt:
        print("Program interrupted by user")
        break

print("Exiting program")