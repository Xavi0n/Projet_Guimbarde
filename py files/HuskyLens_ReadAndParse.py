from huskylib import HuskyLensLibrary, algorthimsByteID
import time
import sys

def RequestHuskyData():
    try:
        print("Initializing HuskyLens...", file=sys.stderr)
        huskylens = HuskyLensLibrary("I2C", 0x32)
        print("HuskyLens initialized", file=sys.stderr)

        # Requests the detected objects 3 times to ensure the data is ready
        i = 0
        while i<3:
            objects = huskylens.requestAll()
            i+= 1
            
        # Request the detected blocks    
        objects = huskylens.requestAll()
        if not objects:
            print("No objects detected", file=sys.stderr)
            return  # No output if no objects

        print(f"Found {len(objects)} objects", file=sys.stderr)
        for obj in objects:
            print(f"{obj.x} {obj.y} {obj.width} {obj.height} {obj.ID}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    RequestHuskyData()

