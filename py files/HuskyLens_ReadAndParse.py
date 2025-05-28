from huskylib import HuskyLensLibrary, algorthimsByteID
import time

def RequestHuskyData():
    huskylens = HuskyLensLibrary("I2C", 0x32)

    # Requests the detected objects 3 times to ensure the data is ready
    i = 0
    while i<3:
        objects = huskylens.requestAll()
        i+= 1
        
    # Request the detected blocks    
    objects = huskylens.requestAll()
    if not objects:
        return  # No output if no objects

    for obj in objects:
        print(f"{obj.x} {obj.y} {obj.width} {obj.height} {obj.ID}")

    return

