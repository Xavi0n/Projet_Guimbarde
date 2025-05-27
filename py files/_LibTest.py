from huskylib import HuskyLensLibrary
import time

huskylens = HuskyLensLibrary("I2C", 0x32)  # adjust address if needed

try:
    while True:
        if huskylens.requestAll():
            print("Data received:", huskylens)
        else:
            print("Read response error, please try again")
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped")

