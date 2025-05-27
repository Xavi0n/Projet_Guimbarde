from huskylib import HuskyLensLibrary
import time

def get_huskylens_data():
    
    huskylens = HuskyLensLibrary("I2C", 0x32)
    huskylens.algorithm("ALGORITHM_OBJECT_RECOGNITION")

    try:
        while True:
            time.sleep(1)  # Wait for a second before requesting data
            if (objects := huskylens.requestAll()):
                print("Data received:", objects)
                print("Debug: Raw data: {}".format([hex(x) for x in objects]))
                for obj in objects:
                    print("Object ID: {obj.id}, X: {obj.x}, Y: {obj.y}, Width: {obj.width}, Height: {obj.height}")

            else:
                print("No objects found, please try again")

    except KeyboardInterrupt:
        print("Stopped")